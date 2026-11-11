#!/usr/bin/env python3
"""Initialize or locate ignored local learner files without overwriting records."""
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[1]
DOMAINS = tuple(sorted(path.parent.name for path in (SKILL / 'references/domains').glob('*/map.md')))
ALIASES = {'serve': 'go-backend', 'agent': 'ai-agent'}


def state_domain(root: Path, domain: str, *, standalone: bool = False) -> str:
    """Resolve public names without moving existing private learner records."""
    canonical = ALIASES.get(domain, domain)
    if canonical not in DOMAINS:
        raise ValueError('Unknown domain: ' + domain)
    if canonical == 'go-backend' and (local_home(root, standalone=standalone) / 'serve').exists():
        return 'serve'
    # Explicit legacy input remains compatible for callers of older versions.
    return 'serve' if domain == 'serve' else canonical


def local_home(root: Path, *, standalone: bool = False) -> Path:
    return root.resolve() if standalone else root.resolve() / '.local/learning'


def git_root(path: Path) -> Path | None:
    """Inspect an existing ancestor without creating the requested directory."""
    ancestor = path
    while not ancestor.exists():
        ancestor = ancestor.parent
    if not ancestor.is_dir():
        raise ValueError('Learning root must be a directory')
    try:
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=ancestor,
                                capture_output=True, text=True,
                                env={**os.environ, 'LC_ALL': 'C', 'LANGUAGE': 'C'})
    except OSError as error:
        raise ValueError('Cannot inspect Git safety boundary; check that Git is installed') from error
    if result.returncode == 0:
        return Path(result.stdout.strip()).resolve()
    # A non-repository is expected; permissions/corruption must not become an opt-out.
    if 'not a git repository' in result.stderr.lower():
        return None
    raise ValueError('Cannot verify Git safety boundary; check repository access')


def check_private_path(path: Path, *, directory: bool) -> None:
    """Reject unsafe existing paths; never silently chmod learner storage."""
    if path.is_symlink():
        raise ValueError('Private state path must not be a symlink')
    if not path.exists():
        return
    if (directory and not path.is_dir()) or (not directory and not path.is_file()):
        raise ValueError('Private state path has an unexpected file type')
    expected = 0o700 if directory else 0o600
    if os.name == 'posix' and path.stat().st_mode & 0o777 != expected:
        raise ValueError(f'private state path must have mode {expected:04o}. '
                         'No existing permissions changed; do not auto-chmod or bypass this check. '
                         'Stop saving until the owner explicitly authorizes remediation.')


def initialize(root: Path, domain: str | None = None, *, standalone: bool = False) -> Path:
    if root.is_symlink():
        raise ValueError('Learning root must not be a symlink')
    root = root.resolve()
    selected = tuple(state_domain(root, item, standalone=standalone) for item in ((domain,) if domain else DOMAINS))
    home = local_home(root, standalone=standalone)
    if home.is_symlink() or (not standalone and (root / '.local').is_symlink()):
        raise ValueError('Local learner directory must not be a symlink')
    repository = git_root(root)
    if standalone:
        if repository is not None:
            raise ValueError('Standalone learning directory must be outside every Git worktree')
    else:
        if repository is None:
            raise ValueError('Not a Git worktree. Use a repository root, or explicitly choose '
                             '--standalone --root <private-directory-outside-Git>. No files written.')
        if repository != root:
            raise ValueError('--root must be the Git worktree root, not a subdirectory')
        probe = '.local/learning/probe.md'
        ignored = subprocess.run(['git', 'check-ignore', '-q', '--no-index', probe], cwd=root,
                                 capture_output=True)
        tracked = subprocess.run(['git', 'ls-files', '-z', '--', '.local'], cwd=root,
                                 capture_output=True)
        if tracked.returncode != 0 or ignored.returncode not in (0, 1):
            raise ValueError('Cannot verify ignore/tracking safety; no files written')
        if ignored.returncode != 0 or tracked.stdout:
            raise ValueError('Refusing initialization: .local must be ignored and untracked')
    # Validate every selected target before creating any files or directories.
    check_private_path(home, directory=True)
    check_private_path(home / 'index.md', directory=False)
    for item in selected:
        folder = home / item
        check_private_path(folder, directory=True)
        check_private_path(folder / 'sessions', directory=True)
        for filename in ('progress.md', 'mistakes.md'):
            check_private_path(folder / filename, directory=False)
    home.mkdir(mode=0o700, parents=True, exist_ok=True)
    for item in selected:
        folder = home / item
        if folder.is_symlink():
            raise ValueError('Learner domain directory must not be a symlink')
        folder.mkdir(mode=0o700, exist_ok=True)
        (folder / 'sessions').mkdir(mode=0o700, exist_ok=True)
        for filename in ('progress.md', 'mistakes.md'):
            target = folder / filename
            if target.exists() or target.is_symlink():
                continue
            content = (SKILL / 'templates' / filename).read_text().replace('{domain}', item)
            with target.open('x', encoding='utf-8') as handle:
                handle.write(content)
            target.chmod(0o600)
    index = home / 'index.md'
    if index.is_symlink():
        raise ValueError('Local index must not be a symlink')
    if not index.exists():
        lines = ['# 本地学习记录', '', '<!-- learning-private -->', '',
                 '个人错题、成绩、复习安排只存本机；本目录被Git忽略，不自动同步云端。', '']
        for item in selected:
            if (home / item).is_dir():
                lines.append(f'- {item}：[进度]({item}/progress.md) · [错题]({item}/mistakes.md)')
        with index.open('x', encoding='utf-8') as handle:
            handle.write('\n'.join(lines) + '\n')
        index.chmod(0o600)
    else:
        content = index.read_text()
        new_links = [f'- {item}：[进度]({item}/progress.md) · [错题]({item}/mistakes.md)'
                     for item in selected if f']({item}/progress.md)' not in content]
        if new_links:
            # Append navigation only; preserve any learner notes and existing records.
            with index.open('a', encoding='utf-8') as handle:
                handle.write('\n' + '\n'.join(new_links) + '\n')
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('init', 'paths'))
    parser.add_argument('--root', type=Path)
    parser.add_argument('--standalone', action='store_true',
                        help='Use a private state directory outside Git; --root is the state directory itself')
    parser.add_argument('--domain', choices=DOMAINS + tuple(ALIASES))
    args = parser.parse_args()
    root = args.root or (Path.home() / '.local/share/knowledge-interviewer' if args.standalone else ROOT)
    try:
        if args.command == 'init':
            index = initialize(root, args.domain, standalone=args.standalone)
        else:
            index = local_home(root, standalone=args.standalone) / 'index.md'
    except (ValueError, OSError) as error:
        parser.exit(2, f'learning_state: {error}\n')
    # Only locations are emitted; private record contents are never printed.
    print(index)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
