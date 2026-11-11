#!/usr/bin/env python3
"""Reject private learner files or personal home paths in the shared Git surface."""
from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def private_path(name: str) -> bool:
    parts = Path(name).parts
    return ('.local' in parts or 'pending-qmind' in parts or
            name in ('interviewer-feedback.md', 'output-style.md') or
            re.fullmatch(r'handbook/[^/]+/(progress|mistakes)\.md', name) is not None)


def violations(root: Path, staged: bool = False) -> list[str]:
    command = ['git', 'ls-files', '-z']
    if not staged:
        command.extend(['--cached', '--others', '--exclude-standard'])
    names = subprocess.check_output(command, cwd=root).decode().split('\0')
    shared_names = set(filter(None, names))
    errors = []
    for name in sorted(set(filter(None, names))):
        if private_path(name):
            errors.append(f'private learner path is in shared files: {name}')
            continue
        if staged:
            data = subprocess.check_output(['git', 'show', f':{name}'], cwd=root)
        else:
            target = root / name
            if not target.is_file() or target.is_symlink():
                continue
            data = target.read_bytes()
        if b'\0' in data:
            continue
        text = data.decode('utf-8', errors='replace')
        if name.startswith('skills/knowledge-interviewer/templates/') and re.search(
                r'^\|\s*`?[a-z][a-z0-9_-]*\.[a-z0-9_.-]+`?\s*\|', text, re.MULTILINE):
            errors.append(f'blank template contains learner rows: {name}')
        if re.search(r'^<!-- learning-private -->$', text, re.MULTILINE) and not name.startswith(
                'skills/knowledge-interviewer/templates/'):
            errors.append(f'private learner marker in shared file: {name}')
        if str(Path.home()) + '/' in text:
            errors.append(f'personal home path in shared file: {name}')
        if staged and name.endswith('.md'):
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                destination = posixpath.normpath(posixpath.join(
                    posixpath.dirname(name), target.split('#')[0]))
                if private_path(destination):
                    errors.append(f'public link targets private learner data: {name}')
                elif destination not in shared_names and not any(
                        item.startswith(destination.rstrip('/') + '/') for item in shared_names):
                    errors.append(f'local link missing from publishable index: {name} -> {target}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    errors = violations(args.root.resolve(), args.staged)
    if errors:
        print('FAIL\n' + '\n'.join(errors))
        return 1
    print('PASS: shared files exclude private learner paths and personal home paths')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
