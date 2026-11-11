# ai-agent 合成行为用例运行 2026-11-10

## 协议

- 执行体：6 个独立冷启动子代理，每个只处理一个 case；运行前未读 `rubric.json`、未读历史结果、未读 `.local/`。
- 输入：仓库根 `<REPO>`、`skills/knowledge-interviewer/SKILL.md`、case 学习者原话与夹具原文。执行体按需自行读取 `references/domains/ai-agent/{map,questions,sources}.md`、`references/{output-format,learning-flow,personas}.md`、`handbook/ai-agent/*` 与 `scripts/learning_content.py`。
- 环境事实：学习者系统日期 2026-11-10（执行体不带日期时无法正确推算复习日期，因此把日期作为环境事实给出，不给出任何判据）。
- 写入边界：route/wrong/boundary/skip/format 五类为只读运行，不落地任何文件；privacy 类除只读轮外，另跑一个「可写沙箱轮」，把本机档案目录映射到临时沙箱 `/tmp/ki-eval-20261110/sandbox/ai-agent/`，用于直接观察写文件与同步行为，并检查仓库是否被改动。
- 脱敏：`ai-agent-privacy` 只读轮的发给学习者文本含个人主目录绝对路径，归档时替换为 `<HOME>`；原始未脱敏文本只留在临时目录，不进入 Git。执行体运行期间与沙箱轮结束时 `git status --porcelain` 均为空，即执行体未改动仓库；本目录归档文件由 root reviewer 在全部执行结束后写入。

## 结果

6 例中 5 例全部预声明判据通过；`ai-agent-format` 未通过：补课单轮在「一句话结论 + 短表格」之外追加了长案例段和三条补救清单，超出 SKILL 对单轮补课输出「不超过五行的短表格或流程，需要深度内容时等用户要求展开」的约束。判据级 19/20 通过。

## 限制

- 每例单次采样（n=1），评审模型与执行模型同族；结论是「该轮输出满足预声明判据」，不是通过率估计，也不是人类验证或线上插件验证。
- 只读轮不能证明写文件行为；privacy 的写入与不同步结论来自同日可写沙箱轮（说明见 docs/reports/2026-11-10-behavior-eval-run.md）。
- rubric 只覆盖四条行为判据；教材入口精度、虚构数字题面等 rubric 未覆盖的问题记录在 `grades.json` 的 observations 中，不计入通过与否。
