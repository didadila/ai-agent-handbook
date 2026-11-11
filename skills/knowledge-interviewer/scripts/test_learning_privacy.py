from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from check_learning_privacy import violations
from learning_state import initialize


class LearnerPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.gitignore').write_text('/.local/\n')

    def git(self, *arguments):
        subprocess.run(['git', *arguments], cwd=self.root, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_fresh_profile_is_empty_and_not_in_git(self):
        index = initialize(self.root, 'frontend')
        self.assertTrue(index.is_file())
        progress = self.root / '.local/learning/frontend/progress.md'
        self.assertNotIn('| fe.', progress.read_text())
        self.assertEqual(violations(self.root), [])

    def test_repeated_init_never_overwrites_personal_records(self):
        initialize(self.root, 'frontend')
        record = self.root / '.local/learning/frontend/mistakes.md'
        record.write_text('synthetic private answer; preserve exactly\n')
        initialize(self.root, 'frontend')
        self.assertEqual(record.read_text(), 'synthetic private answer; preserve exactly\n')

    def test_unignored_local_home_is_rejected(self):
        (self.root / '.gitignore').write_text('')
        with self.assertRaises(ValueError):
            initialize(self.root, 'frontend')
        self.assertFalse((self.root / '.local/learning').exists())

    def test_new_domain_adds_navigation_without_erasing_existing_index_notes(self):
        index = initialize(self.root, 'frontend')
        with index.open('a') as handle:
            handle.write('\nmy synthetic local note\n')
        initialize(self.root, 'serve')
        self.assertIn('my synthetic local note', index.read_text())
        self.assertIn('](serve/progress.md)', index.read_text())

    def test_forced_staging_private_data_is_blocked(self):
        initialize(self.root, 'frontend')
        self.git('add', '-f', '.local/learning/frontend/mistakes.md')
        self.assertTrue(violations(self.root, staged=True))

    def test_index_is_checked_even_if_worktree_is_cleaned_after_staging(self):
        path = self.root / 'note.md'
        path.write_text(f'{Path.home()}/private-record.md\n')
        self.git('add', 'note.md')
        path.write_text('public generic content\n')
        self.assertTrue(violations(self.root, staged=True))
        self.assertEqual(violations(self.root), [])

    def test_legacy_handbook_record_cannot_return_to_shared_surface(self):
        path = self.root / 'handbook/ai-agent/mistakes.md'
        path.parent.mkdir(parents=True)
        path.write_text('synthetic record\n')
        self.git('add', 'handbook')
        self.assertTrue(violations(self.root, staged=True))

    def test_synthetic_fixtures_and_blank_templates_remain_shareable(self):
        fixture = self.root / 'skills/knowledge-interviewer/evals/fixtures/sample/mistakes.md'
        fixture.parent.mkdir(parents=True)
        fixture.write_text('Synthetic evaluation fixture, not a real learner record.\n')
        template = self.root / 'skills/knowledge-interviewer/templates/mistakes.md'
        template.parent.mkdir(parents=True)
        template.write_text('# Blank template\n\n<!-- learning-private -->\n')
        self.git('add', 'skills')
        self.assertEqual(violations(self.root, staged=True), [])

    def test_relocated_private_marker_is_blocked(self):
        path = self.root / 'published.md'
        path.write_text('# Private profile\n\n<!-- learning-private -->\n')
        self.git('add', 'published.md')
        self.assertTrue(violations(self.root, staged=True))

    def test_real_record_cannot_be_published_by_renaming_it_as_a_template(self):
        path = self.root / 'skills/knowledge-interviewer/templates/progress.md'
        path.parent.mkdir(parents=True)
        path.write_text('| fe.js.value | synthetic learner | B | 2026-11-09 | 1 |\n')
        self.git('add', 'skills')
        self.assertTrue(violations(self.root, staged=True))

    def test_unknown_domain_cannot_escape_the_local_directory(self):
        with self.assertRaises(ValueError):
            initialize(self.root, '../../outside')

    def test_local_private_file_cannot_mask_a_broken_public_link(self):
        initialize(self.root, 'frontend')
        page = self.root / 'README.md'
        page.write_text('[my answers](.local/learning/frontend/mistakes.md)\n')
        self.git('add', 'README.md')
        self.assertTrue(violations(self.root, staged=True))

    def test_symlink_cannot_redirect_local_profile_writes(self):
        (self.root / '.local').symlink_to(self.root / 'elsewhere', target_is_directory=True)
        with self.assertRaises(ValueError):
            initialize(self.root, 'frontend')


if __name__ == '__main__':
    unittest.main()
