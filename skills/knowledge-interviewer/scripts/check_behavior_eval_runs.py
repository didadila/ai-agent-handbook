#!/usr/bin/env python3
"""Validate archived behavior-eval runs: envelope, rubric coverage, review consistency.

Reads saved cold-start outputs and the reviewer's per-criterion judgements. It never
generates model outputs and never turns structural completeness into a behavior claim.
Every run directory of a domain is validated, so a later re-run cannot hide an older archive.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'skills/knowledge-interviewer'
RUN_FIELDS = ('selected_domain', 'selected_point_id', 'actions_asked', 'state_action', 'external_sync')
SUMMARY_KEYS = ('cases_total', 'cases_passed', 'criteria_total', 'criteria_passed')


def run_dirs(evals_dir: Path) -> list[Path]:
    return sorted((path for path in (evals_dir / 'runs').glob('*') if (path / 'grades.json').exists()),
                  key=lambda path: path.name)


def counts_of(grades: dict, case_ids: list[str]) -> tuple[int, int, int, int]:
    reviews = [grades['cases'][case_id] for case_id in case_ids if case_id in grades['cases']]
    return (
        len(case_ids),
        sum(1 for review in reviews if review.get('case_pass')),
        sum(len(review['criteria']) for review in reviews),
        sum(sum(1 for item in review['criteria'] if item['passed']) for review in reviews),
    )


def check_run(domain: str, run_dir: Path, case_ids: list[str], rubric: dict, errors: list[str]) -> dict:
    label = f'{domain}/{run_dir.name}'
    grades = json.loads((run_dir / 'grades.json').read_text())
    evidence_text = (run_dir / 'evidence.md').read_text()
    readme = run_dir / 'README.md'
    protocol_text = readme.read_text() if readme.exists() else ''
    if set(grades['cases']) != set(case_ids):
        errors.append(f'{label}: reviewed case set differs from cases.json')
    for case_id in case_ids:
        section = re.search(rf'^## {re.escape(case_id)}\n(.*?)(?=^## |\Z)', evidence_text, re.M | re.S)
        if not section:
            errors.append(f'{label}/{case_id}: missing evidence section')
            continue
        body = section.group(1)
        for field in RUN_FIELDS:
            if f'- {field}:' not in body:
                errors.append(f'{label}/{case_id}: evidence missing field {field}')
        review = grades['cases'].get(case_id)
        if not review:
            errors.append(f'{label}/{case_id}: no review')
            continue
        criteria = review['criteria']
        if [item['criterion'] for item in criteria] != rubric.get(case_id):
            errors.append(f'{label}/{case_id}: criteria text/order changed from rubric')
        if any(not isinstance(item['passed'], bool) for item in criteria):
            errors.append(f'{label}/{case_id}: non-boolean judgement')
        if review['case_pass'] != all(item['passed'] for item in criteria):
            errors.append(f'{label}/{case_id}: case_pass does not follow all-criteria rule')
        if not review['reason'].strip():
            errors.append(f'{label}/{case_id}: empty reviewer reason')
    counts = counts_of(grades, case_ids)
    summary = grades['summary']
    if counts != tuple(summary.get(key) for key in SUMMARY_KEYS):
        errors.append(f'{label}: summary counts do not match reviews {counts}')
    texts = {'evidence.md': evidence_text,
             'grades.json': str(grades.get('method', '')) + json.dumps(grades.get('cases', {}), ensure_ascii=False)}
    if protocol_text:
        texts['README.md'] = protocol_text
    for name, text in texts.items():
        if str(Path.home()) + '/' in text:
            errors.append(f'{label}: {name} contains a personal home path')
    for field in ('协议', '结果', '限制'):
        if f'## {field}' not in protocol_text:
            errors.append(f'{label}: run README missing section {field}')
    return dict(zip(SUMMARY_KEYS, counts))


def check_domain(domain: str, errors: list[str]) -> str:
    evals_dir = SKILL / 'evals' / domain
    cases = json.loads((evals_dir / 'cases.json').read_text())
    rubric = json.loads((evals_dir / 'rubric.json').read_text())['cases']
    case_ids = [case['id'] for case in cases['cases']]
    if set(case_ids) != set(rubric):
        errors.append(f'{domain}: rubric/case coverage mismatch')
    runs = run_dirs(evals_dir)
    if not runs:
        errors.append(f'{evals_dir.relative_to(ROOT)}: no archived behavior run')
        return 'no run'
    latest: dict[str, int] = {}
    for run_dir in runs:
        latest = check_run(domain, run_dir, case_ids, rubric, errors)
        # Any archive cases.json points at must describe that archive's real counts.
        for key in ('run', 'previous_run'):
            pointer = cases.get(key) or {}
            if pointer.get('date') != run_dir.name:
                continue
            mismatched = {field: (pointer.get(field), latest[field])
                          for field in SUMMARY_KEYS if pointer.get(field) != latest[field]}
            if mismatched:
                errors.append(f'{domain}/{run_dir.name}: cases.json {key} disagrees with grades {mismatched}')
    if cases.get('status', '').startswith('not_run') and (cases.get('run') or {}).get('cases_passed') is not None:
        errors.append(f'{domain}: cases.json still marked not_run while run results exist')
    return (f"{runs[-1].name}: {latest['cases_passed']}/{latest['cases_total']} cases, "
            f"{latest['criteria_passed']}/{latest['criteria_total']} criteria ({len(runs)} archived run(s))")


def main() -> int:
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    errors: list[str] = []
    for domain in catalog['domains']:
        result = check_domain(domain['id'], errors)
        print(f"{domain['id']}: {result}")
    for error in errors:
        print('ERROR:', error)
    print('Archived envelopes, rubric coverage and review arithmetic are consistent. '
          'This does not prove the behavior passes: passes come from model review of one sampled turn each.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
