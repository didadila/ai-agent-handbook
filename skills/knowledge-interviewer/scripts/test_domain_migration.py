"""Legacy names keep learner records available without moving or rewriting them."""
import tempfile
import unittest
from pathlib import Path
from learning_state import state_domain


class DomainMigrationTest(unittest.TestCase):
    def test_existing_go_records_win(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            old = root / '.local/learning/serve'
            old.mkdir(parents=True)
            record = old / 'progress.md'
            record.write_text('synthetic legacy progress')
            self.assertEqual(state_domain(root, 'go-backend'), 'serve')
            self.assertEqual(record.read_text(), 'synthetic legacy progress')
            self.assertFalse((old.parent / 'go-backend').exists())

    def test_new_environment_uses_canonical_name(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(state_domain(Path(folder), 'go-backend'), 'go-backend')
            self.assertEqual(state_domain(Path(folder), 'agent'), 'ai-agent')

    def test_unknown_domain_rejected(self):
        with self.assertRaises(ValueError):
            state_domain(Path('.'), 'unknown')
