# Skill Benchmark: knowledge-interviewer

**Model**: Session cold-start agents; model identifiers not recorded; independent same-family reviewer
**Date**: 2026-11-16T08:32:17Z
**Evals**: 1, 2, 3, 4, 5, 6 (1 run each per configuration; generator default corrected to observed count)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 94% ± 14% | 77% ± 24% | +0.17 |
| Time | 109.6s ± 40.2s | 80.4s ± 12.4s | +29.1s |
| Tokens | 585183 ± 122536 | 285037 ± 45657 | +300146 |

## Notes

- With Skill是当前仓库版；Without Skill是旧Skill快照，不是无Skill。新版21/22条、5/6例；旧版17/22条、2/6例。表中pass rate是各例判据比例的宏平均，不是21/22的加权比例。
- 标准差来自不同case，不是同一case重复采样的稳定性；n=1、同族评分、无人类评审。新版有额外Python教材，不能将差异单独归因于提示文字。
- 新版构建边界遗漏“其他Python实现需另核实”，保留失败。privacy和skip两版均过，区分力弱；旧版skip只确认起点，没有机制诊断。
- Tokens是宿主报告的subagent_tokens，未核验为计费或输出token；tool_calls/errors的0是聚合器缺值默认，不是观察值。并行执行耗时不作受控速度结论。
- 聚合器固定生成3次运行，已更正元数据为实际1次；未改变原评分或统计。