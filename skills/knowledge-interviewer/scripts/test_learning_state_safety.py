"""Initialization errors fail closed; standalone storage requires an explicit mode."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import learning_state as state


class InitializationSafetyTest(unittest.TestCase):
    def test_non_git_root_has_readable_error_and_no_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaisesRegex(ValueError, 'Not a Git worktree'):
                state.initialize(root, 'frontend')
            self.assertEqual(list(root.iterdir()), [])

    def test_cli_reports_non_git_without_traceback(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, state.__file__, 'init', '--root', folder],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('--standalone', result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_explicit_standalone_uses_private_root_without_nested_local(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'private-state'
            index = state.initialize(root, 'frontend', standalone=True)
            self.assertEqual(index, root.resolve() / 'index.md')
            self.assertTrue((root / 'frontend/progress.md').is_file())
            self.assertFalse((root / '.local').exists())
            if os.name == 'posix':
                self.assertEqual(root.stat().st_mode & 0o777, 0o700)
                self.assertEqual(index.stat().st_mode & 0o777, 0o600)

    def test_standalone_does_not_overwrite_existing_records(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'state'
            state.initialize(root, 'frontend', standalone=True)
            record = root / 'frontend/mistakes.md'
            record.write_text('synthetic answer, retain exactly')
            state.initialize(root, 'frontend', standalone=True)
            self.assertEqual(record.read_text(), 'synthetic answer, retain exactly')

    def test_standalone_cannot_bypass_git_with_nonexistent_child(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            child = root / 'missing/state'
            with self.assertRaisesRegex(ValueError, 'outside every Git worktree'):
                state.initialize(child, 'frontend', standalone=True)
            self.assertFalse(child.parent.exists())

    def test_repository_subdirectory_is_not_a_new_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'child').mkdir()
            with self.assertRaisesRegex(ValueError, 'worktree root'):
                state.initialize(root / 'child', 'frontend')
            self.assertFalse((root / 'child/.local').exists())

    def test_missing_git_does_not_enable_standalone_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(state.subprocess, 'run', side_effect=FileNotFoundError):
                with self.assertRaisesRegex(ValueError, 'Git is installed'):
                    state.initialize(Path(folder), 'frontend', standalone=True)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_git_access_failure_is_not_treated_as_non_git(self):
        with tempfile.TemporaryDirectory() as folder:
            failure = subprocess.CompletedProcess([], 128, '', 'fatal: permission denied')
            with mock.patch.object(state.subprocess, 'run', return_value=failure):
                with self.assertRaisesRegex(ValueError, 'repository access'):
                    state.initialize(Path(folder), 'frontend', standalone=True)
            self.assertEqual(list(Path(folder).iterdir()), [])

    @unittest.skipUnless(os.name == 'posix', 'POSIX directory permissions')
    def test_standalone_rejects_shared_directory_without_chmod_or_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'shared'
            root.mkdir(mode=0o755)
            root.chmod(0o755)
            with self.assertRaisesRegex(ValueError, 'private'):
                state.initialize(root, 'frontend', standalone=True)
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual(root.stat().st_mode & 0o777, 0o755)

    def test_standalone_cli_init_and_paths_agree(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'private-state'
            common = ['--standalone', '--root', str(root), '--domain', 'frontend']
            init = subprocess.run([sys.executable, state.__file__, 'init', *common], capture_output=True, text=True)
            paths = subprocess.run([sys.executable, state.__file__, 'paths', *common], capture_output=True, text=True)
            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertEqual(paths.returncode, 0, paths.stderr)
            self.assertEqual(init.stdout, paths.stdout)
            self.assertTrue(Path(init.stdout.strip()).is_file())

    @unittest.skipUnless(os.name == 'posix', 'POSIX directory permissions')
    def test_existing_domain_permissions_rejected_before_any_new_state(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'state'
            root.mkdir(mode=0o700)
            domain = root / 'frontend'
            domain.mkdir(mode=0o755)
            domain.chmod(0o755)
            with self.assertRaisesRegex(ValueError, 'do not auto-chmod'):
                state.initialize(root, 'frontend', standalone=True)
            self.assertEqual(domain.stat().st_mode & 0o777, 0o755)
            self.assertFalse((root / 'index.md').exists())
            self.assertFalse((domain / 'progress.md').exists())

    @unittest.skipUnless(os.name == 'posix', 'POSIX directory permissions')
    def test_existing_sessions_and_record_permissions_are_not_silently_repaired(self):
        for target in ('sessions', 'progress.md'):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as folder:
                root = Path(folder) / 'state'
                state.initialize(root, 'frontend', standalone=True)
                path = root / 'frontend' / target
                path.chmod(0o755 if path.is_dir() else 0o644)
                before = {str(p): (p.stat().st_mode, p.stat().st_mtime_ns) for p in root.rglob('*')}
                with self.assertRaisesRegex(ValueError, 'No existing permissions changed'):
                    state.initialize(root, 'frontend', standalone=True)
                after = {str(p): (p.stat().st_mode, p.stat().st_mtime_ns) for p in root.rglob('*')}
                self.assertEqual(before, after)

    def test_new_sessions_directory_exists_and_is_private(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'state'
            state.initialize(root, 'frontend', standalone=True)
            self.assertTrue((root / 'frontend/sessions').is_dir())
            if os.name == 'posix':
                self.assertEqual((root / 'frontend/sessions').stat().st_mode & 0o777, 0o700)
