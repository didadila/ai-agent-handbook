# Python 后端知识小册

**7 章主链 30 点 + 工程底座 6 点，贯穿“异步知识检索任务服务”。** 从 Python 的对象与资源所有权出发，走到异步 API、SQL 真相、任务接管、受限 Agent 工具与交付恢复；另用一章补依赖、测试、错误、时间、安全与性能，避免把“能跑”误当可靠。适用 Python >= 3.11；不要求先读 Java 或 Go，也不以安装最多组件为目标。

本册适合会一些 Python、希望能解释服务故障的人。已有基础可先诊断再跳过相应精读，不预填任何掌握档位，不记录真实用户成绩。五天按每天 3–4 小时，只承诺跑通最小链路并解释关键失败，**不是精通，也不是生产就绪认证**。

## 章节、30 点主链与 6 点工程底座

编号章中的定位格式固定为 `## py.xxx — 中文真实语义标题`；每个 ID 只在对应章有一个二级标题。正文采用结论、具体案例、机制、取舍边界、误解靶子、判据和一题自测。代码与案例均为**未执行教学示例/构造故障**，不是实测日志或 demo 源码复述。

| 章 | 入口 | 点数 | 固定 IDs |
|---|---|---:|---|
| 1 | [Python 基础](01-python-foundations.md) | 6 | `py.lang.objects`, `py.lang.collections`, `py.lang.functions`, `py.lang.types`, `py.lang.resources`, `py.lang.environment` |
| 2 | [异步与并发](02-async-and-concurrency.md) | 4 | `py.async.eventloop`, `py.async.cancellation`, `py.async.backpressure`, `py.async.execution` |
| 3 | [API 与生命周期](03-api-and-lifecycle.md) | 4 | `py.svc.contract`, `py.svc.lifecycle`, `py.svc.idempotency`, `py.svc.streaming` |
| 4 | [存储与检索](04-storage-and-retrieval.md) | 6 | `py.data.model`, `py.data.transactions`, `py.data.indexes`, `py.data.cache`, `py.data.objects`, `py.data.retrieval` |
| 5 | [任务与分发](05-jobs-and-distribution.md) | 4 | `py.jobs.delivery`, `py.jobs.outbox`, `py.jobs.leases`, `py.jobs.scheduling` |
| 6 | [Python Agent](06-python-agent.md) | 3 | `py.agent.tools`, `py.agent.runtime`, `py.agent.evaluation` |
| 7 | [运行与交付](07-operations-and-delivery.md) | 3 | `py.ops.observability`, `py.ops.deployment`, `py.ops.recovery` |
| 附录 | [工程底座](08-engineering-foundations.md) | 6 | `py.eng.dependencies`, `py.eng.testing`, `py.eng.errors`, `py.eng.time`, `py.eng.security`, `py.eng.profiling` |

[knowledge-map.md](knowledge-map.md)给出每点唯一章节、DAG 硬前置、非目标与跨卷桥梁。首次可按 1 → 2 → 3 → 4 → 5 → 6 → 7 读；实际实现分层推进，比如 Day 2 先设计幂等契约，Day 3 落 SQL，Day 4 再检验重放。

工程底座 6 点是**按需查阅**，不占五天必做名额，也不改变主链硬前置。建议在 Day 1 前先读“依赖”和“测试”，在进入租约、工具授权和性能调优时分别回查“时间”“安全”“性能”；读完不等于已掌握，也不要求额外安装工具。

## 五天路线：每日只一个最小验收切片

完整固定 ID 归属与时间分配见 [sprint-5-days.md](sprint-5-days.md)，主链 30 点全部分配但不要求当天全部实现；工程底座 6 点不在五天必做表内。

| 天 | 阅读范围 | 唯一必做最小改动 | 当天不强制完成 |
|---|---|---|---|
| Day 1 | 01 的 6 点：语言、环境、测试 | 空白 query 被拒绝且不留待执行任务的回归用例 | 静态类型/性能工具、生产依赖栈 |
| Day 2 | 02 + 03 的 8 点：异步 API | 一个 TaskGroup + timeout 的双路只读检索适配器及超时清理用例 | 真实 HTTP、限流、executor 测量、SSE |
| Day 3 | 04 的 6 点：SQL 与存储选型 | 关闭后重开数据库仍能查询任务的持久性用例 | **必做 SQL；索引/缓存/对象/检索选读，PG/Redis/S3/向量组件部署未完成** |
| Day 4 | 05 的 4 点：队列、幂等、租约、重启 | 过期接管后旧 lease token 不能提交终态的用例 | broker/Celery、Outbox relay、多机公平调度 |
| Day 5 | 06 + 07 的 6 点：工具、eval、发布恢复 | allowlist 拒绝未知工具且 stub 零调用的 guard 用例 | checkpoint 全故障窗口、真实模型 eval、代理/CDN/滚动/还原演练 |

“适配器 + 对应断言”算同一个有界功能切片，不把更多组件混进验收。已存在的用例补一个新反例即可；未完成项保留为下一轮选学。五天不强迫每天部署一套新基础设施。

## 配套 CLI 与运行入口

- [examples/job_service.py](examples/job_service.py)：标准库 SQLite CLI，提供提交、领取执行、查询、取消与Outbox实验；只读关键词 Agent 替身不调用真实模型。
- [examples/test_job_service.py](examples/test_job_service.py)：54项确定性测试（原48项任务性质，加6项交接/验收/记忆教学协议），2026-11-16在Python 3.13和3.14.5复核通过；协议仅为测试内教学模型。源码通过Python 3.11语法检查，但未在3.11解释器运行；真实HTTP与外部存储未做集成验收。

CLI操作为 `submit --db --key --tenant --query`、`work --db`、`get --db --tenant --task-id` 与 `cancel --db --tenant --task-id`。从仓库根目录运行，以下是命令用法；查询占位符需替换为真实提交所得 ID，数据库路径选择自己的临时文件：

```bash
python3 --version
python3 -m unittest discover -s handbook/python-backend/examples -p 'test_*.py'
python3 handbook/python-backend/examples/job_service.py submit --db /tmp/python-backend-study.db --key study-1 --tenant demo-a --query sqlite
python3 handbook/python-backend/examples/job_service.py work --db /tmp/python-backend-study.db
python3 handbook/python-backend/examples/job_service.py get --db /tmp/python-backend-study.db --tenant demo-a --task-id '<实际 task-id>'
```

检查测试集确实非零；实际覆盖以测试断言为准。内置合成文档使用 `demo-a` 与 `demo-b` 命名空间，未知租户不会回退读取其他租户；CLI 中 `--tenant` **不是生产身份认证**。异步检索与 agent 工具切片若未包含在 CLI 中，应作为教学适配扩展验证，不能反称 demo 已提供这些能力。

## demo、生产契约与选型边界

生产设计可提供 `POST /tasks` 与 `GET /tasks/{id}`，见[第 3 章](03-api-and-lifecycle.md)：先持久受理、同租户幂等键绑定内容、按当前授权查询。**这只是设计契约，demo 并未因此提供 HTTP API**。

- 建议 FastAPI + Pydantic + SQLAlchemy + PostgreSQL 分别承担服务入口、边界校验、持久化映射与权威事务；兼容版本按实际项目锁定与官方资料核验，不硬编码最新依赖。
- Python >= 3.11 用 TaskGroup/timeout 教生命周期。GIL 行为是目标 CPython 构建与扩展边界，不是“所有 Python 永远不能并行”。
- SQLite 适合标准库本地 demo，不模拟 PG 多写能力；Redis 是可重建缓存，不是跨系统事务真相。
- S3 私有工件与公共静态/CDN 分开；访问凭证按秘密保护，预签名 URL 是 bearer 能力，不能进入默认日志。
- Celery ack/retry 不能获得 exactly-once；Outbox 必须同库同事务；租约允许过期接管，外部效果还需幂等、fencing 支持或对账。
- Agent 执行器必须同时有工具 allowlist、schema 和当前授权；checkpoint/预算约束恢复。确定性 stub 只证明控制面路径，不证明真实模型、检索或安全质量。

## 小项目失败矩阵

以下是待验收场景和正确性判据，**不是“已测试通过”的结果表**。可以离线验证的只在实际用例执行后算完成；其他项进入生产前另做。

| 故障注入 | 机制/目标结果 | 最小证据 | 范围 |
|---|---|---|---|
| 默认列表或浅拷贝被一租户修改 | 每任务嵌套状态隔离 | A 的修改不影响 B 的断言 | Python 单元测试 |
| 一路检索长等待、另一任务失败/父超时 | TaskGroup 等待取消清理；不遗留孤儿 | 清理标记、完成状态与受控异步测试 | 教学异步适配器，不是远端效果撤销 |
| 超量提交或下游阻塞 | 活跃数/等待数/字节/期限有上限 | 拒绝路径与队列年龄变化 | 生产入口/负载另验 |
| 同键并发、同键异内容、响应丢失 | 租户唯一约束与摘要；安全重放/冲突 | 一个任务、冲突拒绝、重放查询 | SQLite 功能与 PG 多写分开验 |
| SQL 两次相关写之间异常 | 同事务回滚，不等待网络 | 两项均未提交 | SQLite/PG 各自事务测试 |
| Redis 清空/失效失败 | SQL 真相仍在，缓存可重建 | 终态/幂等正确及不一致窗口 | 可选缓存集成 |
| S3 上传后 SQL 失败、签名泄露风险 | 孤儿回收；权限与 bearer 生命周期 | 对账记录、去敏日志、授权下载检查 | 可选对象存储集成 |
| relay 发布后标记 sent 前崩溃 | 重复发送允许，消费效果幂等 | 同 event ID 重放无新效果 | 同库 Outbox + 真实 broker 另验 |
| 结果提交后 ack 前崩溃 | 投递可能重放，终态/效果不重复 | 稳定效果 ID 与重复 handler 用例 | Celery/broker 真实配置另验 |
| A 租约过期、B 接管、A 恢复 | 新 token 领取，旧 token 条件写拒绝 | 旧写未覆盖；未知外部效果另对账 | 本地恢复不证明多机分区 |
| stub 提议未知工具/非法 schema/跨租户/撤权 | 调用前拒绝，合法范围才执行 | 拒绝断言且适配器零调用 | Day 5 只必做未知工具，其余另验 |
| checkpoint 在外部调用后未落盘 | 查询/对账未知效果，不盲重试 | 持久阶段、效果 ID、恢复分支 | 可选耐久 agent 扩展 |
| SSE 重连重复/缺口/代理断流 | 状态真相独立，去重或 GET 快照恢复 | 流解析与恢复测试 | 生产流设计，非 CLI 能力 |
| API 多 worker 与滚动新旧副本 | 无内存真相、连接预算含重叠、协议兼容 | 代理路由、drain、迁移共存检查 | HTTP/部署另验 |
| CDN 旧静态清单、私有工件缓存 | 哈希工件与可更新入口分离，私有不公开 | 旧客户端仍工作、授权缓存检查 | 静态/CDN 另验 |
| 数据备份还原，索引/对象版本失配 | 接管、重建、引用抽查、效果对账 | 实际还原的 RPO/RTO 与一致性证据 | 生产恢复另验 |

工程底座的检查同样以断言为准，不要求安装额外框架；未运行就写“未验证”。

| 故障注入 | 目标结果 | 最小证据 |
|---|---|---|
| 同一份依赖声明在不同日期解析 | 锁记录完整依赖图、版本与哈希 | 干净环境重建同一 wheel，依赖差异可审阅 |
| 两个测试共享模块级状态/真实时钟 | 每个测试独立、可重复、可并行 | 单独与整组运行结果一致；假时钟推进 |
| 400 校验错误进入通用重试 | 永久错误快速失败，不重试 | 适配器调用次数与错误码断言 |
| naive/aware 时间比较、float 金额累加 | 拒绝混用、金额有精度契约 | 边界用例与量化/舍入断言 |
| 请求体 tenant、任意 URL、不可信 pickle | 主体来源唯一、SSRF/反序列化被拒绝 | 跨租户、内网地址与恶意载荷的拒绝断言 |
| 只加线程/缓存后 p99 仍高 | 先定位等待、连接池或 N+1 | 分位延迟、查询次数与资源证据 |

## 上线门槛：本地全绿也不能自动放行

学习验收是五个有界切片与关键故障解释；以下是生产门槛，未执行就标“未验证”，不要勾成完成：

- **可重复构建**：目标 Python/CPython 构建、完整依赖锁与哈希、非零自动测试集可复现；构建一次并在测试/部署提升同一 wheel，未执行示例不计证据。
- **契约与隔离**：真实 HTTP schema、当前认证/租户授权、大小/容量上限、幂等冲突与旧客户端兼容通过测试；SSRF、路径穿越、不可信反序列化有拒绝用例；CLI tenant 不作替代。
- **持久正确性**：目标 PG 下并发唯一性、条件终态写、短事务/连接预算验证；需要队列时，真实 ack/retry、Outbox 与毒消息出口演练。
- **效果与 agent 安全**：外部幂等/未知结果对账明确；allowlist/schema/当前授权拒绝、checkpoint 恢复与累计预算验证；stub 控制面与真实检索/模型 eval 分开，不能接受实际租户泄露。
- **四路交付**：队列、反向代理多 worker、静态/CDN、滚动发布各有容量/安全/兼容验收；停止接单/领取与有界 drain 有证据。
- **性能与容量**：目标环境有 p50/p95/p99、排队、连接池和内存证据；优化前后同负载复测，不用本地微基准替代生产容量。
- **可恢复与可止损**：队列年龄/终态/租约/成本可观测，日志去敏；备份实际还原、引用重建、授权复核、RPO/RTO 和回滚/前向修复责任明确。

## 配套与衔接

- [30 点主链与 6 点工程底座](knowledge-map.md)、[五天路线](sprint-5-days.md)、[工程底座正文](08-engineering-foundations.md)。
- [官方证据与时效边界](../../skills/knowledge-interviewer/references/domains/python-backend/sources.md)：逐条记录核验切面，不以链接代替实际环境核验。
- [AI Agent 卷](../ai-agent/README.md)：模型提议、上下文、检索与评估。
- [Go 后端卷](../go-backend/README.md)：对照生命周期、背压、幂等和未知效果，不是必读前置。
- [前端卷](../frontend/README.md)：任务投影、流式恢复、审批和旧页面交付。

共享的是教材与空白判据，不是真实个人档案。使用现有 knowledge-interviewer 进入Python路线；仓库版与全局复制安装的版本可能不同，应先核验入口，不自动修改全局设置。
