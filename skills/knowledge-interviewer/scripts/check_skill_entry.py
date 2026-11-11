#!/usr/bin/env python3
"""Verify that a loader entry resolves to this Skill and its current resources."""
import argparse
import hashlib
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REQUIRED = ('SKILL.md', 'references/output-format.md', 'scripts/learning_state.py',
            'scripts/check_response_format.py')


def inspect_entry(entry: Path, expected: Path = SKILL) -> dict:
    same = entry.is_dir() and expected.is_dir() and entry.resolve() == expected.resolve()
    resources = {name: (entry / name).is_file() and (expected / name).is_file()
                 and (entry / name).samefile(expected / name) for name in REQUIRED}
    skill = entry / 'SKILL.md'
    return {'entry_is_symlink': entry.is_symlink(), 'same_directory': same,
            'resources_match': resources, 'passed': same and all(resources.values()),
            'skill_sha256': hashlib.sha256(skill.read_bytes()).hexdigest() if skill.is_file() else None,
            'scope': 'Filesystem entry identity; host process caches are not inspected.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entry', type=Path, default=Path.home() / '.qoder/skills/knowledge-interviewer')
    args = parser.parse_args()
    result = inspect_entry(args.entry)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return not result['passed']


if __name__ == '__main__':
    raise SystemExit(main())
