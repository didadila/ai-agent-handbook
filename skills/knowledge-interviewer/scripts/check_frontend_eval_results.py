#!/usr/bin/env python3
"""Validate saved cold-run evidence and complete semantic reviews; never generate model outputs."""
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    folder = Path(__file__).resolve().parents[1] / 'evals/frontend/history/2026-11-09'
    load = lambda name: json.loads((folder / name).read_text())
    cases = load('cases.json')
    rubric = load('rubric.json')
    grades = load('grades.json')
    expected_ids = {case['id'] for case in cases['cases']}
    if set(rubric['cases']) != expected_ids:
        raise ValueError('Rubric/case coverage mismatch')
    totals = {}
    for round_name in ('baseline', 'retest'):
        evidence = load(f'{round_name}.json')
        responses = evidence['results']
        if len(responses) != len(expected_ids) or {x['case_id'] for x in responses} != expected_ids:
            raise ValueError(f'{round_name}: missing or duplicate case outputs')
        if set(grades['rounds'][round_name]) != expected_ids:
            raise ValueError(f'{round_name}: incomplete reviews')
        passed = 0
        for response in responses:
            case_id = response['case_id']
            for field in ('selected_domain', 'selected_id', 'learner_response', 'state_action',
                          'evidence_paths', 'current_fact_sources'):
                if field not in response:
                    raise ValueError(f'{round_name}/{case_id}: missing {field}')
            if not response['learner_response'].strip():
                raise ValueError(f'{round_name}/{case_id}: empty response')
            review = grades['rounds'][round_name][case_id]
            checks = review['checks']
            if [check['criterion'] for check in checks] != rubric['cases'][case_id]:
                raise ValueError(f'{round_name}/{case_id}: criteria changed or incomplete')
            if not review['reason'].strip() or any(type(x['passed']) is not bool for x in checks):
                raise ValueError(f'{round_name}/{case_id}: invalid review')
            passed += all(check['passed'] for check in checks)
        totals[round_name] = passed
        print(f'{round_name}: {passed}/{len(expected_ids)} cases pass all predeclared semantic checks')
    print('Evidence envelopes and reviews are complete. Semantic scores are model-reviewed, '
          'not independently inferred by this script.')
    return 0 if totals['retest'] == len(expected_ids) else 1


if __name__ == '__main__':
    raise SystemExit(main())
