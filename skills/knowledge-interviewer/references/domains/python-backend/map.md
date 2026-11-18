# 领域包：python-backend — 知识图谱

面向已有 Python 使用经验、希望用几天建立后端存储、任务分发与 Python Agent 最小闭环的学习者。覆盖 36 个稳定 ID：主链 30 点加工程底座 6 点；短期目标是能解释边界、运行本地实验、识别故障窗口，不是“五天精通”或生产上线认证。工程底座按需查阅，不占五天必做，也不改变主链依赖。中文名称可以改进，ID 不改名、不复用。

本包遵守独立领域契约：[map](map.md) 决定范围与依赖，[questions](questions.md) 提供诊断与判据，[sources](sources.md) 记录实际证据，[maintenance](maintenance.md) 规定更新与检查。这里不复制教材正文。

## 教学环境与选择边界

- 默认 Python 3.11+，使用 3.11 已有的 TaskGroup、asyncio.timeout；不把 3.12+ 新 API 当作 3.11 必备。默认实验针对启用 GIL 的常规 CPython；free-threaded 是 3.13 起可选的 CPython 构建，扩展可能重新启用 GIL，不说所有 Python 的 GIL 相同。
- 本地 demo 使用标准库（asyncio、sqlite3、unittest 等）即可跑，不要求安装数据库服务、模型 SDK 或云服务。SQLite 展示事务、唯一约束、持久队列，不模拟出 PostgreSQL 的全部隔离、锁与执行计划语义。
- 生产起步建议 FastAPI + Pydantic + SQLAlchemy + PostgreSQL；这是便于学习的组合，不是普适必须。同步与异步驱动按工作负载选择；Session per thread、AsyncSession per task，不能因连接池存在就共享一个 Session。
- Redis 按缓存/限流需求选配，不作业务真相源。worker 先用简单持久队列讲清提交、领取与恢复，再按运维能力引入 Celery；BackgroundTasks 不替代持久任务系统。
- S3/兼容对象存储、pgvector 属扩展，不必安装；先用本地文件和租户过滤后的确定性检索替身理解边界。Agent 采用工具契约与状态机，不绑定某个 SDK。
- 默认工具仅在授权范围内只读；不自动云同步个人记录，不自动安装、调用付费云资源或部署。写工具和外部副作用必须另有显式授权与审计，schema 合法不等于有权限。

层级表示学习深度而非固定天数：L1 是语言前提，L2 是并发与单服务/存储边界，L3 是跨故障恢复与 Agent/运维。每行“前置”是进入本点机制题之前需要确认的知识点；“无”表示入口点。

## 1. 语言（6 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.lang.objects` | L1 | 对象、绑定与可变性 | 前置：无；赋值绑定、身份与相等、嵌套共享、浅复制的隔离范围 | 赋值会复制对象；不可变容器里的对象都不可变；用 is 比较业务值 |
| `py.lang.collections` | L1 | 容器与迭代 | 前置：py.lang.objects；list/dict/set 的用途、可哈希键、迭代器消费、生成器按需执行及资源边界 | tuple 总能作键；迭代器能反复遍历；生成器天然不占内存且不会持有资源 |
| `py.lang.functions` | L1 | 函数参数与作用域 | 前置：py.lang.objects；可变默认值在定义时求值、调用间共享、闭包读取绑定、关键字参数契约 | 每次调用新建默认列表；lambda 创建时冻结所有变量；参数注解会转换输入 |
| `py.lang.types` | L1 | 类型与输入边界 | 前置：py.lang.collections、py.lang.functions；注解不强制运行时检查、Protocol、显式输入校验与业务授权分离 | 标 int 就拒绝字符串；Pydantic 合法就可执行工具；类型检查证明业务事实 |
| `py.lang.resources` | L1 | 异常与资源所有权 | 前置：py.lang.functions；with/finally、异常传播、关闭连接与事务回滚不是一回事 | GC 保证及时关闭；except 后返回成功；with sqlite 连接会自动 close |
| `py.lang.environment` | L1 | 解释器与可复现环境 | 前置：py.lang.resources；解释器路径、venv、依赖声明与锁定、配置/秘密分离 | 激活了就必用同一解释器；复制 venv 就能部署；虚拟环境隔离系统依赖和云权限 |

## 2. 并发（4 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.async.eventloop` | L2 | 事件循环与让出执行 | 前置：py.lang.functions、py.lang.resources；协程调用与执行、await 的协作调度、阻塞调用、TaskGroup 作用域 | async def 自动后台执行；await 必定让出；async 就是 CPU 并行 |
| `py.async.cancellation` | L2 | 取消与超时 | 前置：py.async.eventloop、py.lang.resources；3.11 timeout、TaskGroup 失败传播、finally 清理、取消等待与实际副作用分离 | 吞 CancelledError 无影响；取消 to_thread 能杀线程或远端；超时代表没执行 |
| `py.async.backpressure` | L2 | 有界并发与背压 | 前置：py.async.eventloop、py.lang.collections；入口队列、worker、信号量、连接池四层容量及满载策略 | 只加 Semaphore 就限制所有待处理任务；Queue(0) 表示零容量；内存队列可恢复 |
| `py.async.execution` | L2 | 执行模型与线程边界 | 前置：py.async.eventloop、py.lang.environment、py.lang.objects；阻塞 I/O 卸载、CPU 进程并行、GIL/扩展/free-threaded 条件、共享状态同步 | 所有 Python 线程都相同；有 GIL 复合操作就安全；FastAPI 自动卸载所有 def 调用 |

## 3. 服务（4 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.svc.contract` | L2 | API、校验与授权契约 | 前置：py.lang.types、py.lang.resources；请求/响应 schema、错误状态、租户/对象授权、参数化输入 | HTTP 200 表示任务完成；通过校验就有权限；异常文本可以直接发给客户端 |
| `py.svc.lifecycle` | L2 | 服务资源生命周期 | 前置：py.async.cancellation、py.async.execution、py.svc.contract；lifespan、请求资源作用域、Session per thread/AsyncSession per task、关闭顺序 | 全局共享 Session；连接池等于会话线程安全；响应后 BackgroundTasks 保证持久交付 |
| `py.svc.idempotency` | L2 | 幂等键与请求指纹 | 前置：py.svc.contract、py.data.transactions；租户作用域幂等键、规范化请求指纹、唯一约束、处理中/成功/未知结果 | 只有 key 不比较载荷；查后插足以防并发；客户端超时可无条件再扣款 |
| `py.svc.streaming` | L2 | 流式输出与恢复契约 | 前置：py.async.cancellation、py.async.backpressure、py.svc.contract；SSE 帧与事件身份、持久日志/快照、断连与任务状态分离 | SSE 是 checkpoint；发到 socket 就持久化；断连证明远端工具停止 |

## 4. 存储（6 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.data.model` | L2 | 数据模型与约束 | 前置：py.lang.collections、py.lang.types、py.svc.contract；关系模型、tenant_id、业务键/唯一约束、外键、参数绑定、schema 演进 | 所有数据塞 JSON 就不需要约束；字符串拼 SQL；应用先查能代替唯一约束 |
| `py.data.transactions` | L2 | 事务与隔离边界 | 前置：py.data.model、py.lang.resources；原子提交/回滚、PG Read Committed 语句快照、冲突重试、事务与外部调用分离 | 回滚撤销 HTTP/邮件；SQLite 与 PG 锁语义一样；Serializable 永不需要重试 |
| `py.data.indexes` | L2 | 查询与索引证据 | 前置：py.data.model、py.data.transactions；按查询形状选索引、PG17 B-tree 列序边界、EXPLAIN/ANALYZE/BUFFERS、写入代价 | 有索引必走；最左规则适用所有索引/版本；ANALYZE 只看计划不执行 |
| `py.data.cache` | L2 | 缓存一致性与锁所有权 | 前置：py.data.transactions、py.async.backpressure；cache-aside 故障窗口、TTL/抖动、租户键、锁随机 token 的原子比较删除 | TTL 保证强一致；Redis 故障只能停业务；锁 token 就是 fencing 且保护所有副作用 |
| `py.data.objects` | L2 | 对象与元数据状态 | 前置：py.data.model、py.svc.contract、py.svc.idempotency；对象内容与数据库元数据分离、presigned 权限/到期/覆盖、上传验证与清理 | 签名 URL 是一次性且永久私密；上传成功等于扫描/索引就绪；签名可绕过对象授权 |
| `py.data.retrieval` | L3 | 租户隔离检索与版本 | 前置：py.data.objects、py.data.indexes、py.svc.contract；检索前租户/ACL 过滤、chunk 与来源版本、embedding 版本、删除传播、召回验证 | 全库 top-k 后过滤就是安全检索；向量相似即事实正确；必须安装 pgvector 才能理解 |

## 5. 任务分发（4 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.jobs.delivery` | L3 | 持久队列与交付语义 | 前置：py.async.backpressure、py.data.transactions、py.svc.idempotency；领取/执行/确认的崩溃窗口、至少一次、Celery ack/retry 与业务去重 | acks_late 保证恰好一次；同 task-id 自动业务去重；BackgroundTasks 是持久队列 |
| `py.jobs.outbox` | L3 | Outbox 与双写窗口 | 前置：py.jobs.delivery、py.data.transactions；业务行与 outbox 同库同事务、发布/标记窗口、消费者去重、积压对账 | 事务后再发消息不会丢；Outbox 是 exactly-once；标已发布证明下游副作用完成 |
| `py.jobs.leases` | L3 | 租约、接管与 fencing | 前置：py.jobs.delivery、py.data.transactions、py.async.cancellation；原子领取、心跳、单调 generation/fencing、接收端条件写、外部副作用边界 | TTL 到期能杀旧 worker；随机解锁 token 就是单调 fencing；DB 拒绝旧写可撤回已发邮件 |
| `py.jobs.scheduling` | L3 | 重试与定时调度 | 前置：py.jobs.delivery、py.jobs.leases；due_at、退避/抖动/上限、死信、计划周期身份、错过周期与时区策略 | sleep 就是持久调度；所有异常无限重试；重放死信不需要授权和幂等 |

## 6. Agent（3 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.agent.tools` | L3 | SDK 无关工具契约 | 前置：py.lang.types、py.svc.contract、py.svc.idempotency；参数校验、只读默认、服务端授权、超时/预算、结构化结果、写工具审批 | 模型生成参数就是授权；标 read_only 可以自动上传；工具 schema 保证工具成功 |
| `py.agent.runtime` | L3 | 持久运行时与恢复 | 前置：py.agent.tools、py.jobs.outbox、py.jobs.leases、py.svc.streaming；run/step状态、checkpoint、审批绑定、未知副作用对账、事件流投影；交接工件与外部固定验收（进阶） | SDK 内存历史可恢复；SSE 文本是 checkpoint；接管后无条件重跑写工具 |
| `py.agent.evaluation` | L3 | 分层评估与故障回放 | 前置：py.agent.tools、py.agent.runtime、py.data.retrieval；固定模拟夹具、检索/工具/状态分层、故障注入、成功与成本/安全指标；开发/保留边界与CLI/SDK契约对齐（进阶） | 一次回答通顺就是可靠；刚复述教材等于掌握；只读测试可默认触发真实云写入 |

## 7. 运维（3 点）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.ops.observability` | L3 | 可归因观测 | 前置：py.svc.lifecycle、py.jobs.delivery、py.agent.runtime；request/run/task/tenant 关联、队列年龄、延迟分位、错误分类、秘密脱敏 | 平均延迟正常就无积压；每层打印全量 prompt 更安全；日志有 token 才方便排障 |
| `py.ops.deployment` | L3 | 部署与容量边界 | 前置：py.lang.environment、py.svc.lifecycle、py.async.backpressure、py.ops.observability；API/worker 分离、副本总连接预算、readiness/关闭、兼容迁移、显式部署授权 | worker 数越多越快；lifespan 是集群只运行一次；复制 venv 就可上线 |
| `py.ops.recovery` | L3 | 备份、恢复与演练 | 前置：py.jobs.scheduling、py.agent.runtime、py.ops.deployment；RPO/RTO、实际还原、数据库/对象/索引版本、任务重放与副作用对账 | 有备份文件就证明能恢复；重启就是恢复；回滚版本会撤回外部副作用 |

## 8. 工程底座（6 点，按需）

工程底座横切主链，不进入五天必做，也不改变上文 30 点的硬前置；可在 Day 1 前先读依赖与测试，或在遇到相应故障时回查。组题时仍只问一个动作，不因为“基础”就一次问完整套工具链。

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `py.eng.dependencies` | L1 | 依赖、打包与可复现构建 | 前置：py.lang.environment；pyproject 声明与锁文件分工、完整依赖图/哈希、构建一次提升同一 wheel、平台标记与供应链边界 | pyproject 就是锁；顶层包锁住就锁住传递依赖；复制 venv 可复现 |
| `py.eng.testing` | L1 | 测试替身、隔离与假时钟 | 前置：py.lang.functions、py.eng.dependencies；fixture 作用域、yield 清理、patch 查找位置、stub/fake/mock 分工、假时钟、异步测试与覆盖率边界 | 覆盖率 100% 就没 bug；mock 越多越隔离；重跑到绿就是通过 |
| `py.eng.errors` | L2 | 错误分类、重试预算与期限 | 前置：py.async.cancellation、py.svc.idempotency、py.jobs.delivery；永久/暂时/未知结果分类、幂等前提、退避抖动、总期限传播、ExceptionGroup | 所有异常都重试；超时等于未执行；重试越多越可靠 |
| `py.eng.time` | L2 | 时间、时区与数值契约 | 前置：py.jobs.leases、py.data.model；aware/naive、UTC 持久化、monotonic 与墙钟分工、跨进程期限、Decimal/最小货币单位、JSON 编码 | datetime.now() 就是 UTC；不带偏移的 ISO 可以；float 够存金额；monotonic 可跨进程 |
| `py.eng.security` | L3 | 认证、授权与输入边界 | 前置：py.svc.contract、py.data.model、py.agent.tools；主体来源、服务端授权与租户、参数绑定、SSRF、路径穿越、反序列化、秘密与日志脱敏 | schema 合法就有权限；内网可信；JWT 签名等于当前权限；ORM 等于无注入 |
| `py.eng.profiling` | L2 | 性能、内存与容量诊断 | 前置：py.async.execution、py.data.indexes、py.ops.observability；分位延迟、cProfile/采样 profiler、tracemalloc、N+1、连接池/worker 预算、同负载复测 | CPU 不高就没性能问题；加线程一定更快；平均值正常就无尾延迟；缓存总能提速 |

## 依赖与教材定位

图谱按模块展示，不等于整张表从上到下就是拓扑顺序：例如先确认 data.model → data.transactions，才能进入 svc.idempotency；随后才能考 data.objects。组题以各行前置为准。核心闭环为：语言 → 事件循环/取消/背压 → API 与数据模型 → 事务 → 幂等 → 交付 → Outbox/租约 → Agent runtime → 观测/部署/恢复。

完整机制与实验由 `handbook/python-backend/` 教材承担；公共图解归 `materials/python-backend/`。用已有定位器按 ID 找正文：

```bash
python3 skills/knowledge-interviewer/scripts/learning_content.py --domain python-backend --point py.jobs.leases
```

读取返回的 path、heading、start_line/end_line 再讲解；引用真实 display_title，不把本表名称冒充教材标题。章节由其他维护者补齐时，定位为空就明确“教材尚未可定位”，仅用本包参考继续，不编造章节、行号或运行记录。独立安装 Skill 而没有小册同样回退。

## 首次诊断：先语言，再并发，再任务

建议最多四个定位点，计划不是题数配额。只发当前首题，等回答后才决定下一题，不同时列出整套诊断题。

1. py.lang.objects（L1）：用嵌套列表绑定的输出题定位共享模型。
2. py.lang.functions（L1）：用默认参数的独立输出题定位调用间共享；不把“平时用 Python”当作已掌握语言证据。
3. py.async.eventloop（L2）：前置确认后，用阻塞调用定位调度模型；语言缺口未补上就停在语言，不硬跳。
4. py.jobs.delivery（L3）：只在事务/幂等前置已有证据后考“效果提交后、确认前崩溃”的交付窗口；前置不明先补单服务/数据基础，任务题留后续。不要直接冷启动到复杂 Agent 设计。

首题结论正确但机制未知，按缺口另轮追问。未见过的最小变体可验证是否接住，刚听完复述最多视作接住提示，不直接记 A；掌握需要后续独立迁移与失败边界证据。明确不会或当天累计两次 C/D 就补课；题面含糊先作废澄清，不给学习者记错。已有学习记录沿用到期复习，不因新增领域重置进度。

## 几天的起步路线（可伸缩）

| 阶段 | 覆盖组 | 本轮目标 |
|---|---|---|
| 第 1 天附近 | 语言 6 点 | 对象/参数/类型/资源/环境可解释，标准库实验可启动 |
| 第 2 天附近 | 并发 4 点、服务 4 点 | 识别阻塞与取消边界，接口与生命周期可描述；幂等先补事务前置 |
| 第 3 天附近 | 存储 6 点 | 用 SQLite 建立约束与事务闭环，理解 PG/缓存/对象/检索扩展差异 |
| 第 4 天附近 | 任务 4 点 | 持久队列跑通，构造重复/丢失窗口，接管不覆盖旧结果 |
| 第 5 天附近 | Agent 3 点、运维 3 点 | 只读工具与可恢复状态相连，做模拟故障回放与恢复计划 |
| 按需 | 工程底座 6 点 | Day 1 前读依赖/测试；租约、工具授权、调优时回查时间/安全/性能 |

路线覆盖全部 30 点不等于每点已掌握；工程底座 6 点也不因“读过”自动记掌握。按前置与实际答题调整时间，没跑的实验和生产集成均标未验证。跨域时按判断对象选域：Python 实现与 worker 选本包，模型/上下文机制选 ai-agent，浏览器流与交互选 frontend，不混写不同领域成绩。
