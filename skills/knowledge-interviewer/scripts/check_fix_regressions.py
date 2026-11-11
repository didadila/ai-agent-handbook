#!/usr/bin/env python3
"""Validate v2 fix evidence without rewriting or rescoring the original v1 run."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from check_response_format import check_response

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / 'skills/knowledge-interviewer/evals/regressions/2026-11-10-fixes'


def check_suite(folder: Path, root: Path = ROOT) -> tuple[list[str], dict]:
    errors = []
    cases = json.loads((folder / 'cases.json').read_text())
    rubric = json.loads((folder / 'rubric.json').read_text())['cases']
    responses = json.loads((folder / 'responses.json').read_text())['results']
    grades = json.loads((folder / 'grades.json').read_text())
    ids = [case['id'] for case in cases['cases']]
    actual = [result['case_id'] for result in responses]
    if len(set(ids)) != len(ids) or len(set(actual)) != len(actual) or set(actual) != set(ids):
        errors.append('Missing or duplicate case/response IDs')
    if set(rubric) != set(ids) or set(grades['cases']) != set(ids):
        errors.append('Rubric/review coverage mismatch')
    if cases['status'].startswith('not_run'):
        errors.append('Executed suite still marked not_run')
    for response in responses:
        identifier = response['case_id']
        for field in ('selected_domain', 'selected_point_id', 'learner_response', 'evidence_paths',
                      'commands', 'state_action', 'external_sync', 'actions_asked', 'written_files'):
            if field not in response:
                errors.append(f'{identifier}: missing {field}')
        if not response.get('learner_response', '').strip():
            errors.append(f'{identifier}: empty learner response')
        case = next((c for c in cases['cases'] if c['id'] == identifier), {})
        if cases.get('schema_version', 0) >= 3 and case.get('format_mode'):
            structure_errors = check_response(response.get('learner_response', ''), case['format_mode'])
            review = grades['cases'].get(identifier, {})
            first = review.get('criteria', [{}])[0]
            if first.get('passed') != (not structure_errors):
                errors.append(f'{identifier}: structural judgement contradicts format checker: {structure_errors}')
    for identifier in ids:
        review = grades['cases'].get(identifier)
        if not review:
            continue
        criteria = review['criteria']
        if [c['criterion'] for c in criteria] != rubric.get(identifier):
            errors.append(f'{identifier}: changed criterion text/order')
        if any(type(c['passed']) is not bool for c in criteria):
            errors.append(f'{identifier}: judgement is not Boolean')
        if review['case_pass'] != all(c['passed'] for c in criteria):
            errors.append(f'{identifier}: case_pass contradicts criteria')
        if not review['reason'].strip():
            errors.append(f'{identifier}: missing review reason')
    reviews = list(grades['cases'].values())
    expected = dict(cases_total=len(ids), cases_passed=sum(r['case_pass'] for r in reviews),
                    criteria_total=sum(len(r['criteria']) for r in reviews),
                    criteria_passed=sum(c['passed'] for r in reviews for c in r['criteria']))
    if any(grades['summary'].get(k) != v for k, v in expected.items()):
        errors.append('Summary arithmetic mismatch')
    for path in folder.glob('*.json'):
        if re.search(r'/(?:Users|home)/[^/\s<>]+/', path.read_text()):
            errors.append(f'{path.name}: personal home path in public evidence')
    snapshot = folder / 'baseline-sha256.json'
    if snapshot.exists():
        for name, checksum in json.loads(snapshot.read_text()).items():
            path = root / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
                errors.append(f'Original evidence/rubric changed: {name}')
    return errors, expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', type=Path, default=SUITE)
    args = parser.parse_args()
    errors, summary = check_suite(args.suite)
    print('initial:', json.dumps(summary))
    retest = args.suite / 'privacy-retest'
    if (retest / 'responses.json').exists():
        retest_errors, retest_summary = check_suite(retest)
        errors.extend(retest_errors)
        print('privacy retest:', json.dumps(retest_summary))
    for error in errors:
        print('ERROR:', error)
    print('Envelope and original-evidence checks only; semantic judgements are saved model reviews.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
