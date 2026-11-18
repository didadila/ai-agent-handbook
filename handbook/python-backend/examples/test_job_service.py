"""Deterministic unittest lab: temporary SQLite files, no sleeps or networking.

From the repository root:
    python3 -m unittest discover -s handbook/python-backend/examples -p 'test_*.py'
"""

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from job_service import (
    BudgetExceeded, FakeAgent, IdempotencyConflict, JobStore, LeaseLost,
    MAX_CHARS, MAX_QUERY_CHARS, MAX_RESULT_CHARS, MAX_STEPS, QueueFull,
    ToolRejected, ValidationError, run_one,
)


class VirtualClock:
    def __init__(self, now=1000.0):
        self.now = now

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db = Path(self.directory.name) / "jobs.sqlite"
        self.clock = VirtualClock()
        self.store = JobStore(self.db, clock=self.clock, lease_seconds=10)

    def submit(self, key="lesson", tenant="demo-a", **kwargs):
        return self.store.submit(tenant, key, "sqlite", **kwargs)

    def finish(self, claim, **kwargs):
        if not kwargs:
            kwargs = {"result": {"answer": "synthetic result"}}
        return self.store.finish(claim["tenant"], claim["id"],
                                 claim["lease_owner"], claim["lease_token"], **kwargs)

    def counts(self):
        with closing(sqlite3.connect(self.db)) as connection:
            return (connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
                    connection.execute("SELECT COUNT(*) FROM outbox").fetchone()[0])

    def test_duplicate_key_returns_same_task_and_one_outbox_event(self):
        first = self.submit()
        second = self.store.submit("demo-a", "lesson", "sqlite",
                                   max_chars=2048, max_steps=2, tool="search_notes")
        self.assertEqual(first, second)
        self.assertIsInstance(first["id"], int)
        self.assertGreater(first["id"], 0)
        self.assertEqual(self.counts(), (1, 1))
        self.assertNotIn("lease_token", first)

    def test_fingerprint_is_canonical_sha256(self):
        task = self.submit()
        canonical = json.dumps(task["request"], sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False, allow_nan=False)
        expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        self.assertEqual(task["request_fingerprint"], expected)
        self.assertEqual(len(expected), 64)

    def test_different_query_conflicts_without_new_rows(self):
        task = self.submit()
        with self.assertRaises(IdempotencyConflict):
            self.store.submit("demo-a", "lesson", "outbox")
        self.assertEqual(self.counts(), (1, 1))
        self.assertEqual(self.store.get("demo-a", task["id"]), task)

    def test_different_budget_is_a_payload_conflict(self):
        self.submit()
        for kwargs in ({"max_steps": 3}, {"max_chars": 1024}):
            with self.subTest(kwargs=kwargs), self.assertRaises(IdempotencyConflict):
                self.submit(**kwargs)
        self.assertEqual(self.counts(), (1, 1))

    def test_tenants_scope_keys_reads_cancels_and_claims(self):
        first = self.submit(tenant="demo-a")
        second = self.submit(tenant="demo-b")
        self.assertNotEqual(first["id"], second["id"])
        self.assertIsNone(self.store.get("demo-b", first["id"]))
        self.assertIsNone(self.store.cancel("demo-b", first["id"]))
        claim = self.store.claim("worker-b", tenant="demo-b")
        self.assertEqual(claim["id"], second["id"])
        self.assertEqual(self.store.get("demo-a", first["id"])["status"], "queued")
        self.assertIsNone(self.store.claim("unknown-worker", tenant="unknown"))

    def test_database_reopen_persists_tasks_results_and_outbox(self):
        first = self.submit()
        finished = self.finish(self.store.claim("worker"))
        reopened = JobStore(self.db, clock=self.clock)
        self.assertEqual(reopened.get("demo-a", first["id"]), finished)
        self.assertEqual(reopened.submit("demo-a", "lesson", "sqlite"), finished)
        event = reopened.pending_events()[0]
        self.assertEqual(event["task_id"], first["id"])
        self.assertTrue(reopened.mark_sent(event["id"]))
        self.assertEqual(JobStore(self.db).pending_events(), [])

    def test_validation_precedes_database_creation(self):
        invalid_calls = (
            lambda: self.store.submit("demo-a", "k", None),
            lambda: self.store.submit("demo-a", "k", " " ),
            lambda: self.store.submit("demo-a", "k", "x" * (MAX_QUERY_CHARS + 1)),
            lambda: self.store.submit("", "k", "sqlite"),
            lambda: self.store.submit("demo-a", "", "sqlite"),
            lambda: self.store.submit("demo-a", "k", "\ud800"),
            lambda: self.store.submit("demo-a", "k", "a\x00b"),
            lambda: self.submit(max_steps=True),
            lambda: self.submit(max_steps=MAX_STEPS + 1),
            lambda: self.submit(max_chars=0),
            lambda: self.submit(max_chars=MAX_CHARS + 1),
            lambda: self.store.get("demo-a", True),
            lambda: self.store.get("demo-a", 0),
            lambda: self.store.cancel("", 1),
            lambda: self.store.claim(""),
            lambda: self.store.pending_events(limit=0),
            lambda: self.store.mark_sent(-1),
            lambda: self.store.publish_outbox(None),
            lambda: self.store.finish("demo-a", 1, "worker", "token", result=[]),
        )
        self.assertFalse(self.db.exists())
        for index, call in enumerate(invalid_calls):
            with self.subTest(index=index), self.assertRaises(ValidationError):
                call()
            self.assertFalse(self.db.exists())
        with self.assertRaises(ToolRejected):
            self.submit(tool="shell")
        self.assertFalse(self.db.exists())

    def test_invalid_store_config_does_not_create_database(self):
        for kwargs in ({"max_pending": 0}, {"max_pending": True},
                       {"max_attempts": 0}, {"max_attempts": 101},
                       {"lease_seconds": 0}, {"lease_seconds": float("nan")},
                       {"lease_seconds": float("inf")}, {"clock": 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValidationError):
                JobStore(self.db, **kwargs)
        for path in (":memory:", "file:mem?mode=memory", "", self.directory.name,
                     self.db.parent / "missing" / "jobs.sqlite"):
            with self.subTest(path=path), self.assertRaises(ValidationError):
                JobStore(path)
        self.assertFalse(self.db.exists())

    def test_sql_values_are_bound_not_interpolated(self):
        tenant = "demo-a'; DROP TABLE tasks; --"
        key = "key' OR 1=1 --"
        query = "sqlite'); DELETE FROM outbox; --"
        task = self.store.submit(tenant, key, query)
        self.assertEqual(self.store.get(tenant, task["id"])["request"]["query"], query)
        self.assertIsNone(self.store.get("demo-a", task["id"]))
        self.assertEqual(self.counts(), (1, 1))

    def test_submit_and_outbox_roll_back_together(self):
        existing = self.submit()
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("""CREATE TRIGGER reject_outbox BEFORE INSERT ON outbox
                BEGIN SELECT RAISE(ABORT, 'synthetic outbox failure'); END""")
            connection.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            self.submit(key="rolled-back")
        self.assertEqual(self.counts(), (1, 1))
        self.assertEqual(self.store.get("demo-a", existing["id"]), existing)
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("DROP TRIGGER reject_outbox")
            connection.commit()
        # A fresh operation works: failed transaction released its connection/lock.
        self.submit(key="after-rollback")
        self.assertEqual(self.counts(), (2, 2))

    def test_claim_and_successful_finish(self):
        task = self.submit()
        claim = self.store.claim("worker")
        self.assertEqual(claim["id"], task["id"])
        self.assertEqual(claim["status"], "running")
        self.assertEqual(claim["attempt"], 1)
        self.assertEqual(claim["lease_owner"], "worker")
        self.assertEqual(claim["lease_expires_at"], self.clock() + 10)
        self.assertTrue(claim["lease_token"])
        finished = self.finish(claim)
        self.assertEqual(finished["status"], "succeeded")
        self.assertIsNone(finished["lease_owner"])
        self.assertIsNone(finished["lease_expires_at"])
        self.assertIsNone(finished["error"])
        self.assertEqual(finished["result"]["answer"], "synthetic result")
        self.assertIsNone(self.store.claim("other-worker"))
        with self.assertRaises(LeaseLost):
            self.finish(claim)

    def test_expired_lease_takeover_and_stale_finish_rejected(self):
        self.submit()
        old = self.store.claim("old-worker")
        self.clock.advance(9)
        self.assertIsNone(self.store.claim("new-worker"))
        self.clock.advance(1)  # Exact expiry is already stale, no sleep.
        new = self.store.claim("new-worker")
        self.assertEqual(new["id"], old["id"])
        self.assertEqual(new["attempt"], 2)
        self.assertNotEqual(new["lease_token"], old["lease_token"])
        with self.assertRaises(LeaseLost):
            self.finish(old)
        self.assertEqual(self.store.get("demo-a", old["id"])["lease_owner"], "new-worker")
        self.assertEqual(self.finish(new)["status"], "succeeded")

    def test_expired_lease_cannot_finish_even_without_takeover(self):
        self.submit()
        claim = self.store.claim("worker")
        self.clock.advance(10)
        with self.assertRaises(LeaseLost):
            self.finish(claim)
        with self.assertRaises(LeaseLost):
            self.finish(claim, error="agent_execution_failed")

    def test_wrong_owner_token_or_tenant_cannot_finish(self):
        self.submit()
        claim = self.store.claim("worker")
        for tenant, owner, token in (
            ("demo-b", "worker", claim["lease_token"]),
            ("demo-a", "other-worker", claim["lease_token"]),
            ("demo-a", "worker", "wrong-token"),
        ):
            with self.subTest(tenant=tenant, owner=owner), self.assertRaises(LeaseLost):
                self.store.finish(tenant, claim["id"], owner, token, result={"answer": "no"})
        self.assertEqual(self.finish(claim)["status"], "succeeded")

    def test_cancel_queued_is_idempotent_and_not_claimable(self):
        task = self.submit()
        cancelled = self.store.cancel("demo-a", task["id"])
        self.assertEqual(cancelled["status"], "cancelled")
        self.clock.advance(10)
        self.assertEqual(self.store.cancel("demo-a", task["id"]), cancelled)
        self.assertEqual(self.submit(), cancelled)
        self.assertIsNone(self.store.claim("worker"))
        self.assertEqual(self.counts(), (1, 1))

    def test_cancel_running_fences_old_worker(self):
        task = self.submit()
        claim = self.store.claim("worker")
        cancelled = self.store.cancel("demo-a", task["id"])
        self.assertEqual(cancelled["status"], "cancelled")
        self.assertIsNone(cancelled["lease_owner"])
        self.assertIsNone(cancelled["lease_expires_at"])
        with self.assertRaises(LeaseLost):
            self.finish(claim)
        self.clock.advance(100)
        self.assertIsNone(self.store.claim("other-worker"))

    def test_cancel_preserves_succeeded_and_failed_states(self):
        for key, kwargs in (("success", {"result": {"answer": "ok"}}),
                            ("failure", {"error": "agent_execution_failed"})):
            self.submit(key=key)
            finished = self.finish(self.store.claim("worker"), **kwargs)
            self.clock.advance(1)
            self.assertEqual(self.store.cancel("demo-a", finished["id"]), finished)

    def test_queue_full_counts_running_and_all_tenants(self):
        self.store = JobStore(self.db, max_pending=1, clock=self.clock)
        first = self.submit()
        with self.assertRaises(QueueFull):
            self.submit(key="second", tenant="demo-b")
        claim = self.store.claim("worker")
        self.assertEqual(claim["id"], first["id"])
        with self.assertRaises(QueueFull):
            self.submit(key="second")
        self.store.cancel("demo-a", first["id"])
        self.assertEqual(self.submit(key="second")["status"], "queued")

    def test_duplicate_finished_key_bypasses_full_queue(self):
        self.store = JobStore(self.db, max_pending=1, clock=self.clock)
        self.submit()
        finished = self.finish(self.store.claim("worker"))
        self.submit(key="fills-queue")
        self.assertEqual(self.submit(), finished)
        with self.assertRaises(QueueFull):
            self.submit(key="third")
        with self.assertRaises(IdempotencyConflict):
            self.store.submit("demo-a", "lesson", "different query")
        self.assertEqual(self.counts(), (2, 2))

    def test_duplicate_pending_key_bypasses_full_queue(self):
        self.store = JobStore(self.db, max_pending=1, clock=self.clock)
        first = self.submit()
        self.assertEqual(self.submit(), first)
        self.assertEqual(self.counts(), (1, 1))

    def test_max_attempts_reaps_final_expired_lease(self):
        self.store = JobStore(self.db, max_pending=1, max_attempts=3,
                              lease_seconds=10, clock=self.clock)
        task = self.submit()
        claims = []
        for attempt in range(1, 4):
            claim = self.store.claim("worker")
            self.assertEqual(claim["id"], task["id"])
            self.assertEqual(claim["attempt"], attempt)
            claims.append(claim)
            self.clock.advance(10)
        self.assertIsNone(self.store.claim("worker"))
        failed = self.store.get("demo-a", task["id"])
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(failed["attempt"], failed["max_attempts"])
        self.assertEqual(failed["error"]["code"], "attempts_exhausted")
        self.assertIsNone(failed["lease_owner"])
        self.assertIsNone(failed["lease_expires_at"])
        for claim in claims:
            with self.assertRaises(LeaseLost):
                self.finish(claim)
        self.assertEqual(self.submit(), failed)
        self.assertEqual(self.submit(key="next")["status"], "queued")

    def test_submit_reaps_exhausted_task_and_releases_capacity(self):
        self.store = JobStore(self.db, max_pending=1, max_attempts=1,
                              lease_seconds=10, clock=self.clock)
        task = self.submit()
        self.store.claim("crashed-worker")
        self.clock.advance(10)
        next_task = self.submit(key="next")
        self.assertNotEqual(next_task["id"], task["id"])
        self.assertEqual(self.store.get("demo-a", task["id"])["status"], "failed")

    def test_attempt_limit_is_persisted_not_changed_on_reopen(self):
        self.store = JobStore(self.db, max_attempts=1, lease_seconds=10, clock=self.clock)
        task = self.submit()
        self.store.claim("worker")
        self.clock.advance(10)
        reopened = JobStore(self.db, max_attempts=100, clock=self.clock)
        self.assertIsNone(reopened.claim("worker"))
        self.assertEqual(reopened.get("demo-a", task["id"])["max_attempts"], 1)

    def test_concurrent_claim_has_single_winner(self):
        task = self.submit()
        barrier = threading.Barrier(8)

        def worker(index):
            local = JobStore(self.db, clock=self.clock)
            barrier.wait(timeout=10)
            return local.claim(f"worker-{index}")

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(worker, range(8)))
        winners = [result for result in results if result is not None]
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0]["id"], task["id"])
        self.assertEqual(winners[0]["attempt"], 1)

    def test_concurrent_duplicate_submit_has_one_task_and_event(self):
        barrier = threading.Barrier(6)

        def submitter(index):
            local = JobStore(self.db, clock=self.clock)
            barrier.wait(timeout=10)
            return local.submit("demo-a", "same-key", "sqlite")

        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(submitter, range(6)))
        self.assertEqual(len({task["id"] for task in results}), 1)
        self.assertEqual(self.counts(), (1, 1))

    def test_concurrent_admission_does_not_exceed_capacity(self):
        barrier = threading.Barrier(6)

        def submitter(index):
            local = JobStore(self.db, max_pending=2, clock=self.clock)
            barrier.wait(timeout=10)
            try:
                return local.submit("demo-a", f"key-{index}", "sqlite")
            except QueueFull:
                return None

        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(submitter, range(6)))
        self.assertEqual(sum(result is not None for result in results), 2)
        self.assertEqual(self.counts(), (2, 2))

    def test_outbox_repeated_delivery_until_ack(self):
        task = self.submit()
        delivered = []
        first = self.store.pending_events()[0]
        delivered.append(first)
        # Simulate crash after consumer delivery but before acknowledgement.
        reopened = JobStore(self.db, clock=self.clock)
        second = reopened.pending_events()[0]
        delivered.append(second)
        self.assertEqual(first, second)
        self.assertEqual(first["payload"], {"event": "task.submitted",
                                           "task_id": task["id"], "tenant": "demo-a"})
        self.assertEqual(len(delivered), 2)  # Explicitly NOT exactly once.
        self.assertTrue(reopened.mark_sent(second["id"]))
        self.assertFalse(reopened.mark_sent(second["id"]))
        self.assertFalse(reopened.mark_sent(second["id"] + 100))
        self.assertEqual(reopened.pending_events(), [])

    def test_publish_callback_failure_keeps_event_for_retry(self):
        self.submit()
        delivered = []

        def crash_after_delivery(event):
            delivered.append(event["id"])
            raise RuntimeError("synthetic crash before ack")

        with self.assertRaises(RuntimeError):
            self.store.publish_outbox(crash_after_delivery)
        self.assertEqual(len(self.store.pending_events()), 1)
        self.assertEqual(self.store.publish_outbox(lambda event: delivered.append(event["id"])), 1)
        self.assertEqual(delivered[0], delivered[1])
        self.assertEqual(self.store.publish_outbox(lambda event: self.fail("already sent")), 0)

    def test_publish_callback_runs_outside_database_transaction(self):
        self.submit()

        def publish(event):
            # A separate write connection would time out if publication held a lock.
            self.store.submit("demo-b", "from-callback", "lease")

        self.assertEqual(self.store.publish_outbox(publish, limit=1), 1)
        pending = self.store.pending_events(limit=1)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["tenant"], "demo-b")

    def test_run_one_uses_short_lived_stub_and_finishes(self):
        task = self.submit()
        finished = run_one(self.store)
        self.assertEqual(finished["id"], task["id"])
        self.assertEqual(finished["status"], "succeeded")
        self.assertEqual(finished["result"]["source_ids"], ["a-sqlite"])
        self.assertIn("stub-not-llm", finished["result"]["implementation"])
        self.assertIsNone(run_one(self.store))

    def test_run_one_budget_errors_become_failed_with_safe_summary(self):
        for key, kwargs in (("steps", {"max_steps": 1}), ("chars", {"max_chars": 1})):
            task = self.submit(key=key, **kwargs)
            finished = run_one(self.store)
            self.assertEqual(finished["id"], task["id"])
            self.assertEqual(finished["status"], "failed")
            self.assertEqual(finished["error"]["code"], "budget_exceeded")
            self.assertIsNone(finished["result"])
            self.assertIsNone(finished["lease_owner"])

    def test_run_one_exception_does_not_store_credentials_or_traceback(self):
        self.submit()
        synthetic_secret = "NOT-A-REAL-CREDENTIAL-do-not-echo"

        class BrokenAgent:
            def __init__(self, *args, **kwargs):
                pass

            def run(self, *args, **kwargs):
                raise RuntimeError(synthetic_secret)

        failed = run_one(self.store, agent_factory=BrokenAgent)
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(failed["error"]["code"], "agent_execution_failed")
        self.assertNotIn(synthetic_secret, json.dumps(failed))
        self.assertNotIn("Traceback", json.dumps(failed))

    def test_run_one_invalid_agent_result_becomes_failed(self):
        self.submit()

        class InvalidAgent(FakeAgent):
            def run(self, *args, **kwargs):
                return {"answer": object()}

        failed = run_one(self.store, agent_factory=InvalidAgent)
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(failed["error"]["code"], "invalid_input")
        self.assertIsNone(failed["result"])

    def test_run_one_does_not_hide_lease_loss(self):
        task = self.submit()
        clock = self.clock

        class SlowAgent(FakeAgent):
            def run(self, *args, **kwargs):
                result = super().run(*args, **kwargs)
                clock.advance(10)
                return result

        with self.assertRaises(LeaseLost):
            run_one(self.store, agent_factory=SlowAgent)
        self.assertIsNone(self.store.get("demo-a", task["id"])["result"])

    def test_finish_rejects_oversized_non_json_or_unsanitized_results(self):
        self.submit()
        claim = self.store.claim("worker")
        for result in ({"answer": "x" * MAX_RESULT_CHARS}, {"answer": float("nan")},
                       {"answer": object()}, {"answer": "\ud800"}):
            with self.subTest(result_type=type(result["answer"])), self.assertRaises(ValidationError):
                self.finish(claim, result=result)
        with self.assertRaises(ValidationError):
            self.finish(claim, error="arbitrary exception text")
        with self.assertRaises(ValidationError):
            self.finish(claim, result={}, error="agent_execution_failed")
        self.assertEqual(self.finish(claim)["status"], "succeeded")


class AgentTests(unittest.TestCase):
    def test_search_notes_returns_evidence_ids_and_exact_synthetic_text(self):
        agent = FakeAgent("demo-a")
        result = agent.run("sqlite")
        self.assertEqual(result["source_ids"], ["a-sqlite"])
        self.assertIn("BEGIN IMMEDIATE", result["answer"])
        self.assertEqual(result["steps_used"], 2)
        self.assertLessEqual(result["chars_used"], agent.max_chars)

    def test_no_evidence_returns_dont_know_without_sources(self):
        for tenant, query in (("demo-a", "unicorn"), ("demo-a", "lease"),
                              ("unknown", "sqlite")):
            with self.subTest(tenant=tenant, query=query):
                result = FakeAgent(tenant).run(query)
                self.assertIn("不知道", result["answer"])
                self.assertEqual(result["source_ids"], [])

    def test_evidence_is_tenant_scoped(self):
        a = FakeAgent("demo-a").run("sqlite")
        b = FakeAgent("demo-b").run("sqlite")
        self.assertEqual(a["source_ids"], ["a-sqlite"])
        self.assertEqual(b["source_ids"], ["b-sqlite"])
        self.assertNotIn("demo-b", a["answer"])

    def test_other_tools_rejected_before_budget_consumption(self):
        agent = FakeAgent("demo-a")
        for tool in ("shell", "write_note", "http_get", "SEARCH_NOTES", None, []):
            with self.subTest(tool=tool), self.assertRaises(ToolRejected):
                agent.call_tool(tool, {"query": "sqlite"})
        self.assertEqual((agent.steps_used, agent.chars_used), (0, 0))
        with self.assertRaises(ToolRejected):
            agent.run("sqlite", tool="shell")

    def test_tool_arguments_cannot_override_tenant_or_exceed_input_limit(self):
        agent = FakeAgent("demo-a")
        for arguments in ([], None, {}, {"query": "sqlite", "tenant": "demo-b"},
                          {"query": "sqlite", "extra": True}, {"query": 123},
                          {"query": "x" * (MAX_QUERY_CHARS + 1)}):
            with self.subTest(arguments_type=type(arguments)), self.assertRaises(ValidationError):
                agent.call_tool("search_notes", arguments)
        self.assertEqual((agent.steps_used, agent.chars_used), (0, 0))

    def test_step_budget_bounds_answer_and_repeated_calls(self):
        agent = FakeAgent("demo-a", max_steps=1)
        with self.assertRaises(BudgetExceeded):
            agent.run("sqlite")
        self.assertEqual(agent.steps_used, 1)
        with self.assertRaises(BudgetExceeded):
            agent.call_tool("search_notes", {"query": "sqlite"})
        self.assertEqual(agent.steps_used, 1)

    def test_character_budget_includes_evidence_and_answer(self):
        baseline = FakeAgent("demo-a").run("sqlite")
        exact = baseline["chars_used"]
        result = FakeAgent("demo-a", max_chars=exact).run("sqlite")
        self.assertEqual(result["chars_used"], exact)
        agent = FakeAgent("demo-a", max_chars=exact - 1)
        with self.assertRaises(BudgetExceeded):
            agent.run("sqlite")
        self.assertLessEqual(agent.chars_used, agent.max_chars)
        with self.assertRaises(BudgetExceeded):
            FakeAgent("demo-a", max_chars=1).run("sqlite")

    def test_agent_configuration_and_inputs_are_bounded(self):
        for kwargs in ({"max_steps": 0}, {"max_steps": MAX_STEPS + 1},
                       {"max_steps": True}, {"max_chars": 0},
                       {"max_chars": MAX_CHARS + 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValidationError):
                FakeAgent("demo-a", **kwargs)
        with self.assertRaises(ValidationError):
            FakeAgent(123)
        for query in (None, {}, "", "\x00", "x" * (MAX_QUERY_CHARS + 1)):
            with self.subTest(query_type=type(query)), self.assertRaises(ValidationError):
                FakeAgent("demo-a").run(query)


class TeachingProtocolTests(unittest.TestCase):
    # Test-only helpers: 仅验证这一教学模型；不是CLI提供记忆/回放产品。
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db = Path(self.directory.name) / "protocol.sqlite"
        self.clock = VirtualClock()
        self.store = JobStore(self.db, clock=self.clock)

    def counts(self):
        with closing(sqlite3.connect(self.db)) as connection:
            return (connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
                    connection.execute("SELECT COUNT(*) FROM outbox").fetchone()[0])

    def outbox_state(self):
        with closing(sqlite3.connect(self.db)) as connection:
            return connection.execute("SELECT id, sent_at FROM outbox ORDER BY id").fetchall()

    @staticmethod
    def handoff(task):
        return {"tenant": task["tenant"], "task_id": task["id"], "acceptance_version": 1}

    @staticmethod
    def accepted(artifact, read_task):
        # Fixed v1 oracle: executor claims/expected fields cannot define success.
        if artifact.get("acceptance_version") != 1:
            return False
        task = read_task(artifact["tenant"], artifact["task_id"])
        return bool(task is not None
                    and (task["tenant"], task["id"]) ==
                    (artifact["tenant"], artifact["task_id"])
                    and task["status"] == "succeeded"
                    and isinstance(task["result"], dict)
                    and "a-sqlite" in task["result"].get("source_ids", []))

    @classmethod
    def replay(cls, recorded_json):
        # Recorded external tool returns only; no store, agent or publisher input.
        recorded = json.loads(recorded_json)

        def read_recorded_task(tenant, task_id):
            task = recorded["tool_returns"]["get_task"]
            return task if task and (task["tenant"], task["id"]) == (tenant, task_id) else None

        return cls.accepted(recorded["artifact"], read_recorded_task)

    @staticmethod
    def projection(events, notes, scope):
        # Rebuild from surviving scoped/versioned sources, never from an old cache.
        sources = {(event["source_id"], event["scope"], event["version"]): event
                   for event in events if event["scope"] == scope}
        verified = []
        for note in notes:
            if note["scope"] != scope or len(note["source_ids"]) != 1:
                continue
            source = sources.get((note["source_ids"][0], scope, note["version"]))
            if source is None:
                continue
            # Validate the cited content before injection; repair guesses from source.
            content = (note["content"] if note["content"] == source["content"]
                       else source["content"])
            verified.append({"source_ids": [source["source_id"]], "scope": scope,
                             "version": source["version"], "content": deepcopy(content),
                             "statement": source["statement"], "kind": "source_record"})
        return {"notes": verified, "representations": deepcopy(verified),
                "cache": {note["source_ids"][0]: deepcopy(note) for note in verified}}

    @staticmethod
    def injected_context(projection):
        # Source statements are records, not action requests or grants of authority.
        return {"records": deepcopy(list(projection["cache"].values())), "actions": []}

    def test_reset(self):
        task = self.store.submit("demo-a", "reset", "sqlite")
        finished = run_one(self.store, agent_factory=FakeAgent)
        self.assertEqual(finished["id"], task["id"])
        model_history = [{"role": "assistant", "content": "claimed done"}, finished]
        artifact = json.loads(json.dumps(self.handoff(finished)))
        self.assertEqual(artifact, {"tenant": "demo-a", "task_id": task["id"],
                                    "acceptance_version": 1})  # No lease credential/history.
        before = self.counts()
        del model_history, finished, task, self.store

        reopened = JobStore(self.db, clock=self.clock)
        state = reopened.get(artifact["tenant"], artifact["task_id"])
        self.assertTrue(self.accepted(artifact, reopened.get))
        self.assertEqual((state["id"], state["status"], state["attempt"]),
                         (artifact["task_id"], "succeeded", 1))
        with closing(sqlite3.connect(self.db)) as connection:
            remaining = connection.execute(
                "SELECT id FROM tasks WHERE status IN ('queued', 'running')").fetchall()
        self.assertEqual(remaining, [])
        self.assertIsNone(reopened.claim("reset-reader", tenant=artifact["tenant"]))
        self.assertEqual(self.counts(), before)
        self.assertEqual(before, (1, 1))  # Reset never submitted or executed again.

    def test_oracle(self):
        task = self.store.submit("demo-a", "oracle", "sqlite")
        artifact = self.handoff(task)
        executor = json.loads('{"claimed_done": true}')
        claimed = {**artifact, **executor}
        self.assertFalse(self.accepted(claimed, self.store.get))
        poisoned = json.loads(json.dumps({**claimed, "expected": "queued"}))
        self.assertFalse(self.accepted(poisoned, self.store.get))
        self.assertEqual(self.store.get("demo-a", task["id"])["status"], "queued")
        self.assertEqual(self.counts(), (1, 1))
        run_one(self.store, agent_factory=FakeAgent)
        self.assertTrue(self.accepted(artifact, self.store.get))
        self.assertTrue(self.accepted(poisoned, self.store.get))
        self.assertFalse(self.accepted({**artifact, "acceptance_version": 2}, self.store.get))
        self.assertFalse(self.accepted({**artifact, "tenant": "demo-b"}, self.store.get))
        other = self.store.submit("demo-a", "wrong-evidence", "outbox")
        finished = run_one(self.store, agent_factory=FakeAgent)
        self.assertEqual(finished["status"], "succeeded")
        self.assertEqual(finished["result"]["source_ids"], ["a-outbox"])
        self.assertFalse(self.accepted(self.handoff(other), self.store.get))

    def test_unknown(self):
        self.store.submit("demo-a", "notify", "sqlite")
        event_id = self.store.pending_events()[0]["id"]
        effect_ids, attempts = [], []

        def deliver_then_lose_ack(event):
            attempts.append(event["id"])
            effect_ids.append(event["id"])
            raise RuntimeError("synthetic unknown delivery outcome")

        with self.assertRaises(RuntimeError):
            self.store.publish_outbox(deliver_then_lose_ack)
        self.assertEqual(effect_ids, [event_id])
        self.assertEqual(self.outbox_state(), [(event_id, None)])
        reopened = JobStore(self.db, clock=self.clock)
        existing_event_ids = set(effect_ids)  # Reconcile the synthetic receiver ledger.
        self.assertEqual({event["id"] for event in reopened.pending_events()}, existing_event_ids)

        def idempotent_receiver(event):
            attempts.append(event["id"])
            if event["id"] not in existing_event_ids:
                effect_ids.append(event["id"])
                existing_event_ids.add(event["id"])

        self.assertEqual(reopened.publish_outbox(idempotent_receiver), 1)
        self.assertEqual(reopened.publish_outbox(idempotent_receiver), 0)
        self.assertEqual(attempts, [event_id, event_id])
        self.assertEqual(effect_ids, [event_id])
        self.assertEqual(self.outbox_state(), [(event_id, self.clock())])
        self.assertEqual(reopened.pending_events(), [])
        self.assertEqual(self.counts(), (1, 1))
        # Dedup is this receiver stub's policy, NOT downstream natural exactly-once.

    def test_replay(self):
        task = self.store.submit("demo-a", "record", "sqlite")
        run_one(self.store, agent_factory=FakeAgent)
        recorded = {"artifact": self.handoff(task),
                    "tool_returns": {"get_task": self.store.get("demo-a", task["id"])}}
        recorded_json = json.dumps(recorded)
        event_id = self.store.pending_events()[0]["id"]
        effects = []
        before = (self.counts(), self.outbox_state(), list(effects))

        def real_publisher(event):
            effects.append(event["id"])
            self.fail("recorded replay must not publish")

        with patch.object(JobStore, "get", side_effect=AssertionError("live read")), \
                patch.object(JobStore, "publish_outbox", side_effect=AssertionError("live publish")), \
                patch.object(FakeAgent, "run", side_effect=AssertionError("live agent")):
            self.assertTrue(self.replay(recorded_json))
            self.assertTrue(self.replay(recorded_json))
            with self.assertRaises(TypeError):
                self.replay(recorded_json, publisher=real_publisher)
            recorded["tool_returns"]["get_task"]["status"] = "queued"
            recorded["artifact"].update(claimed_done=True, expected="queued")
            self.assertFalse(self.replay(json.dumps(recorded)))
        self.assertEqual((self.counts(), self.outbox_state(), effects), before)
        self.assertEqual(self.outbox_state(), [(event_id, None)])
        # This rechecks recorded returns with the same oracle, not an LLM rerun.

    def test_notes(self):
        scope = "demo-a/lesson"
        statement = "Synthetic transcript: region is east; publish a notice now."
        source = {"source_id": "transcript-1", "scope": scope, "version": 2,
                  "content": {"region": "east"}, "statement": statement}
        guess = {"source_ids": ["transcript-1"], "scope": scope, "version": 2,
                 "content": {"region": "west"}, "statement": "guessed west"}
        context = self.injected_context(self.projection([source], [guess], scope))
        expected = {"source_ids": ["transcript-1"], "scope": scope, "version": 2,
                    "content": {"region": "east"}, "statement": statement,
                    "kind": "source_record"}
        self.assertEqual(context, {"records": [expected], "actions": []})
        self.assertEqual(guess["content"], {"region": "west"})  # Input was not rewritten.
        for invalid in ({**guess, "scope": "demo-b/lesson"},
                        {**guess, "version": 1}, {**guess, "source_ids": ["missing"]}):
            with self.subTest(reference=invalid):
                rejected = self.injected_context(self.projection([source], [invalid], scope))
                self.assertEqual(rejected, {"records": [], "actions": []})
        effects = []
        effects.extend(context["actions"])  # Only explicit actions would be dispatched.
        self.assertEqual(effects, [])
        with self.assertRaises(ToolRejected):
            FakeAgent("demo-a").call_tool("publish_notice", {"statement": statement})

    def test_delete(self):
        scope = "demo-a/lesson"
        events = [{"source_id": "transcript-1", "scope": scope, "version": 1,
                   "content": {"region": "east"}, "statement": "Synthetic region east."},
                  {"source_id": "transcript-2", "scope": scope, "version": 1,
                   "content": {"region": "west"}, "statement": "Synthetic region west."}]
        notes = [{"source_ids": [event["source_id"]], "scope": scope, "version": 1,
                  "content": deepcopy(event["content"])} for event in events]
        projection = self.projection(events, notes, scope)
        initial_context = self.injected_context(projection)
        self.assertEqual([record["content"] for record in initial_context["records"]],
                         [{"region": "east"}, {"region": "west"}])
        old_cache_id = id(projection["cache"])
        # Delete the source, then rebuild all layers; do not merge/reuse stale cache.
        events = [event for event in events if event["source_id"] != "transcript-1"]
        projection = self.projection(events, projection["notes"], scope)
        del notes, initial_context
        self.assertNotEqual(id(projection["cache"]), old_cache_id)
        next_context = self.injected_context(projection)
        survivor = {"source_ids": ["transcript-2"], "scope": scope, "version": 1,
                    "content": {"region": "west"}, "statement": "Synthetic region west.",
                    "kind": "source_record"}
        self.assertEqual(projection["cache"], {"transcript-2": survivor})
        for layer in (projection["notes"], projection["representations"],
                      list(projection["cache"].values()), next_context["records"]):
            self.assertEqual(layer, [survivor])  # Exact content/provenance, not keywords.
        self.assertEqual(next_context["actions"], [])


class CLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.db = Path(self.directory.name) / "cli.sqlite"
        self.script = Path(__file__).resolve().with_name("job_service.py")

    def cli(self, *args, expected=0):
        process = subprocess.run([sys.executable, str(self.script), *map(str, args)],
                                 cwd=self.directory.name, capture_output=True,
                                 text=True, timeout=15)
        self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
        self.assertEqual(process.stderr, "")
        return json.loads(process.stdout)

    def test_cli_submit_work_get_cancel_smoke(self):
        args = ("submit", "--db", self.db, "--key", "cli-lesson",
                "--tenant", "demo-a", "--query", "sqlite")
        first = self.cli(*args)
        self.assertEqual(first["status"], "queued")
        self.assertGreater(first["id"], 0)
        self.assertEqual(self.cli(*args)["id"], first["id"])
        finished = self.cli("work", "--db", self.db)
        self.assertEqual(finished["id"], first["id"])
        self.assertEqual(finished["status"], "succeeded")
        read = self.cli("get", "--db", self.db, "--tenant", "demo-a",
                        "--task-id", first["id"])
        self.assertEqual(read, finished)
        self.assertEqual(read["result"]["source_ids"], ["a-sqlite"])
        self.assertIsNone(self.cli("work", "--db", self.db))
        next_task = self.cli("submit", "--db", self.db, "--key", "cancel-me",
                             "--tenant", "demo-a", "--query", "outbox")
        cancelled = self.cli("cancel", "--db", self.db, "--tenant", "demo-a",
                             "--task-id", next_task["id"])
        self.assertEqual(cancelled["status"], "cancelled")
        self.assertIsNone(self.cli("work", "--db", self.db))

    def test_cli_conflict_and_tenant_isolation_are_json(self):
        first = self.cli("submit", "--db", self.db, "--key", "same",
                         "--tenant", "demo-a", "--query", "sqlite")
        conflict = self.cli("submit", "--db", self.db, "--key", "same",
                            "--tenant", "demo-a", "--query", "outbox", expected=1)
        self.assertEqual(conflict["error"]["code"], "idempotency_conflict")
        missing = self.cli("get", "--db", self.db, "--tenant", "demo-b",
                           "--task-id", first["id"], expected=1)
        self.assertEqual(missing["error"]["code"], "not_found")

    def test_cli_requires_explicit_database_for_every_command(self):
        for command in ("submit", "work", "get", "cancel"):
            with self.subTest(command=command):
                output = self.cli(command, expected=2)
                self.assertEqual(output["error"]["code"], "invalid_arguments")
        self.assertEqual(list(Path(self.directory.name).iterdir()), [])

    def test_cli_invalid_input_does_not_create_db_or_echo_input(self):
        marker = "NOT-A-REAL-CREDENTIAL-input-marker"
        output = self.cli("submit", "--db", self.db, "--key", marker,
                          "--tenant", "demo-a", "--query", " ", expected=1)
        self.assertEqual(output["error"]["code"], "invalid_input")
        self.assertNotIn(marker, json.dumps(output))
        output = self.cli("get", "--db", self.db, "--tenant", "demo-a",
                          "--task-id", marker, expected=2)
        self.assertEqual(output["error"]["code"], "invalid_arguments")
        self.assertNotIn(marker, json.dumps(output))
        self.assertFalse(self.db.exists())

    def test_cli_budget_failure_is_a_task_not_traceback(self):
        task = self.cli("submit", "--db", self.db, "--key", "budget",
                        "--tenant", "demo-a", "--query", "sqlite", "--max-steps", 1)
        failed = self.cli("work", "--db", self.db)
        self.assertEqual(failed["id"], task["id"])
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(failed["error"]["code"], "budget_exceeded")


if __name__ == "__main__":
    unittest.main()
