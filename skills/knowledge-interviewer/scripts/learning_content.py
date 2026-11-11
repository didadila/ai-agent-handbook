#!/usr/bin/env python3
"""Locate public teaching sections by stable ID. Never read learner data."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ALIASES = {'serve': 'go-backend', 'agent': 'ai-agent'}


def locate(root: Path, domain: str, point: str) -> dict:
    domain = ALIASES.get(domain, domain)
    catalog = json.loads((root / 'catalog.json').read_text())
    if domain not in {item['id'] for item in catalog['domains']}:
        raise ValueError('Unknown domain')
    ref = root / 'skills/knowledge-interviewer/references/domains' / domain
    ids = set(re.findall(r'^\|\s*`([^`]+)`\s*\|', (ref / 'map.md').read_text(), re.M))
    if point not in ids:
        raise ValueError('Unknown point for this domain')
    matches = []
    for path in sorted((root / 'handbook' / domain).glob('[0-9][0-9]-*.md')):
        lines = path.read_text().splitlines()
        for offset, line in enumerate(lines):
            if not line.startswith('## ') or not re.search(r'(?<![\w.])' + re.escape(point) + r'(?![\w.])', line):
                continue
            end = next((i for i in range(offset + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
            heading = line[3:]
            display_title = re.sub(r'^(?:\d+(?:\.\d+)*\s+)?' + re.escape(point) + r'\s*[—-]+\s*', '', heading)
            matches.append({'path': str(path.relative_to(root)), 'start_line': offset + 1,
                            'end_line': end, 'heading': heading, 'display_title': display_title})
    return {'domain': domain, 'point_id': point, 'sections': matches,
            'questions': str((ref / 'questions.md').relative_to(root)),
            'sources': str((ref / 'sources.md').relative_to(root)),
            'materials': f'materials/{domain}/README.md'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain', required=True)
    parser.add_argument('--point', required=True)
    args = parser.parse_args()
    result = locate(ROOT, args.domain, args.point)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['sections'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
