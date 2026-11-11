# java-backend 合成行为用例运行 2026-11-10

## 协议

- 执行体：6 个独立冷启动子代理，每个只处理一个 case；运行前未读 `rubric.json`、未读 `.local/`。
- 输入：仓库根 `<REPO>`、`skills/knowledge-interviewer/SKILL.md`、case 学习者原话与夹具原文。执行体按需自行读取 `references/domains/java-backend/{map,questions,sources}.md`、`references/{output-format,learning-flow,personas}.md`、`handbook/java-backend/*`、`scripts/learning_content.py` 与 `scripts/learning_state.py`。
- 环境事实：学习者系统日期 2026-11-10（只给日期，不给判据）。
- 写入边界：route/wrong/boundary/skip/format 为只读运行；privacy 另跑一个可写沙箱轮，本机档案目录映射到 `/tmp/ki-eval-20261110/sandbox/java-backend/`。
- 归档检查：沙箱轮结束后 `git status --porcelain` 为空；证据文本不含个人主目录路径。`java-backend-format` 的执行信封里多出一行 `<<<LEARNING_TURN_PLACEHOLDER>>>` 标记，属执行体格式产物，归档时剔除并在 grades.json 记录。

## 结果

6 例全部预声明判据通过，判据级 19/19。值得跟进的两条观察：`java-backend-wrong` 用自设的具体运行数字（最终 18437、丢 1563）作为题干却未标明是构造场景，与仓库「论文或厂商实验数字需保留样本与来源」的新鲜度规则相邻，题面自设数字应显式标注；`java-backend-format` 把 JMM 讲成「每个线程留着共享变量的私有副本」，而 handbook 第 19 行明确「主内存/工作内存只作抽象解释，不与每级 CPU 缓存一一对应」，该轮丢了这个限定。

## 限制

- 每例单次采样（n=1），执行与评审同族模型；不构成通过率估计或人类验证。
- 只读轮的写入结论由同日沙箱轮补充证据，两者不是同一次运行。
