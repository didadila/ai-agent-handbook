# 五天路线：异步知识检索任务服务

**假设每天 3–4 小时，总计 15–20 小时。** 目标是能跑通本地链路、解释关键故障，并知道哪些生产能力未验证；不是五天精通 Python、分布式或 Agent。时间不足就保留最小改动，把选学标为未完成，不把欠账挤进下一天全部安装。

目标 Python >= 3.11。会 Python 可先用第 1 章自测与最小反例诊断，能解释对应机制就跳过精读；不能自动预填 A，也不能跳过环境、测试入口与项目验收。这里没有真实学习成绩，所有示例片段、建议测试与部署动作在执行前都应视为**未验证**。

[入口与失败矩阵](README.md) · [30 点主链与 6 点工程底座](knowledge-map.md) · [官方证据](../../skills/knowledge-interviewer/references/domains/python-backend/sources.md)

## 项目交付边界

配套 [job_service.py](examples/job_service.py) 与 [test_job_service.py](examples/test_job_service.py) 已提供标准库实验；54项测试（原48项任务性质，加6项测试内教学协议）在2026-11-16的Python 3.13和3.14.5环境复核通过；3.11仅通过语法检查，未验证运行。`submit --db --key --tenant --query`、`work --db`、`get --db --tenant --task-id` 和 `cancel` 都是**CLI，不是 HTTP API**。`submit`返回任务对象，从其 `id` 查询；实际字段以源码与测试为准，测试通过不代表学习者已独立掌握。

贯穿的逻辑链是：校验查询 → 耐久受理 → worker 领取 → 检索适配器 → 条件提交结果 → 租户范围查询。第 2、5 天的异步与工具练习属于小项目扩展，若 CLI 没有对应接口，就用单独的教学适配层完成该最小验证；不能说 demo 已具备 HTTP、真实模型或 agent checkpoint。

生产 `POST /tasks` + `GET /tasks/{id}` 只是[第 3 章设计契约](03-api-and-lifecycle.md)。FastAPI、Pydantic、SQLAlchemy、PostgreSQL 是后续建议组合，SQLite 是标准库实验，不模拟 PG 多写能力。Redis、Celery、S3、向量服务与真实模型都不是五天必装项。

## 固定 ID 全量归属表

表中 ID 表示当天首次阅读/诊断归属；**归属不等于当天实现全部内容**。只在“必做最小改动”列验收一个有界改动，其余是阅读或后续选学。各天 IDs 合计 30，互不重复。另 6 个 `py.eng.*` 工程底座点按需查阅，不占五天名额，见[工程底座](08-engineering-foundations.md)。

| 天 | 固定 IDs（全部归属） | 必做最小改动，仅一个 | 后续选学 / 未完成 |
|---|---|---|---|
| 1 语言与环境/测试 | `py.lang.objects`, `py.lang.collections`, `py.lang.functions`, `py.lang.types`, `py.lang.resources`, `py.lang.environment` | 为提交入口增加一个“拒绝空白 query”的回归用例 | 深层状态隔离、迭代内存测量、静态类型检查与生产依赖锁定 |
| 2 异步 API | `py.async.eventloop`, `py.async.cancellation`, `py.async.backpressure`, `py.async.execution`, `py.svc.contract`, `py.svc.lifecycle`, `py.svc.idempotency`, `py.svc.streaming` | 增加一个有整组期限的只读双路检索适配器，附一个超时清理验收用例 | HTTP 适配器、schema/鉴权、限流、executor 实测、SSE 恢复 |
| 3 SQL 与存储选择 | `py.data.model`, `py.data.transactions`, `py.data.indexes`, `py.data.cache`, `py.data.objects`, `py.data.retrieval` | 增加一个“关闭后重新打开数据库仍能查询已受理任务”的 SQL 持久性用例 | **SQL 为必做；索引、Redis、S3、全文/向量检索只选读边界，实际部署/评估未完成** |
| 4 队列幂等租约重启 | `py.jobs.delivery`, `py.jobs.outbox`, `py.jobs.leases`, `py.jobs.scheduling` | 增加一个“过期接管后旧 lease token 不能提交终态”的恢复回归用例 | 真实 broker/Celery 故障、Outbox relay、重试退避、公平调度、多机时钟/分区 |
| 5 受限 agent、eval、发布恢复 | `py.agent.tools`, `py.agent.runtime`, `py.agent.evaluation`, `py.ops.observability`, `py.ops.deployment`, `py.ops.recovery` | 增加一个 allowlist 拒绝未知工具的 guard，附“stub 适配器零调用”用例 | checkpoint、预算全链路、真实模型 eval、代理多 worker、CDN、滚动/备份恢复演练 |

改动是一个验收切片，不是要求只增加一行代码；测试所需的小适配器算同一切片。若该功能/用例已由示例交付，不重复堆功能：补一个能暴露该机制的新反例并记录证据。若缺少相应实现，先完成最小适配，不顺带扩成生产框架。所有练习是建议任务，本文没有宣称它们已完成。

## Day 1：让最小输入边界有证据

**时间预算**：20 分钟诊断，40–60 分钟语言/环境精读，90 分钟一个测试改动，30–50 分钟运行与解释。

- 基线操作：核实 Python >= 3.11 和解释器路径，确认两份示例文件存在；运行非零测试集。安装失败先解决解释器/导入边界，不先上全套依赖。
- **唯一必做改动**：空白 query 回归用例。验收：输入 `"   "` 被提交入口拒绝，不能留下待执行任务；具体错误类型/退出码依实际示例契约断言，不编造 CLI 输出。若已有空串用例，用纯空白反例补足语义。
- 口头解释：默认参数的列表为什么能跨调用污染、浅拷贝为什么不隔离、SQLite 事务退出为什么不等于关闭连接。可用未执行章节片段设计自己的反例，执行后才记录结果。
- **选学/未完成**：生成器峰值内存、frozen 的浅层边界、类型检查器与锁定依赖。不会这些不阻止进入 Day 2，但不能记作已掌握。

## Day 2：为请求内并发建立退出边界

**时间预算**：45–60 分钟异步机制，30 分钟 API 契约草图，90 分钟一个适配器切片，30–60 分钟失败解释。

- 阅读取舍：重点精读 eventloop、cancellation 与 lifecycle；backpressure/execution/idempotency/streaming 先能指出风险，不要求全实现。
- **唯一必做改动**：带 `TaskGroup` 与 `asyncio.timeout` 的只读双路检索适配器。用可控 awaitable 的 stub 让一路等待；父期限到达后验收“返回/抛出约定超时，子任务完成清理，没有未等待的孤儿任务”。优先用事件与清理标记同步，避免依赖精确毫秒调度。snippet 的两秒是教学值，不是 SLA。
- 契约草图是理解材料，不是额外交付 HTTP 服务：受理先耐久，tenant 来自认证主体；API worker 内存不共享；断流不算成功。Day 3 再落实 SQL 原子性，Day 4 再验证重放。
- **选学/未完成**：真正的 FastAPI 路由、Pydantic 严格 schema、当前授权、入队上限与 SSE。不要把 CLI 的 `--tenant` 称作生产鉴权。

## Day 3：只落实 SQL，明确其他存储为何暂不装

**时间预算**：45–60 分钟 SQL 模型/事务，90 分钟一个持久化用例，30–40 分钟选四类存储边界，15–50 分钟故障说明。

- **唯一必做改动**：关闭提交端连接，再以新连接按 tenant + task ID 查询，同一任务仍存在。测试使用临时数据库并清理；task ID 取自提交结果或实现暴露的查询方式，不假造固定返回值。验收证明本地 SQL 耐久路径，而不是多机/备份能力。
- 必读 model/transactions：唯一键、状态迁移、短事务、session 所有者。说明为何任务和幂等记录不能分开提交，以及为何模型/S3 网络等待不放事务内。
- **明确选读而非安装**：indexes 看查询形状；cache 看 Redis 丢失仍有 SQL 真相；objects 看签名 URL 的 bearer 权限和孤儿回收；retrieval 看租户过滤、原文版本及 stub 的质量边界。每项最多读到能说出“何时需要/何时不需要”。
- **选学/未完成**：PostgreSQL 并发与执行计划、Redis 失效、S3 凭证/生命周期、真实全文/向量索引与召回评估。六点归属 Day 3，不是一天部署六类组件。

## Day 4：接管后不允许旧执行者落库

**时间预算**：45–60 分钟投递/租约机制，90 分钟一个恢复用例，30 分钟 Outbox/调度选读，15–60 分钟重启解释。

- **唯一必做改动**：一个恢复回归用例中，A 领取、推进受控时间令租约过期、B 接管，再尝试 A 的终态写。验收：B 获得新 token，A 条件写被拒绝且未覆盖终态。用假 clock 或显式到期字段，不用长时间 sleep 等运气；若 demo 未暴露 clock，采用最小测试适配。
- CLI 的 `work --db` 可用于观察处理，但不能据此宣称具有真实 broker ack/retry。重启可接管与外部效果幂等分开：旧 A 可能还在远端执行，SQL token 不会自动撤销它。
- **选学/未完成**：kill -9 多进程故障、Celery 的 ack/retry/worker-lost 配置、Outbox relay 重复发布、退避与公平。说明同库同事务 Outbox 的必要性，不要求当日安装队列。若 worker 直接轮询任务表，第一版不需要跨库发布。

## Day 5：验证执行器拒绝，再列出上线欠账

**时间预算**：45–60 分钟工具与 runtime/eval，90 分钟一个 guard 切片，30–40 分钟发布/恢复边界，15–50 分钟复盘。

- **唯一必做改动**：固定 stub 提议未知工具，执行器在适配器调用前拒绝；断言拒绝及调用计数为零。allowlist 映射由代码维护，不用模型给出的 import 路径。合法工具的 schema/当前授权是必须理解的生产要求，但不是这一个测试已覆盖的范围。
- eval 解释：这一测试证明控制面拒绝路径，不证明真实模型会选择正确工具、无注入或能答对问题。checkpoint 恢复还要重新校验授权、版本、未知效果与剩余预算；不得把聊天记录等同耐久执行状态。
- 发布/恢复仅审阅[失败矩阵与上线门槛](README.md)：队列、代理多 worker、静态/CDN、滚动发布分别怎样失败。未做实际部署就写未验证，不以“五天结束”替代门禁。
- **选学/未完成**：真实模型固定问题集、检索分层 eval、预算预留、checkpoint 崩溃点、备份还原、代理/SSE/CDN 和新旧版本共存。下一轮按风险逐个切片，不一次补完。

## 通用运行入口与证据记录

下面是命令用法，从仓库根目录运行。提交后从实际JSON结果取得 task ID，再替换占位符；不预填本机运行结果或学习成绩：

```bash
python3 -m unittest discover -s handbook/python-backend/examples -p 'test_*.py'
python3 handbook/python-backend/examples/job_service.py submit --db /tmp/python-backend-study.db --key study-1 --tenant demo-a --query sqlite
python3 handbook/python-backend/examples/job_service.py work --db /tmp/python-backend-study.db
python3 handbook/python-backend/examples/job_service.py get --db /tmp/python-backend-study.db --tenant demo-a --task-id '<实际 task-id>'
```

选择自己的临时数据库路径，避免覆盖其他练习的数据；示例未交付时只记录“阻塞：缺少示例”，不把 0 tests 当成功。每个切片记录环境、输入、断言、执行命令、实际结果和未覆盖范围；真实个人记录只留本机，不写回公共教材，也不上传个人成绩。

## 五天结束的有限验收

能跑 CLI 的受理/处理/查询与非零测试集；能解释共享对象、事件循环阻塞、超时未知效果、SQL 原子性、租约接管和工具拒绝；能明确区分“已验证切片”“读过机制”“后续未完成”。这就是五天目标。

生产 HTTP、真正多 worker 并发、PG/Redis/S3/broker、真实检索/模型质量、checkpoint 全故障窗口、备份还原和发布演练不在此承诺内。一个 stub 测试、一个 SQLite 恢复用例或一张设计表都不能把这些门槛自动变绿。
