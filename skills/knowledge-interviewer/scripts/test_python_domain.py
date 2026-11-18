"""Python domain joins the public lookup and private-state contracts without migration."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from learning_content import ROOT, locate
from learning_state import DOMAINS, initialize, state_domain


class PythonDomainTest(unittest.TestCase):
    def test_catalog_and_private_domain_are_registered(self):
        domains = json.loads((ROOT / 'catalog.json').read_text())['domains']
        python = next(item for item in domains if item['id'] == 'python-backend')
        self.assertEqual(python['prefixes'], ['py.'])
        self.assertEqual(python['points'], 36)
        self.assertIn('python-backend', DOMAINS)
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(state_domain(Path(folder), 'python-backend'), 'python-backend')

    def test_standalone_initializes_only_empty_python_records(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'synthetic-state'
            index = initialize(root, 'python-backend', standalone=True)
            self.assertIn('python-backend/progress.md', index.read_text())
            progress = root / 'python-backend/progress.md'
            self.assertIn('# python-backend 学习进度', progress.read_text())
            self.assertNotIn('| py.', progress.read_text())
            self.assertFalse((root / 'ai-agent').exists())
            self.assertFalse((root / 'go-backend').exists())

    def test_initialization_preserves_existing_synthetic_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'synthetic-state'
            initialize(root, 'python-backend', standalone=True)
            progress = root / 'python-backend/progress.md'
            original = progress.read_text() + '\nsynthetic learner note: do not overwrite\n'
            progress.write_text(original)
            initialize(root, 'python-backend', standalone=True)
            self.assertEqual(progress.read_text(), original)

    def test_public_link_checks_keep_real_links_not_fenced_archive_source(self):
        spec = importlib.util.spec_from_file_location('public_contract_check', ROOT / 'scripts/check_system.py')
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        outside = '[real link](missing.md)'
        for fence in ('```', '````', '~~~'):
            with self.subTest(fence=fence):
                text = outside + '\n' + fence + 'text\n[archived source](handbook/example.md)\n' + fence + '\n' + outside
                self.assertEqual(checker.without_fenced_code(text), outside + '\n' + outside)
        self.assertEqual(checker.without_fenced_code('````text\n```\n[still code](missing.md)\n````'), '')
        self.assertEqual(checker.without_fenced_code(outside), outside)
        self.assertEqual(checker.without_fenced_code('```unclosed\n[still code](missing.md)'), '')

    def test_python_implementation_points_do_not_leak_into_agent_domain(self):
        found = locate(ROOT, 'python-backend', 'py.agent.tools')
        self.assertEqual(len(found['sections']), 1)
        self.assertEqual(found['sections'][0]['path'],
                         'handbook/python-backend/06-python-agent.md')
        for domain, point in [('ai-agent', 'py.agent.tools'),
                              ('python-backend', 'go.agent.runtime'),
                              ('python-backend', 'agent.ctx.compaction')]:
            with self.subTest(domain=domain, point=point), self.assertRaises(ValueError):
                locate(ROOT, domain, point)


if __name__ == '__main__':
    unittest.main()
