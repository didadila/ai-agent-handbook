"""Archived behavior runs keep rubric order, all-critical passes, and no personal paths."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import check_behavior_eval_runs as checker


def build_fixture(root: Path, *, criteria=('选对领域与稳定ID', '只有一个作答动作'), case_pass=True,
                  passed=(True, True), status='run_reviewed_2026-01-01', evidence_extra='') -> Path:
    evals = root / 'skills/knowledge-interviewer/evals/demo'
    run = evals / 'runs/2026-01-01'
    run.mkdir(parents=True)
    (root / 'catalog.json').write_text(json.dumps({'domains': [{'id': 'demo'}]}))
    (evals / 'cases.json').write_text(json.dumps({
        'schema_version': 1, 'domain': 'demo', 'status': status,
        'run': {'date': '2026-01-01', 'cases_total': 1, 'cases_passed': int(all(passed) and case_pass),
                'criteria_total': len(criteria), 'criteria_passed': sum(passed)},
        'cases': [{'id': 'demo-a', 'point_id': 'demo.a', 'type': 'route'}]}))
    (evals / 'rubric.json').write_text(json.dumps({'cases': {'demo-a': list(criteria)}}))
    (run / 'grades.json').write_text(json.dumps({
        'method': 'model review' + evidence_extra,
        'cases': {'demo-a': {
            'criteria': [{'criterion': name, 'passed': flag}
                         for name, flag in zip(criteria, passed)],
            'case_pass': case_pass, 'reason': 'r', 'observations': []}},
        'summary': {'cases_total': 1, 'cases_passed': 1 if case_pass and all(passed) else 0,
                    'criteria_total': len(criteria), 'criteria_passed': sum(passed)}}))
    (run / 'evidence.md').write_text(
        '# evidence\n\n## demo-a\n\n- selected_domain: demo\n- selected_point_id: demo.a\n'
        '- actions_asked: 1\n- state_action: none\n- external_sync: none\n\n'
        '一轮真实输出。' + evidence_extra + '\n')
    (run / 'README.md').write_text('# demo\n\n## 协议\n\n冷启动。\n\n## 结果\n\n1/1。\n\n## 限制\n\n单次采样。\n')
    return evals


class BehaviorRunArchiveTest(unittest.TestCase):
    def check(self, **kwargs):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            build_fixture(root, **kwargs)
            errors: list[str] = []
            with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'SKILL', root / 'skills/knowledge-interviewer'):
                result = checker.check_domain('demo', errors)
            return result, errors

    def test_clean_archive_reports_counts_without_errors(self):
        result, errors = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(result, '2026-01-01: 1/1 cases, 2/2 criteria (1 archived run(s))')

    def test_cases_json_summary_must_match_its_archive(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evals = build_fixture(root)
            path = evals / 'cases.json'
            cases = json.loads(path.read_text())
            cases['run']['cases_passed'] = 1
            cases['run']['criteria_passed'] = 2
            path.write_text(json.dumps(cases))
            grades = json.loads((evals / 'runs/2026-01-01/grades.json').read_text())
            for item in grades['cases']['demo-a']['criteria']:
                item['passed'] = False
            grades['cases']['demo-a']['case_pass'] = False
            grades['summary']['cases_passed'] = 0
            grades['summary']['criteria_passed'] = 0
            (evals / 'runs/2026-01-01/grades.json').write_text(json.dumps(grades))
            errors: list[str] = []
            with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'SKILL', root / 'skills/knowledge-interviewer'):
                checker.check_domain('demo', errors)
            self.assertTrue(any('cases.json run disagrees with grades' in item for item in errors), errors)

    def test_older_run_is_still_validated_when_a_new_run_is_added(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evals = build_fixture(root)
            second = evals / 'runs/2026-02-02'
            second.mkdir(parents=True)
            for name in ('grades.json', 'evidence.md', 'README.md'):
                (second / name).write_text((evals / 'runs/2026-01-01' / name).read_text())
            # Break only the older archive: the newest run must not mask it.
            grades = json.loads((evals / 'runs/2026-01-01/grades.json').read_text())
            grades['summary']['criteria_passed'] = 99
            (evals / 'runs/2026-01-01/grades.json').write_text(json.dumps(grades))
            errors: list[str] = []
            with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'SKILL', root / 'skills/knowledge-interviewer'):
                result = checker.check_domain('demo', errors)
            self.assertTrue(any('2026-01-01: summary counts do not match' in item for item in errors), errors)
            self.assertIn('2 archived run(s)', result)

    def test_criteria_order_change_is_caught(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evals = build_fixture(root)
            grades = json.loads((evals / 'runs/2026-01-01/grades.json').read_text())
            grades['cases']['demo-a']['criteria'].reverse()
            (evals / 'runs/2026-01-01/grades.json').write_text(json.dumps(grades))
            errors: list[str] = []
            with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'SKILL', root / 'skills/knowledge-interviewer'):
                checker.check_domain('demo', errors)
            self.assertTrue(any('criteria text/order' in item for item in errors), errors)

    def test_dropped_criterion_is_caught(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evals = build_fixture(root)
            path = evals / 'runs/2026-01-01/grades.json'
            grades = json.loads(path.read_text())
            grades['cases']['demo-a']['criteria'].pop()
            path.write_text(json.dumps(grades))
            errors: list[str] = []
            with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'SKILL', root / 'skills/knowledge-interviewer'):
                checker.check_domain('demo', errors)
            self.assertTrue(any('criteria text/order' in item for item in errors), errors)

    def test_partial_credit_cannot_be_reported_as_case_pass(self):
        _, errors = self.check(passed=(True, False))
        self.assertTrue(any('all-criteria rule' in item for item in errors), errors)

    def test_personal_home_path_in_evidence_is_rejected(self):
        _, errors = self.check(evidence_extra=' ' + str(Path.home()) + '/notes.md')
        self.assertTrue(any('personal home path' in item for item in errors), errors)

    def test_not_run_status_conflicts_with_archived_results(self):
        _, errors = self.check(status='not_run')
        self.assertTrue(any('still marked not_run' in item for item in errors), errors)

    def test_missing_run_directory_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            evals = build_fixture(root)
            shutil.rmtree(evals / 'runs')
            errors: list[str] = []
            with mock.patch.object(checker, 'ROOT', root), mock.patch.object(checker, 'SKILL', root / 'skills/knowledge-interviewer'):
                checker.check_domain('demo', errors)
            self.assertTrue(any('no archived behavior run' in item for item in errors), errors)

    def test_shipped_archive_passes_structural_checks(self):
        self.assertEqual(checker.main(), False, 'archived four-domain runs are structurally inconsistent')


if __name__ == '__main__':
    unittest.main()
