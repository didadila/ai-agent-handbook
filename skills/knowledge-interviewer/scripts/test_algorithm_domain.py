"""Public algorithm-domain contract, prerequisite DAG and synthetic local state."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from learning_content import ROOT, locate
from learning_state import DOMAINS, initialize


class AlgorithmDomainTest(unittest.TestCase):
    def test_all_points_have_one_real_section(self):
        domain = 'algorithms-python'
        self.assertIn(domain, DOMAINS)
        ref = ROOT / 'skills/knowledge-interviewer/references/domains' / domain
        ids = re.findall(r'^\| `([^`]+)`', (ref / 'map.md').read_text(), re.M)
        self.assertEqual(len(ids), 26)
        for point in ids:
            with self.subTest(point=point):
                found = locate(ROOT, domain, point)
                self.assertEqual(len(found['sections']), 1)
                section = found['sections'][0]
                line = (ROOT / section['path']).read_text().splitlines()[section['start_line']-1]
                self.assertEqual(line, '## ' + section['heading'])
        with self.assertRaises(ValueError):
            locate(ROOT, 'python-backend', 'alg.window')
        with self.assertRaises(ValueError):
            locate(ROOT, domain, 'py.async.eventloop')

    def test_prerequisites_are_declared_and_acyclic(self):
        text = (ROOT / 'skills/knowledge-interviewer/references/domains/algorithms-python/map.md').read_text()
        rows = re.findall(r'^\| `(alg\.[^`]+)`[^\n]*?前置：([^；]+)；', text, re.M)
        dependencies = {point: re.findall(r'alg\.[\w-]+', values) for point, values in rows}
        self.assertEqual(len(dependencies), 26)
        done, visiting = set(), set()
        def visit(point):
            self.assertIn(point, dependencies)
            self.assertNotIn(point, visiting)
            if point in done:
                return
            visiting.add(point)
            for previous in dependencies[point]:
                visit(previous)
            visiting.remove(point)
            done.add(point)
        for point in dependencies:
            visit(point)

    def test_synthetic_profile_is_empty_and_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'synthetic'
            initialize(root, 'algorithms-python', standalone=True)
            progress = root / 'algorithms-python/progress.md'
            self.assertNotIn('| alg.', progress.read_text())
            original = progress.read_text() + '\nsynthetic note\n'
            progress.write_text(original)
            initialize(root, 'algorithms-python', standalone=True)
            self.assertEqual(progress.read_text(), original)
            self.assertFalse((root / 'python-backend').exists())

    def test_behavior_cases_are_planned_not_fabricated_runs(self):
        base = ROOT / 'skills/knowledge-interviewer/evals/algorithms-python'
        cases = json.loads((base / 'cases.json').read_text())
        self.assertEqual(cases['status'], 'not_run')
        self.assertEqual({c['type'] for c in cases['cases']}, {'route','wrong','boundary','privacy','skip','format'})
        self.assertFalse((base / 'runs').exists())


if __name__ == '__main__':
    unittest.main()
