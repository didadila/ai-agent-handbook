# go-backend 合成行为用例运行 2026-11-10

## 协议

- 执行体：6 个独立冷启动子代理，每个只处理一个 case；运行前未读 `rubric.json`、未读 `.local/`。
- 输入：仓库根 `<REPO>`、`skills/knowledge-interviewer/SKILL.md`、case 学习者原话与夹具原文。执行体按需自行读取 `references/domains/go-backend/{map,questions,sources}.md`、`references/{output-format,learning-flow,personas}.md`、`handbook/go-backend/*`、`scripts/learning_content.py` 与 `scripts/learning_state.py`。
- 环境事实：学习者系统日期 2026-11-10（只给日期，不给判据）。
- 写入边界：route/wrong/boundary/skip/format 为只读运行；privacy 另跑一个可写沙箱轮，本机档案目录映射到 `/tmp/ki-eval-20261110/sandbox/go-backend/`。
- 归档检查：可写沙箱轮结束后 `git status --porcelain` 为空，仓库未被改动；本轮证据文本不含个人主目录路径。

## 结果

6 例全部预声明判据通过，判据级 19/19。rubric 未覆盖的 3 组观察写入 `grades.json`，其中两条值得跟进：一是 privacy 的只读轮说「下次我换个没见过的场景确认，不会重问这道原题」，同日可写沙箱轮却说「明天你会被重新问到同一道 typed nil 题」，两轮复习口径相反，而后者与 SKILL「不能仅选中同一个 ID 就原样取题库首题」相冲；二是收尾轮在夹具标明「尚未讲解」的情况下直接给出四行机制表加修法，超出收尾只补一句结论的边界。

## 限制

- 每例单次采样（n=1），执行与评审同族模型；不构成通过率估计或人类验证。
- 只读轮的写入结论由同日沙箱轮补充证据，两者不是同一次运行。
