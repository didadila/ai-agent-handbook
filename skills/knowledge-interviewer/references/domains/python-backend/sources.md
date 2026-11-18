# Python 后端领域 — 证据索引

## 核验口径

本次实际用 WebFetch 读取正文并核验的官方页面共 35 个（主链 22 个，工程底座新增 13 个）。以下 `verified_at=2026-11-16` **只覆盖每条列明的切面**，是核验日期，不是发布时间、版本发布日期或整套产品认证。没有全表通用核验日期。失败、只得到重定向、未打开的页面一律待核验；一个页面中的链接不算已读取。

默认教学 Python 3.11+；Python 3.11、PostgreSQL 17、SQLAlchemy 2.0 是引用文档边界，不称最新版本。URL 中的 `latest`/`stable` 是官方路由，不代表本包承诺当前最高版本或所有配置相同。free-threaded 资料讨论可选 CPython 构建，不把它反推为 3.11 默认行为。

稳定机制、组件契约与工程设计分开：官方材料支持具体 API/隔离/交付规则；本包设计的 tenant+key、generation 条件写、Outbox 状态机、审批字段与教学时间安排不是这些文档的标准定义。引用一页不能证明本地 demo、真实云集成、性能或生产恢复已验证。

## 已读取的主要官方来源

### Python 语言与并发

| 来源 | 实际 URL | 本次明确支持的切面 | 状态与不外推边界 |
|---|---|---|---|
| P01 | [Python 3.11 Coroutines and Tasks](https://docs.python.org/3.11/library/asyncio-task.html) | TaskGroup 与 asyncio.timeout 在 3.11 新增；协程/任务、协作调度；非 CancelledError 失败取消组内其他任务并等待；finally 清理、通常传播取消；吞取消会影响结构化并发；to_thread 主要用于阻塞 I/O，释放 GIL 的扩展/其他实现有 CPU 例外 | verified_at=2026-11-16；不证明远端副作用被取消或撤销，不给出线程硬终止承诺，不声称所有 await 都挂起 |
| P02 | [Python 3.11 Data model](https://docs.python.org/3.11/reference/datamodel.html) | 对象有身份/类型/值；容器保存引用；不可变容器可引用可变对象；不依赖及时垃圾回收，外部资源应显式释放，with/finally 可管理 | verified_at=2026-11-16；id 是地址仅属 CPython 实现细节，不泛化所有实现；本次未完整核验其映射/哈希子节 |
| P03 | [Python 3.11 More Control Flow Tools](https://docs.python.org/3.11/tutorial/controlflow.html) | 默认表达式在定义时求值一次，可变默认值跨调用共享；None 后新建容器；lambda 可访问外层作用域；位置/关键字与 `/`、`*` 参数契约 | verified_at=2026-11-16；本次明确读取不独立证明所有闭包晚绑定场景，相关精确切面另列待核验 |
| P04 | [Python 3.11 typing](https://docs.python.org/3.11/library/typing.html) | Python 运行时不强制函数/变量注解；Protocol 支持结构化静态子类型 | verified_at=2026-11-16；不证明运行时 schema 转换、工具授权或业务正确 |
| P05 | [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html) | 3.13 起可选 CPython free-threaded 构建；构建/运行参数与扩展兼容性可能启用 GIL；内置类型内部保护不替代显式同步建议 | verified_at=2026-11-16；不称所有 Python 实现/版本 GIL 相同，不宣称默认安装一定无 GIL，不据此保证共享 Session 安全 |
| P16 | [Python 3.11 asyncio Queues](https://docs.python.org/3.11/library/asyncio-queue.html) | maxsize>0 有界，满时 await put 等待；put_nowait 可 QueueFull；maxsize<=0 无界；task_done/join 用未完成任务计数；不线程安全 | verified_at=2026-11-16；页面不承诺磁盘持久交付，join 不能证明外部副作用成功 |
| P17 | [Python 3.11 sqlite3](https://docs.python.org/3.11/library/sqlite3.html) | 值用占位参数绑定；Connection 上下文提交/回滚但不关闭连接、不隐式打开新事务；check_same_thread 默认 True；3.11 isolation_level 与显式提交/回滚 | verified_at=2026-11-16；不把 Python 3.12 的 autocommit 属性当作 3.11 API，不把 SQLite 的实验当作 PG 隔离/锁证明 |
| P18 | [Python 3.11 venv](https://docs.python.org/3.11/library/venv.html) | 默认 Python 包环境隔离；可直接用环境解释器而不激活；环境含绝对路径、非可搬交付物，目标位置重建 | verified_at=2026-11-16；不证明系统依赖、解释器、秘密和云权限都已隔离/锁定 |
| P21 | [Python 3.11 Built-in Types](https://docs.python.org/3.11/library/stdtypes.html) | 本次返回内容明确支持 list.copy/切片为浅复制；迭代器 StopIteration 后保持耗尽；生成器实现迭代器协议 | verified_at=2026-11-16；返回内容未完整覆盖 dict.copy、集合顺序、含不可哈希成员 tuple 的精确规则，这些不随本行日期视为已核验 |

### FastAPI 与 SQLAlchemy

| 来源 | 实际 URL | 本次明确支持的切面 | 状态与不外推边界 |
|---|---|---|---|
| P06 | [FastAPI Concurrency and async/await](https://fastapi.tiangolo.com/async/) | FastAPI 管理的普通 def 路由/依赖在线程池；直接调用普通工具函数不自动卸载；async 并发与 CPU 并行区别 | verified_at=2026-11-16；不把 async def 的同步阻塞代码说成自动异步，不保证性能或所有第三方库安全 |
| P07 | [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/) | 推荐 lifespan async context manager；yield 前启动、yield 后关闭；提供 lifespan 时旧 startup/shutdown handlers 不同时执行；主应用范围 | verified_at=2026-11-16；不是集群只运行一次，不证明 SIGKILL 会完成清理或本项目已正确优雅关闭 |
| P08 | [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) | 响应后同进程运行；重型/跨进程工作可考虑 Celery 等独立系统 | verified_at=2026-11-16；未承诺持久队列/崩溃恢复；不把文档推荐 Celery 外推为任何配置都可靠 |
| P09 | [SQLAlchemy 2.0 Session Basics — concurrency](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-thread-safe-is-asyncsession-safe-to-share-in-concurrent-tasks) | Session 是可变、有状态的单事务对象；并发模型是 **Session per thread、AsyncSession per task**；上下文管理生命周期 | verified_at=2026-11-16；无片段的页面入口首次抓取失败，本次该节正文成功；不把 engine/pool 复用等同 Session 复用，不给出任意驱动性能结论 |

### PostgreSQL、Redis、队列与对象

| 来源 | 实际 URL | 本次明确支持的切面 | 状态与不外推边界 |
|---|---|---|---|
| P10 | [PostgreSQL 17 Transaction Isolation](https://www.postgresql.org/docs/17/transaction-iso.html) | Read Committed SELECT 以语句开始快照读取；RR/Serializable 的隔离与序列化失败需重试事务；序列计数不随回滚恢复 | verified_at=2026-11-16；不用摘要推导“只读 Serializable 永远不冲突”，不外推 SQLite，不保证外部 HTTP/邮件回滚 |
| P11 | [PostgreSQL 17 Indexes](https://www.postgresql.org/docs/17/indexes.html) | 索引可能加速定位/检索，但给数据库增加开销 | verified_at=2026-11-16；这是章概览，不单凭它证明复合列序、实际计划或具体写入/空间数字 |
| P19 | [PostgreSQL 17 Multicolumn Indexes](https://www.postgresql.org/docs/17/indexes-multicolumn.html) | PG17 B-tree 扫描范围由左侧等值与首个非等值列条件限制；右侧条件可过滤但不据此缩小相同扫描范围；不同索引类型规则不同 | verified_at=2026-11-16；不把“最左前缀”当作所有类型、所有 PG 版本的绝对规则，仍以实际计划为准 |
| P20 | [PostgreSQL 17 Using EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html) | EXPLAIN 显示估计；ANALYZE 实际执行并给实际行数/时间；BUFFERS 查看缓冲访问；写语句会产生修改，可用事务保护表数据实验 | verified_at=2026-11-16；回滚表数据不保证撤销外部触发副作用；cost 非毫秒，测量也有开销 |
| P12 | [Redis Distributed Locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) | SET NX PX 与跨获取唯一随机 token；释放须原子比较 token 后删除；有效期限制与异步复制故障切换互斥风险；明确建议 fencing 且不要假定进程活着就持锁 | verified_at=2026-11-16；token 比较删除不是单调 fencing；不证明任意外部副作用恰好一次，不推荐 Redlock 为普适必须。本包使用概念性 compare-delete，可用文中的 Lua 形式，不要求新版本 DELEX |
| P13 | [Redis EXPIRE](https://redis.io/docs/latest/commands/expire/) | key 的过期、刷新/移除期限，覆盖值与就地修改对 TTL 的不同影响；过期依据时间 | verified_at=2026-11-16；只证明 key 到期机制，不证明 cache-aside 强一致、缓存抖动策略或不存在回填竞态 |
| P14 | [Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html) | 任务应幂等；默认执行前确认；acks_late 在返回后确认但执行子进程异常退出仍可能确认；task_reject_on_worker_lost 的重投边界与风险；retry 沿用 task-id/队列；自动重试可退避/抖动 | verified_at=2026-11-16；ack/retry 不自动业务去重，不承诺 exactly-once；broker 持久化/可见性/配置仍需另外核验，不能把 same task-id 当作数据库唯一效果 |
| P15 | [Amazon S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html) | presigned URL 按签名者权限授权；临时凭证生命周期限制有效期；可重复使用到到期；同 key 上传可覆盖；URL 是 bearer token 应保密 | verified_at=2026-11-16；不证明上传完成等于内容安全/检索就绪；不推导本地文件替身已通过 S3 集成或任意兼容存储语义相同 |

### 流式协议

| 来源 | 实际 URL | 本次明确支持的切面 | 状态与不外推边界 |
|---|---|---|---|
| P22 | [WHATWG HTML Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html) | SSE text/event-stream；id 字段与重连的 Last-Event-ID | verified_at=2026-11-16；本次只核验该协议切面，不把 SSE 视作 Python 执行 checkpoint、持久日志或 exactly-once；应用恢复状态另行设计 |

### 工程底座

| 来源 | 实际 URL | 本次明确支持的切面 | 状态与不外推边界 |
|---|---|---|---|
| P23 | [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/) | `[build-system]` 声明构建依赖；`[project]` 声明名称、版本、描述、依赖与 `requires-python`；`dynamic` 交由后端提供；该规范不定义锁文件，`pylock.toml` 另列 | verified_at=2026-11-16；不证明任意工具都支持所有字段，不覆盖系统库/解释器/构建工具的可复现性 |
| P24 | [pip dependency resolution](https://pip.pypa.io/en/stable/topics/dependency-resolution/) | 使用回溯寻找兼容版本；冲突可报 `ResolutionImpossible`；文档未承诺解析结果跨时间确定 | verified_at=2026-11-16；不据此声称 pip 每次结果不同，也不证明锁工具行为；索引内容与缓存仍需另行控制 |
| P25 | [pylock.toml specification](https://packaging.python.org/en/latest/specifications/pylock-toml/) | 用于“可复现安装”，记录包名、版本与哈希；工具必须支持 wheel | verified_at=2026-11-16；规范支持不等于当前项目已采用或所有工具已成熟；不覆盖系统依赖与运行环境 |
| P26 | [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | fixture 有 function/class/module/package/session 五种作用域；yield 后执行 teardown；每个测试可获得独立结果；autouse 可自动请求 | verified_at=2026-11-16；不证明测试断言有效、异步测试已配置或覆盖率有意义 |
| P27 | [Python 3.11 datetime](https://docs.python.org/3.11/library/datetime.html) | aware 能定位具体时刻，naive 依赖程序解释；naive 与 aware 大小比较抛 `TypeError`、相等为 False；推荐 aware UTC，`utcnow()` 返回 naive；`fromtimestamp(..., tz=UTC)` | verified_at=2026-11-16；不规定数据库列类型、展示时区或夏令时业务策略 |
| P28 | [Python 3.11 time](https://docs.python.org/3.11/library/time.html) | `monotonic()` 不倒退、不受系统时钟更新影响，参考点未定义，只能比较差值；`time()` 在系统时钟回拨后可能小于前一次调用 | verified_at=2026-11-16；不证明单调值可持久化跨进程比较，不替代审计时间或租约的外部时钟协议 |
| P29 | [Python 3.11 decimal](https://docs.python.org/3.11/library/decimal.html) | 十进制数可精确表示，float 的 0.1/0.2 等无精确表示且误差会累积；会计场景偏好 decimal；有有效位、上下文精度/舍入与 `quantize` | verified_at=2026-11-16；不规定币种、最小单位或数据库存储；不声称 Decimal 一定比 float 快 |
| P30 | [Python 3.11 pickle](https://docs.python.org/3.11/library/pickle.html) | 恶意 pickle 可在反序列化时执行任意代码；不要反序列化不可信或可能被篡改的数据；JSON 等格式更安全 | verified_at=2026-11-16；不把 HMAC 签名当作无密钥管理问题的通用方案；不覆盖所有序列化库 |
| P31 | [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | allowlist 是可行方案；动态目标需阻断私有网段与元数据地址（示例 `169.254.169.254`）；解析后校验 IP；禁用或校验重定向；网络分段限制出口 | verified_at=2026-11-16；本次为摘要读取，具体实现、DNS 重绑定细节与云元数据差异仍需按环境核验 |
| P32 | [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | 认证确认身份，授权确认允许的动作；最小权限；默认拒绝；授权必须在服务端执行，客户端检查可绕过 | verified_at=2026-11-16；不定义租户模型、撤权传播或异步任务恢复时的当前授权策略，这些是本包设计 |
| P33 | [Python 3.11 profile](https://docs.python.org/3.11/library/profile.html) | `cProfile` 是确定性 profiler，监控函数调用/返回/异常并记录区间时间；有事件记录开销，不适合当基准；`cProfile` 通常优于纯 Python `profile` | verified_at=2026-11-16；不证明采样 profiler 行为，不把 profile 结果直接外推生产容量 |
| P34 | [Python 3.11 tracemalloc](https://docs.python.org/3.11/library/tracemalloc.html) | 追踪 Python 分配，记录分配 traceback；比较两次快照找增长；快照不含启动前分配；帧数增加会提高开销 | verified_at=2026-11-16；不覆盖 C 扩展默认域之外或全部 RSS；不证明存在泄漏而非缓存增长 |
| P35 | [Python 3.11 unittest.mock](https://docs.python.org/3.11/library/unittest.mock.html) | 用 mock 替换系统部分并断言使用；`patch` 在作用域结束恢复；要 patch 在“被查找”的命名空间；`create=True` 可对不存在 API 造出通过测试 | verified_at=2026-11-16；不规定 pytest fixture 用法，不证明过度 mock 的测试仍然有效 |

## 36 个知识点的证据与设计定位

表中“设计”是本包的教学/工程推导，不冒充已读取文档的标准。来源不足的切面明确指向下方待核验清单；仍可在给定题面下验证机制，但不出“当前版本规定是什么”的事实题。

| ID | 已读取支持 | 设计或仍待核验的切面 |
|---|---|---|
| `py.lang.objects` | P02 对象/容器引用，P21 list 浅复制 | dict.copy 精确切面待 U02；更新路径复制为教学设计 |
| `py.lang.collections` | P21 迭代器耗尽与生成器协议，P02 资源显式管理 | 哈希成员、set 顺序、生成器关闭细节待 U02/U03；不说不可变就一定可哈希 |
| `py.lang.functions` | P03 默认值与参数契约、lambda 外层访问 | 闭包循环晚绑定待 U03 的精确解释 |
| `py.lang.types` | P04 注解与 Protocol | Pydantic 转换/strict 的具体库契约待 U01；授权分离为设计 |
| `py.lang.resources` | P02、P17 with/显式关闭与 sqlite 事务上下文 | 具体资源池关闭顺序由所有权设计，不泛化 with |
| `py.lang.environment` | P18 环境解释器与重建 | 锁文件工具/系统依赖/供应链事实待核验，秘密分离为设计 |
| `py.async.eventloop` | P01 协程/任务/TaskGroup，P06 并发与并行 | 不把异步语法当性能证明 |
| `py.async.cancellation` | P01 取消/timeout/清理与 to_thread 的适用性 | 已运行线程的 cancel 精确契约待 U04；不撤回远端副作用是跨资源边界推导 |
| `py.async.backpressure` | P16 Queue，P01 任务生命周期 | 四层容量预算/拒绝策略为设计 |
| `py.async.execution` | P01、P05、P06 | executor 的取消/进程细节待 U04，容量收益需实际测量 |
| `py.svc.contract` | P04 类型不强制，P06 FastAPI 调用模型 | 输入/响应库契约待 U01；租户授权与错误脱敏为设计，安全检查待 U09 |
| `py.svc.lifecycle` | P07/P08、P09、P17 | readiness/drain/进程级资源预算为设计，部署组件细节待 U08 |
| `py.svc.idempotency` | P10 事务边界，P14 任务幂等要求 | tenant+key+指纹+状态与唯一约束为设计；DDL 精确规则待 U05，外部幂等协议另验 |
| `py.svc.streaming` | P22 协议字段，P01 协作取消 | 持久日志/快照/保留窗口与 checkpoint 为应用契约 |
| `py.data.model` | P17 值参数绑定，P10 事务 | 约束/外键精确规则待 U05；模型与迁移阶段为设计 |
| `py.data.transactions` | P10 PG17、P17 SQLite3.11 | 事务不包含任意网络效果，不把两引擎隔离等同；对账为设计 |
| `py.data.indexes` | P11/P19/P20 | 按负载选择与本地测量，未声称实际 PG 执行过 |
| `py.data.cache` | P12 token/有效期，P13 TTL | cache-aside 回填窗口、抖动/合并回源为设计；模式参考待 U06 |
| `py.data.objects` | P15 presigned | 元数据状态机、扫描/清理/授权为设计；具体 SDK/兼容存储待集成核验 |
| `py.data.retrieval` | P15 对象授权切面，P19 普通数据库索引边界 | 租户/ACL 检索前约束为安全设计；pgvector/近似索引过滤实现待 U07/U09，不称已安装 |
| `py.jobs.delivery` | P14 ack/retry，P08 BackgroundTasks，P16 内存计数 | 简单持久队列与原子效果去重为设计；broker 配置待 U10 |
| `py.jobs.outbox` | P10 事务，P14 重复与幂等边界 | Outbox 同库同事务及发布/标记竞态为设计，参考模式文档待 U11；非 exactly-once |
| `py.jobs.leases` | P12 TTL/误删/fencing 提醒，P01 取消 | generation 原子领取与接收端条件写为设计，不推导外部邮件恰好一次 |
| `py.jobs.scheduling` | P14 退避/抖动 | due_at/周期身份/死信策略为设计，Celery 定时具体规则待 U10 |
| `py.agent.tools` | P04 类型边界，P01 超时与取消 | SDK 无关 schema/只读/授权/审批为设计；校验库具体行为待 U01，安全指南待 U09 |
| `py.agent.runtime` | P01 生命周期、P12 租约提醒、P22 流事件身份 | run/step/checkpoint/审批/未知副作用对账为应用设计，不绑定 SDK |
| `py.agent.evaluation` | P01/P14 给出需注入的故障窗口 | 分层指标/模拟夹具/独立迁移为教学评估设计，不声称行为评测已跑 |
| `py.ops.observability` | P14 重试，P15 bearer token 风险 | 指标/关联身份/脱敏为设计；OpenTelemetry 实现与语义约定待 U08 |
| `py.ops.deployment` | P07 生命周期、P09 会话边界、P18 可复现环境 | 副本连接总预算、readiness/drain/迁移窗口为设计；部署组件待 U08 |
| `py.ops.recovery` | P10 事务/回滚限制、P14 重试边界 | RPO/RTO/备份还原/对象版本对账为运维设计；PG 实际备份流程待 U08 |
| `py.eng.dependencies` | P23 pyproject 声明，P24 解析/冲突，P25 锁与哈希 | 构建一次提升同一 wheel、私有索引凭证、供应链审计为设计；具体锁工具行为待 U12 |
| `py.eng.testing` | P26 fixture 作用域/yield，P35 patch 查找位置与恢复 | 假时钟、异步测试、覆盖率/变异边界为设计；变异与 flaky 策略待 U13 |
| `py.eng.errors` | P01 取消/TaskGroup/超时，P14 重试边界 | 错误分类、重试预算、断路器与期限传播为设计；官方重试协议待 U14 |
| `py.eng.time` | P27 aware/naive，P28 monotonic/墙钟，P29 Decimal | 跨进程期限容差、JSON 编码与币种策略为设计；数据库时间类型待 U05 |
| `py.eng.security` | P30 pickle，P31 SSRF，P32 授权，P17 参数绑定 | 租户来源、当前授权、路径与秘密管理为设计；OWASP 类别清单未完整核验，见 U15 |
| `py.eng.profiling` | P33 cProfile，P34 tracemalloc，P20 EXPLAIN | 采样 profiler、连接池/worker 容量模型为设计；生产负载与压测方法待 U16 |

## 待核验清单（不带 verified_at）

| 项 | 官方候选来源 | 当前状态与需读范围 |
|---|---|---|
| U01 | [Pydantic 2.11 Models](https://docs.pydantic.dev/2.11/concepts/models/)、[实际重定向目标](https://pydantic.dev/docs/validation/2.11/concepts/models/) | **待核验：两种入口（latest 与 2.11）只得到跨主机重定向，目标均返回 403，未读取正文。** BaseModel 输出约束、类型转换/strict 模式不能标已核验；不绑定 Agent SDK |
| U02 | [Python 3.11 Built-in Types — dict](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)、[set](https://docs.python.org/3.11/library/stdtypes.html#set-types-set-frozenset)、[hashable](https://docs.python.org/3.11/glossary.html#term-hashable) | **待核验：** 整页抓取返回未完整含这些子节；dict.copy、键可哈希、set 顺序与 tuple 成员条件需定点读取，不能沿用 P21 日期 |
| U03 | [Python FAQ — loop lambdas](https://docs.python.org/3.11/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result)、[yield expressions](https://docs.python.org/3.11/reference/expressions.html#yield-expressions) | **待核验：未打开。** 晚绑定、暂停/close 与清理的精确契约 |
| U04 | [Python 3.11 concurrent.futures](https://docs.python.org/3.11/library/concurrent.futures.html) | **待核验：未打开。** 已运行 Future.cancel、线程/进程执行器与取消等待区别；不会据缺证据许诺强制停止远端 |
| U05 | [PostgreSQL 17 Constraints](https://www.postgresql.org/docs/17/ddl-constraints.html)、[SQLite foreign keys](https://www.sqlite.org/foreignkeys.html) | **待核验：未打开。** unique/NULL/外键行为及 SQLite 连接级启用边界；简单 demo 不证明生产约束配置 |
| U06 | [Redis client-side caching](https://redis.io/docs/latest/develop/clients/client-side-caching/) | **待核验：未打开。** 仅是候选缓存资料，不将 client-side tracking 与本包 cache-aside 当作同一模式；TTL 原语已有 P13 |
| U07 | [pgvector 项目官方仓库](https://github.com/pgvector/pgvector) | **待核验：未打开。** 扩展版本、近似索引、过滤/迭代扫描与执行计划；若维护时读取 GitHub 用 gh，不自动安装扩展 |
| U08 | [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)、[FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/)、[PostgreSQL 17 backup](https://www.postgresql.org/docs/17/backup.html) | **待核验：未打开。** tracing/metrics SDK、进程部署细节、备份/PITR；恢复方案必须另有真实演练 |
| U09 | [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | **待核验：未打开。** 授权原则已见 P32；对象级授权、撤权传播与多租户验证清单仍需定点读取，不把 P32 的原则当作完整控制集 |
| U10 | [Celery periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)、[Celery configuration](https://docs.celeryq.dev/en/stable/userguide/configuration.html) | **待核验：未打开。** 调度单例/周期、broker/ack/可见性/重投配置；Tasks 页已核验不等于配置全验 |
| U11 | [AWS transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | **待核验：未打开。** 同事务事件意图/重复交付的模式参考，不影响本包“不承诺 exactly-once”的设计边界 |
| U12 | [uv lockfile](https://docs.astral.sh/uv/concepts/projects/lockfile/)、[Poetry lock](https://python-poetry.org/docs/basic-usage/#commit-your-lock-file-to-version-control) | **待核验：未打开。** P25 只覆盖 pylock 规范；具体锁工具的跨平台、可选依赖与哈希行为不据规范外推 |
| U13 | [pytest flaky tests](https://docs.pytest.org/en/stable/how-to/failures.html)、[coverage.py](https://coverage.readthedocs.io/) | **待核验：未打开。** 变异测试与 flaky 重跑策略没有在本轮读取；覆盖率语义只按 P26/通用定义讲解，不冒充已核验 |
| U14 | [urllib3 Retry](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html) | **待核验：未打开。** 退避/重试次数/状态码分类的库契约；本包重试预算与未知结果对账是设计，不称某库官方标准 |
| U15 | [OWASP Top 10](https://top10.owasp.org/) | **待核验：页面只返回版本入口，未列出完整类别。** 不据搜索摘要写“2025 类别清单”；安全题以 P30/P31/P32 的具体切面为准 |
| U16 | [Python 3.11 test](https://docs.python.org/3.11/library/test.html)、[py-spy](https://github.com/benfred/py-spy) | **待核验：未打开。** 采样 profiler、压测工具与生产容量模型；P33/P34 只支持 cProfile/tracemalloc 的切面，不外推采样工具行为 |

访问失败留痕：SQLAlchemy 无片段入口 fetch failed 后 P09 的目标节成功；Redis 旧 `develop/use/patterns/distributed-locks/` 与 `develop/use/keyspace/` 返回 404，改用上方实际成功的官方路径，不把失败页面标 verified。Pydantic latest 目标 `https://pydantic.dev/docs/validation/latest/concepts/models/` 为 403；换固定引用版本仍 403，所以 U01 继续待核验。

## 机制与易变事实更新边界

- 对象共享、取消不代表撤销外部效果、事务范围、重复交付、fencing 的接收端边界等进入稳定机制。任务/事件字段和库选型是建议，不是普适规定。
- Python 构建/扩展兼容性、FastAPI 生命周期 API、Pydantic 转换规则、Celery/broker 配置、PG 索引优化、对象存储权限限制等作为版本化事实。出版本题先读目标版本官方资料，超过 14 天或不确定就即时重验；不以发布日期猜 API 行为。
- 只更新实际重新读取切面的日期。待核验来源不可通过“同域名”“目录里有链接”“搜索摘要”批量升格；失败就保留原因并收窄题目。
- 学习者答题、模型评测、SQLite 本地实验和生产集成各自记录证据。未运行不写“实测/通过”；不会为了更新公共来源修改个人成绩或迁移旧 ID。
