# Skill Benchmark: knowledge-interviewer

**Model**: host-managed general-purpose agent; exact model identifier unavailable
**Date**: 2026-11-16T09:44:26Z
**Evals**: 1, 2, 3 (1 runs each per configuration)

## Summary

| Metric | With Skill | Old Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 57% ± 6% | +0.43 |
| Time | 168.4s ± 9.3s | 169.7s ± 9.4s | -1.2s |
| Tokens | 411161 ± 71427 | 389921 ± 22772 | +21240 |

## Notes

- Development regression only: 3 synthetic single-turn cases, n=1 each/configuration. with_skill 14/14 criteria and 3/3 cases; old_skill 8/14 and 0/3. No repeated reliability, holdout, human agreement or learning effectiveness claim.
- The summary pass rate is a macro-average across unequal-size case rubrics; criterion totals are reported separately. Standard deviations describe across-case variation, not repeated-run uncertainty.
- Both versions pass all format criteria and correct the 15pp range/nonpipeline concepts. New-version differences concern explicit exposure audit, misclassification structure, current authorization, evaluator bias boundaries and sensitive collection safeguards.
- The harness criterion permits absence of a universal requirement; current reply does not actively explain task/model-based harness simplification. A future transfer case can probe it; fixed rubric and original replies are unchanged.
- Execution and grading share an agent family; no human review. public_reads is executor-reported and checked for file existence, not independently complete I/O.
- Time and subagent_tokens come from host completion notifications; tokens are not validated output or billable counts. tool_calls is the host total tool-use count; error count unavailable and not defaulted to zero.
- Both configurations disallow handbook and real learner state. Baseline is the immediately preceding Skill, not no-Skill or initial Git HEAD. See protocol.json for snapshots and limitations.
