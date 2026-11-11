"""Corruptions of evidence and original-run hashes must be rejected."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from check_fix_regressions import check_suite


class FixEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'suite'
        self.folder.mkdir()
        self.write('cases.json', {'status': 'run_reviewed', 'cases': [{'id': 'one'}]})
        self.write('rubric.json', {'cases': {'one': ['criterion']}})
        self.write('responses.json', {'results': [dict(case_id='one', selected_domain='demo',
                   selected_point_id='demo.point', learner_response='synthetic', evidence_paths=[],
                   commands=[], state_action='none', external_sync='none', actions_asked=1, written_files=[])]})
        self.write('grades.json', {'cases': {'one': {'criteria': [{'criterion': 'criterion', 'passed': True}],
                   'case_pass': True, 'reason': 'synthetic'}}, 'summary': {'cases_total': 1,
                   'cases_passed': 1, 'criteria_total': 1, 'criteria_passed': 1}})

    def write(self, name, value):
        (self.folder / name).write_text(json.dumps(value))

    def test_valid_synthetic_envelope(self):
        self.assertEqual(check_suite(self.folder, self.root)[0], [])

    def test_original_run_mutation_detected(self):
        old = self.root / 'original.json'
        old.write_text('old failure')
        self.write('baseline-sha256.json', {'original.json': hashlib.sha256(old.read_bytes()).hexdigest()})
        old.write_text('rewritten pass')
        self.assertTrue(any('Original evidence' in e for e in check_suite(self.folder, self.root)[0]))

    def test_duplicate_response_and_missing_body_detected(self):
        self.write('responses.json', {'results': [{'case_id': 'one'}, {'case_id': 'one'}]})
        errors, _ = check_suite(self.folder, self.root)
        self.assertTrue(any('duplicate' in e for e in errors))
        self.assertTrue(any('empty learner response' in e for e in errors))

    def test_changed_rubric_is_not_used_to_rescore_old_checks(self):
        self.write('rubric.json', {'cases': {'one': ['new criterion']}})
        self.assertTrue(any('criterion text' in e for e in check_suite(self.folder, self.root)[0]))

    def test_v3_bad_structure_cannot_be_reviewed_as_pass(self):
        self.write('cases.json', {'schema_version': 3, 'status': 'run_reviewed',
                                  'cases': [{'id': 'one', 'format_mode': 'teach'}]})
        self.assertTrue(any('structural judgement' in e for e in check_suite(self.folder, self.root)[0]))

    def test_v3_failed_structure_remains_valid_failure_evidence(self):
        self.write('cases.json', {'schema_version': 3, 'status': 'run_reviewed',
                                  'cases': [{'id': 'one', 'format_mode': 'teach'}]})
        self.write('grades.json', {'cases': {'one': {'criteria': [{'criterion': 'criterion', 'passed': False}],
                   'case_pass': False, 'reason': 'bad structure retained'}},
                   'summary': {'cases_total': 1, 'cases_passed': 0, 'criteria_total': 1, 'criteria_passed': 0}})
        self.assertEqual(check_suite(self.folder, self.root)[0], [])
