# frontend 合成行为用例运行 2026-11-10

## 协议

- 执行体：6 个独立冷启动子代理，每个只处理一个 case；运行前未读 `rubric.json`、未读 `history/2026-11-09` 结果、未读 `.local/`。
- 输入：仓库根 `<REPO>`、`skills/knowledge-interviewer/SKILL.md`、case 学习者原话与夹具原文。执行体按需自行读取 `references/domains/frontend/{map,questions,sources}.md`、`references/{output-format,learning-flow,personas}.md`、`handbook/frontend/*`、`scripts/learning_content.py` 与 `scripts/learning_state.py`。
- 环境事实：学习者系统日期 2026-11-10（只给日期，不给判据）。
- 写入边界：route/wrong/boundary/skip/format 为只读运行；privacy 另跑一个可写沙箱轮，本机档案目录映射到 `/tmp/ki-eval-20261110/sandbox/frontend/`。
- 脱敏：`frontend-privacy` 只读轮的发给学习者文本含个人主目录绝对路径，归档时替换为 `<HOME>`；未脱敏原文只留在临时目录。执行体运行期间 `git status --porcelain` 为空，即执行体未改动仓库；本目录归档文件由 root reviewer 在全部执行结束后写入。

## 结果

6 例全部预声明判据通过，判据级 19/19。另有 4 条 rubric 未覆盖的观察项写入 `grades.json`，其中最实质的是补课轮的教材入口用知识点名称指代章节，而章节实际标题不同，且未先用 `learning_content.py` 定位。

## 限制

- 每例单次采样（n=1），执行与评审同族模型；不构成通过率估计或人类验证。
- 只读轮的写入结论由同日沙箱轮补充证据，两者不是同一次运行。
- 历史前端 12 例（`history/2026-11-09`）反映旧目录与旧领域名，本轮不与之合并计分。
