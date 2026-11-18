"""Python 3.11+ / standard-library-only, single-machine teaching job service.

Run with an explicitly chosen local database (the parent directory must exist):
    python3 job_service.py submit --db /tmp/lab.sqlite --tenant demo-a \
        --key lesson-1 --query sqlite
    python3 job_service.py work --db /tmp/lab.sqlite
    python3 job_service.py get --db /tmp/lab.sqlite --tenant demo-a --task-id 1

Use only synthetic queries: request/result data is persisted locally. Tenant
filters illustrate scoping, NOT authentication or authorization. FakeAgent is a
bounded keyword-search stub over synthetic public notes, NOT an LLM or a claim
of real RAG quality. It has no network, shell, write tool, or personal memory.

Every operation opens/closes its own file-backed SQLite connection and uses
BEGIN IMMEDIATE (including schema creation), without executescript's implicit
commits. This deliberately simple local experiment is not a multi-node queue.
Lease fencing protects only this database's task result, not external effects.
Expired final attempts are reaped on the next claim/submit, not by a timer.
Outbox publication is at least once; publish then acknowledge can duplicate on
crash or concurrent delivery. It does NOT give external business exactly once.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
from pathlib import Path
import secrets
import sqlite3
import sys
import time
from typing import Any, Callable, Iterator


MAX_QUERY_CHARS = 1024
MAX_STEPS = 8
MAX_CHARS = 8192
MAX_RESULT_CHARS = 16384


class ValidationError(ValueError):
    """Invalid input; validate before opening a database connection."""


class IdempotencyConflict(Exception):
    """The tenant/key already names a different canonical request."""


class QueueFull(Exception):
    """The database-wide queued + running admission limit was reached."""


class LeaseLost(Exception):
    """A worker no longer holds the current, unexpired lease."""


class ToolRejected(Exception):
    """Only the read-only search_notes tool is allowed."""


class BudgetExceeded(Exception):
    """The per-agent step or cumulative character budget was exhausted."""


ERROR_MESSAGES = {
    "attempts_exhausted": "The final worker lease expired.",
    "budget_exceeded": "The teaching agent exhausted its budget.",
    "tool_rejected": "The requested tool was rejected.",
    "invalid_input": "The teaching agent received invalid input.",
    "agent_execution_failed": "The teaching agent failed; details are suppressed.",
}


def _text(value: Any, name: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValidationError(f"{name} must be nonblank text of at most {limit} characters")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise ValidationError(f"{name} must be valid UTF-8 text") from None
    if "\x00" in value:
        raise ValidationError(f"{name} must not contain NUL")
    return value


def _integer(value: Any, name: str, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValidationError(f"{name} must be an integer in [{minimum}, {maximum}]")
    return value


def _duration(value: Any) -> float:
    if (type(value) not in (int, float) or not math.isfinite(value)
            or not 0 < value <= 86400):
        raise ValidationError("lease_seconds must be finite and in (0, 86400]")
    return float(value)


def _json(value: Any) -> str:
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False)
        encoded.encode("utf-8")
        return encoded
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError):
        raise ValidationError("payload must be finite, UTF-8 JSON") from None


def _result_json(result: Any) -> str:
    if not isinstance(result, dict):
        raise ValidationError("result must be a JSON object")
    encoded = _json(result)
    if len(encoded) > MAX_RESULT_CHARS:
        raise ValidationError("result exceeds the character limit")
    return encoded


def _request(query: Any, tool: Any, max_steps: Any, max_chars: Any) -> dict:
    query = _text(query, "query", MAX_QUERY_CHARS)
    if tool != "search_notes" or not isinstance(tool, str):
        raise ToolRejected("only search_notes is allowed")
    return {
        "query": query,
        "tool": tool,
        "max_steps": _integer(max_steps, "max_steps", 1, MAX_STEPS),
        "max_chars": _integer(max_chars, "max_chars", 1, MAX_CHARS),
    }


SCHEMA = (
    """CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant TEXT NOT NULL,
        idempotency_key TEXT NOT NULL,
        request_json TEXT NOT NULL,
        request_fingerprint TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN
            ('queued', 'running', 'succeeded', 'failed', 'cancelled')),
        attempt INTEGER NOT NULL DEFAULT 0,
        max_attempts INTEGER NOT NULL CHECK(max_attempts BETWEEN 1 AND 100),
        lease_owner TEXT,
        lease_token TEXT,
        lease_expires_at REAL,
        result_json TEXT,
        error_json TEXT,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL,
        UNIQUE(tenant, idempotency_key),
        CHECK(attempt >= 0 AND attempt <= max_attempts),
        CHECK((status = 'running' AND lease_owner IS NOT NULL
            AND lease_token IS NOT NULL AND lease_expires_at IS NOT NULL)
          OR (status != 'running' AND lease_owner IS NULL
            AND lease_token IS NULL AND lease_expires_at IS NULL))
    )""",
    """CREATE INDEX IF NOT EXISTS tasks_pending
        ON tasks(status, lease_expires_at, id)""",
    """CREATE TABLE IF NOT EXISTS outbox (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL UNIQUE REFERENCES tasks(id),
        tenant TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at REAL NOT NULL,
        sent_at REAL
    )""",
    """CREATE INDEX IF NOT EXISTS outbox_pending ON outbox(sent_at, id)""",
)


class JobStore:
    """Local file-backed queue. Constructor validates but does not create a DB.

    Configuration is admission/worker policy, not part of request identity;
    max_attempts is snapshotted into each new task. Keep admission configuration
    consistent across local submitters. Pending counts queued AND running tasks
    across tenants; terminal history/outbox retention is intentionally unbounded.
    Task IDs are monotonic SQLite integers, lease tokens are opaque random fences.
    """

    def __init__(self, db: str | Path, *, max_pending: int = 100,
                 max_attempts: int = 3, lease_seconds: float = 30,
                 clock: Callable[[], float] = time.time):
        if not isinstance(db, (str, Path)) or not str(db).strip():
            raise ValidationError("an explicit file database path is required")
        if str(db) == ":memory:" or str(db).startswith("file:") or "\x00" in str(db):
            raise ValidationError("use a file path, not :memory: or a SQLite URI")
        self.db = Path(db).expanduser().resolve()
        if not self.db.parent.is_dir() or self.db.is_dir():
            raise ValidationError("database parent must exist; database must be a file")
        self.max_pending = _integer(max_pending, "max_pending", 1, 100000)
        self.max_attempts = _integer(max_attempts, "max_attempts", 1, 100)
        self.lease_seconds = _duration(lease_seconds)
        if not callable(clock):
            raise ValidationError("clock must be callable")
        self.clock = clock

    def _now(self) -> float:
        value = self.clock()
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValidationError("clock must return a finite nonnegative timestamp")
        return float(value)

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(str(self.db), timeout=5, isolation_level=None)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("BEGIN IMMEDIATE")
            for statement in SCHEMA:
                connection.execute(statement)
            yield connection
            connection.commit()
        except BaseException:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _task(row: sqlite3.Row, *, with_token: bool = False) -> dict:
        task = dict(row)
        task["request"] = json.loads(task.pop("request_json"))
        task["result"] = json.loads(task.pop("result_json") or "null")
        task["error"] = json.loads(task.pop("error_json") or "null")
        if not with_token:
            task.pop("lease_token")
        return task

    @staticmethod
    def _expire_exhausted(connection: sqlite3.Connection, now: float) -> None:
        connection.execute(
            """UPDATE tasks SET status = 'failed', error_json = ?, updated_at = ?,
                lease_owner = NULL, lease_token = NULL, lease_expires_at = NULL
                WHERE status = 'running' AND lease_expires_at <= ?
                    AND attempt >= max_attempts""",
            (_json({"code": "attempts_exhausted",
                    "message": ERROR_MESSAGES["attempts_exhausted"]}), now, now),
        )

    def submit(self, tenant: str, key: str, query: str, *,
               tool: str = "search_notes", max_steps: int = 2,
               max_chars: int = 2048) -> dict:
        tenant = _text(tenant, "tenant", 128)
        key = _text(key, "key", 128)
        request_json = _json(_request(query, tool, max_steps, max_chars))
        fingerprint = hashlib.sha256(request_json.encode("utf-8")).hexdigest()
        with self._transaction() as connection:
            existing = connection.execute(
                "SELECT * FROM tasks WHERE tenant = ? AND idempotency_key = ?",
                (tenant, key),
            ).fetchone()
            # Deduplication/conflict comes BEFORE capacity: even a finished task
            # can be replayed while unrelated tasks fill the pending queue.
            if existing is not None:
                if existing["request_fingerprint"] != fingerprint:
                    raise IdempotencyConflict("key already names a different request")
                return self._task(existing)
            now = self._now()
            self._expire_exhausted(connection, now)
            pending = connection.execute(
                "SELECT COUNT(*) FROM tasks WHERE status IN ('queued', 'running')"
            ).fetchone()[0]
            if pending >= self.max_pending:
                raise QueueFull("pending queue is full")
            cursor = connection.execute(
                """INSERT INTO tasks
                    (tenant, idempotency_key, request_json, request_fingerprint,
                     status, max_attempts, created_at, updated_at)
                    VALUES (?, ?, ?, ?, 'queued', ?, ?, ?)""",
                (tenant, key, request_json, fingerprint, self.max_attempts, now, now),
            )
            task_id = cursor.lastrowid
            connection.execute(
                """INSERT INTO outbox(task_id, tenant, payload_json, created_at)
                    VALUES (?, ?, ?, ?)""",
                (task_id, tenant, _json({"event": "task.submitted",
                                        "task_id": task_id, "tenant": tenant}), now),
            )
            return self._task(connection.execute(
                "SELECT * FROM tasks WHERE id = ? AND tenant = ?", (task_id, tenant)
            ).fetchone())

    def get(self, tenant: str, task_id: int) -> dict | None:
        tenant = _text(tenant, "tenant", 128)
        task_id = _integer(task_id, "task_id", 1, 2**63 - 1)
        with self._transaction() as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = ? AND tenant = ?", (task_id, tenant)
            ).fetchone()
            return self._task(row) if row is not None else None

    def claim(self, owner: str, *, tenant: str | None = None) -> dict | None:
        """Claim oldest eligible task; optional tenant scope for a local worker.

        BEGIN IMMEDIATE serializes selection + conditional update. A takeover
        increments attempt and rotates token; equality at expiration is expired.
        No heartbeats: slow work must finish before its fixed lease or lose it.
        """
        owner = _text(owner, "owner", 128)
        if tenant is not None:
            tenant = _text(tenant, "tenant", 128)
        with self._transaction() as connection:
            now = self._now()  # Sample AFTER acquiring the write lock.
            self._expire_exhausted(connection, now)
            row = connection.execute(
                """SELECT * FROM tasks WHERE (? IS NULL OR tenant = ?)
                    AND attempt < max_attempts
                    AND (status = 'queued'
                        OR (status = 'running' AND lease_expires_at <= ?))
                    ORDER BY id LIMIT 1""", (tenant, tenant, now),
            ).fetchone()
            if row is None:
                return None
            token = secrets.token_hex(16)
            cursor = connection.execute(
                """UPDATE tasks SET status = 'running', attempt = attempt + 1,
                    lease_owner = ?, lease_token = ?, lease_expires_at = ?,
                    updated_at = ? WHERE id = ? AND attempt < max_attempts
                    AND (status = 'queued'
                        OR (status = 'running' AND lease_expires_at <= ?))""",
                (owner, token, now + self.lease_seconds, now, row["id"], now),
            )
            if cursor.rowcount != 1:
                raise LeaseLost("claim did not acquire a lease")
            return self._task(connection.execute(
                "SELECT * FROM tasks WHERE id = ?", (row["id"],)
            ).fetchone(), with_token=True)

    def finish(self, tenant: str, task_id: int, owner: str, token: str, *,
               result: dict | None = None, error: str | None = None) -> dict:
        """Complete only a matching running task with a strictly valid lease.

        Provide exactly one of a bounded JSON result or a fixed error code.
        Exception text, credentials, and tracebacks are never error summaries.
        """
        tenant = _text(tenant, "tenant", 128)
        task_id = _integer(task_id, "task_id", 1, 2**63 - 1)
        owner = _text(owner, "owner", 128)
        token = _text(token, "token", 128)
        if (result is None) == (error is None):
            raise ValidationError("provide exactly one of result or error")
        result_json = error_json = None
        if error is not None:
            if not isinstance(error, str) or error not in ERROR_MESSAGES:
                raise ValidationError("error must be a known, sanitized error code")
            error_json = _json({"code": error, "message": ERROR_MESSAGES[error]})
            status = "failed"
        else:
            result_json = _result_json(result)
            status = "succeeded"
        with self._transaction() as connection:
            now = self._now()
            cursor = connection.execute(
                """UPDATE tasks SET status = ?, result_json = ?, error_json = ?,
                    lease_owner = NULL, lease_token = NULL, lease_expires_at = NULL,
                    updated_at = ? WHERE tenant = ? AND id = ? AND status = 'running'
                    AND lease_owner = ? AND lease_token = ? AND lease_expires_at > ?""",
                (status, result_json, error_json, now, tenant, task_id, owner, token, now),
            )
            if cursor.rowcount != 1:
                raise LeaseLost("task is missing, cancelled, completed, or lease is lost")
            return self._task(connection.execute(
                "SELECT * FROM tasks WHERE id = ? AND tenant = ?", (task_id, tenant)
            ).fetchone())

    def cancel(self, tenant: str, task_id: int) -> dict | None:
        """Idempotent cancellation of queued/running tasks; terminal states stay."""
        tenant = _text(tenant, "tenant", 128)
        task_id = _integer(task_id, "task_id", 1, 2**63 - 1)
        with self._transaction() as connection:
            connection.execute(
                """UPDATE tasks SET status = 'cancelled', updated_at = ?,
                    lease_owner = NULL, lease_token = NULL, lease_expires_at = NULL
                    WHERE tenant = ? AND id = ? AND status IN ('queued', 'running')""",
                (self._now(), tenant, task_id),
            )
            row = connection.execute(
                "SELECT * FROM tasks WHERE tenant = ? AND id = ?", (tenant, task_id)
            ).fetchone()
            return self._task(row) if row is not None else None

    def pending_events(self, *, limit: int = 100) -> list[dict]:
        """Trusted local dispatcher interface, NOT a tenant-facing read API."""
        limit = _integer(limit, "limit", 1, 1000)
        with self._transaction() as connection:
            rows = connection.execute(
                "SELECT * FROM outbox WHERE sent_at IS NULL ORDER BY id LIMIT ?",
                (limit,),
            ).fetchall()
            events = []
            for row in rows:
                event = dict(row)
                event["payload"] = json.loads(event.pop("payload_json"))
                events.append(event)
            return events

    def mark_sent(self, event_id: int) -> bool:
        """Acknowledge after delivery. False means unknown or already sent."""
        event_id = _integer(event_id, "event_id", 1, 2**63 - 1)
        with self._transaction() as connection:
            cursor = connection.execute(
                "UPDATE outbox SET sent_at = ? WHERE id = ? AND sent_at IS NULL",
                (self._now(), event_id),
            )
            return cursor.rowcount == 1

    def publish_outbox(self, publish: Callable[[dict], None], *, limit: int = 100) -> int:
        """Publish outside the DB transaction, then ack; failure leaves unsent.

        The callback MUST raise on failure, and consumers need event-id dedup if
        desired. Even dedup here cannot guarantee exactly-once external effects.
        """
        if not callable(publish):
            raise ValidationError("publish must be callable")
        count = 0
        for event in self.pending_events(limit=limit):
            publish(event)
            self.mark_sent(event["id"])
            count += 1
        return count


# Entire corpus is fabricated public teaching material; demo-b notes must not
# appear in demo-a searches. Unknown tenants have no notes, never a fallback.
PUBLIC_NOTES = (
    ("demo-a", "a-sqlite", "SQLite transactions",
     "SQLite BEGIN IMMEDIATE serializes local writers. Parameters bind SQL values.",
     ("sqlite", "transaction", "事务")),
    ("demo-a", "a-outbox", "Transactional outbox",
     "An outbox stores an event with its task in one transaction. Delivery may repeat.",
     ("outbox", "delivery", "发件箱")),
    ("demo-b", "b-lease", "Worker leases",
     "An expired lease can be taken over. A stale token cannot finish the local task.",
     ("lease", "token", "租约")),
    ("demo-b", "b-sqlite", "SQLite scope",
     "This synthetic demo-b note illustrates tenant-scoped SQLite retrieval.",
     ("sqlite", "tenant", "租户")),
)


class FakeAgent:
    """Read-only keyword stub, scoped at construction, with per-instance budgets.

    One step for search, one for answer. Characters count input query, returned
    evidence (source IDs, titles, bodies), and answer text; fixed JSON metadata is
    not charged. Counters accumulate even across direct tool calls. No history
    survives a task. Search arguments may contain ONLY query, never tenant.
    """

    def __init__(self, tenant: str, *, max_steps: int = 2, max_chars: int = 2048):
        self.tenant = _text(tenant, "tenant", 128)
        self.max_steps = _integer(max_steps, "max_steps", 1, MAX_STEPS)
        self.max_chars = _integer(max_chars, "max_chars", 1, MAX_CHARS)
        self.steps_used = 0
        self.chars_used = 0

    def _charge(self, *, steps: int = 0, chars: int = 0) -> None:
        if (self.steps_used + steps > self.max_steps
                or self.chars_used + chars > self.max_chars):
            raise BudgetExceeded("step or character budget exhausted")
        self.steps_used += steps
        self.chars_used += chars

    def call_tool(self, name: str, arguments: dict) -> list[dict]:
        if not isinstance(name, str) or name != "search_notes":
            raise ToolRejected("only search_notes is allowed")
        if not isinstance(arguments, dict) or set(arguments) != {"query"}:
            raise ValidationError("search_notes requires only a query argument")
        query = _text(arguments["query"], "query", MAX_QUERY_CHARS)
        self._charge(steps=1, chars=len(query))
        folded = query.casefold()
        hits = []
        for tenant, source_id, title, body, keywords in PUBLIC_NOTES:
            if tenant != self.tenant:
                continue
            if any(word in folded for word in keywords):
                self._charge(chars=len(source_id) + len(title) + len(body))
                hits.append({"source_id": source_id, "title": title, "text": body})
        return hits

    def run(self, query: str, *, tool: str = "search_notes") -> dict:
        evidence = self.call_tool(tool, {"query": query})
        answer = ("\n".join(note["text"] for note in evidence) if evidence
                  else "不知道：没有找到当前租户的公开合成文档证据。")
        self._charge(steps=1, chars=len(answer))
        return {
            "implementation": "read-only-keyword-stub-not-llm",
            "answer": answer,
            "source_ids": [note["source_id"] for note in evidence],
            "steps_used": self.steps_used,
            "chars_used": self.chars_used,
        }


def run_one(store: JobStore, owner: str = "local-worker", *,
            tenant: str | None = None,
            agent_factory: Callable[..., FakeAgent] = FakeAgent) -> dict | None:
    """Claim and run one short-lived stub. Execution errors are final failures.

    Lease loss is not hidden: finish raises LeaseLost if work became stale.
    The factory is an in-process test seam, not a dynamic/plugin CLI loader.
    """
    task = store.claim(owner, tenant=tenant)
    if task is None:
        return None
    result = None
    error = None
    try:
        request = task["request"]
        agent = agent_factory(task["tenant"], max_steps=request["max_steps"],
                              max_chars=request["max_chars"])
        result = agent.run(request["query"], tool=request["tool"])
        _result_json(result)  # Invalid stub output is also a sanitized failure.
    except Exception as exc:
        # Do not stringify exceptions: they may contain queries or credentials.
        if isinstance(exc, BudgetExceeded):
            error = "budget_exceeded"
        elif isinstance(exc, ToolRejected):
            error = "tool_rejected"
        elif isinstance(exc, ValidationError):
            error = "invalid_input"
        else:
            error = "agent_execution_failed"
    return store.finish(task["tenant"], task["id"], owner, task["lease_token"],
                        result=result if error is None else None, error=error)


class _JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse's message can echo user input; use a fixed safe summary.
        print(_json({"error": {"code": "invalid_arguments",
                               "message": "Invalid arguments; consult --help."}}))
        raise SystemExit(2)


def main(argv: list[str] | None = None) -> int:
    parser = _JSONArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("submit", "work", "get", "cancel"):
        command = commands.add_parser(name)
        command.add_argument("--db", required=True, help="explicit local SQLite file path")
        if name != "work":
            command.add_argument("--tenant", required=True)
        if name == "submit":
            command.add_argument("--key", required=True)
            command.add_argument("--query", required=True)
            command.add_argument("--max-pending", type=int, default=100)
            command.add_argument("--max-attempts", type=int, default=3)
            command.add_argument("--max-steps", type=int, default=2)
            command.add_argument("--max-chars", type=int, default=2048)
        elif name == "work":
            command.add_argument("--owner", default="local-worker")
            command.add_argument("--lease-seconds", type=float, default=30)
        else:
            command.add_argument("--task-id", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        store = JobStore(args.db, max_pending=getattr(args, "max_pending", 100),
                         max_attempts=getattr(args, "max_attempts", 3),
                         lease_seconds=getattr(args, "lease_seconds", 30))
        if args.command == "submit":
            output = store.submit(args.tenant, args.key, args.query,
                                  max_steps=args.max_steps, max_chars=args.max_chars)
        elif args.command == "work":
            output = run_one(store, args.owner)
        elif args.command == "get":
            output = store.get(args.tenant, args.task_id)
        else:
            output = store.cancel(args.tenant, args.task_id)
        if output is None and args.command != "work":
            print(_json({"error": {"code": "not_found", "message": "Task not found."}}))
            return 1
        print(_json(output))
        return 0
    except (ValidationError, ToolRejected, IdempotencyConflict, QueueFull,
            LeaseLost, sqlite3.Error, OSError) as exc:
        errors = {
            ValidationError: ("invalid_input", "Invalid input or local database path."),
            ToolRejected: ("tool_rejected", "Only search_notes is allowed."),
            IdempotencyConflict: ("idempotency_conflict", "Key names a different request."),
            QueueFull: ("queue_full", "Pending queue is full."),
            LeaseLost: ("lease_lost", "Worker no longer holds a valid lease."),
        }
        code, message = errors.get(type(exc), ("storage_error", "Local storage operation failed."))
        print(_json({"error": {"code": code, "message": message}}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
