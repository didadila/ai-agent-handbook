# Python 后端陪练评测

[6个原始用例与只读fixture](cases.json)和[22条预声明判据](rubric.json)覆盖五天计划、异步阻塞、GIL构建边界、收尾隐私、换点及工具授权。[evals.json](evals.json)提供Skill Creator格式的同组prompt与assertions；执行时仍须同时采用cases.json的fixture，尤其不能忽略privacy的只读限制。

## 实际运行

[2026-11-16运行归档](runs/2026-11-16/README.md)保留新版六例的真实单轮输出、读取元数据、逐项理由与实际成绩。新旧版共12次冷启动；工作区`with_skill`是当前仓库版本，`without_skill`是旧Skill快照，**不是完全不使用Skill**。旧版源自提交`2e4a02c`，新增Python内容没有提前交给旧版执行体。

打开[评审页](../../../knowledge-interviewer-workspace/iteration-1/review.html)可逐例查看新旧输出、评分和benchmark，并留下本地反馈；评审页本身不发布到云端。自动评分不替代人工审阅。

## 验证范围

模型评测检查教学路由、机制、教材入口、短表与单个问题。privacy例未读真实档案，未授权任何真实状态写入，不能把“没有保存”解释成成功验证了写档；`test_python_domain.py`与既有state安全测试另用合成临时目录验证空表初始化、数据保留及路径/权限门禁。

每例每版n=1，执行与评分同族；旧版资源不同，不能把差值当长期学习收益或生产可靠性。原四域24例及旧rubric独立保留。目录、格式和汇总脚本通过只说明结构与算术一致，不自动证明模型语义通过。

配套CLI的48项确定性测试与这6例模型行为测评是不同证据；真实HTTP、LLM、Redis/S3、Celery/broker、部署和还原仍需按教材门槛另验。
