import tempfile
import unittest
from pathlib import Path
from check_skill_entry import inspect_entry, REQUIRED


class SkillEntryTest(unittest.TestCase):
    def test_symlink_must_resolve_to_expected_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            expected = root / 'current'
            old = root / 'old'
            for target in (expected, old):
                for name in REQUIRED:
                    path = target / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('same bytes')
            entry = root / 'entry'
            entry.symlink_to(old, target_is_directory=True)
            self.assertFalse(inspect_entry(entry, expected)['passed'])
            entry.unlink()
            entry.symlink_to(expected, target_is_directory=True)
            self.assertTrue(inspect_entry(entry, expected)['passed'])

    def test_missing_companion_is_not_a_complete_skill(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'SKILL.md').write_text('main file only')
            self.assertFalse(inspect_entry(root, root)['passed'])

    def test_missing_entry_reports_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertFalse(inspect_entry(root / 'missing', root)['passed'])
