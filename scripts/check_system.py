#!/usr/bin/env python3
"""Check the public four-domain contract; never read learner records."""
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/knowledge-interviewer'


def main():
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    errors = []
    total = 0
    for domain in catalog['domains']:
        name = domain['id']
        ref = SKILL / 'references/domains' / name
        book = ROOT / 'handbook' / name
        required = [book / f for f in ('README.md', 'knowledge-map.md')]
        required += [ref / f for f in ('map.md', 'questions.md', 'sources.md', 'maintenance.md')]
        required += [ROOT / 'materials' / name / f for f in ('README.md', 'maps/overview.html', 'cards/01.md')]
        required += [SKILL / 'evals' / name / f for f in ('cases.json', 'rubric.json')]
        for path in required:
            if not path.is_file():
                errors.append(f'missing {path.relative_to(ROOT)}')
        pattern = r'^\|\s*`([^`]+)`\s*\|'
        if name == 'frontend':
            pattern += r'\s*L[123]\s*\|'
        ids = re.findall(pattern, (ref / 'map.md').read_text(), re.M)
        questions = re.findall(r'^###\s+`([^`]+)`', (ref / 'questions.md').read_text(), re.M)
        if len(ids) != domain['points'] or len(set(ids)) != len(ids):
            errors.append(f'{name}: map count/duplicates')
        if set(ids) != set(questions) or len(questions) != len(set(questions)):
            errors.append(f'{name}: question coverage/duplicates')
        text = '\n'.join(p.read_text() for p in book.glob('*.md') if p.name not in ('README.md', 'knowledge-map.md', 'progress.md', 'mistakes.md'))
        for identifier in ids:
            if identifier not in text:
                errors.append(f'{name}: no chapter coverage for {identifier}')
        reading_text = (book / 'knowledge-map.md').read_text()
        for identifier in ids:
            if identifier not in reading_text:
                errors.append(f'{name}: missing reading-map ID {identifier}')
        cases_path = SKILL / 'evals' / name / 'cases.json'
        rubric_path = cases_path.with_name('rubric.json')
        if cases_path.exists() and rubric_path.exists():
            cases = json.loads(cases_path.read_text())['cases']
            rubric = json.loads(rubric_path.read_text())['cases']
            if {c['id'] for c in cases} != set(rubric):
                errors.append(f'{name}: eval rubric coverage')
            for case in cases:
                if case['point_id'] not in ids:
                    errors.append(f'{name}: unknown eval point {case["point_id"]}')
        total += len(ids)
        print(f'{name}: {len(ids)} points / {len(questions)} question chains')
    # Include tracked and new public files, excluding ignored local records.
    listed = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT).decode().split('\0')
    files = {Path(f) for f in listed if f and (ROOT / f).is_file()}
    for relative in sorted(files):
        if relative.suffix != '.md':
            continue
        # Historical evidence may contain intentionally recorded former paths.
        if 'history' in relative.parts or 'legacy' in relative.parts:
            continue
        text = (ROOT / relative).read_text()
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            target = unquote(target.split('#')[0])
            if not target or re.match(r'^[a-zA-Z][\w+.-]*:', target):
                continue
            path = (relative.parent / target).resolve() if relative.is_absolute() else (ROOT / relative.parent / target).resolve()
            try:
                published = path.relative_to(ROOT)
            except ValueError:
                errors.append(f'{relative}: link outside repository {target}')
                continue
            if published not in files and not path.is_dir():
                errors.append(f'{relative}: missing public link {target}')
    for error in errors:
        print('ERROR:', error)
    print(f'{total} stable points; {len(errors)} errors. Static coverage does not prove model behavior.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
