# Go 后端知识图谱

本图只发布通用知识，不包含任何学习者的档位、错答或复习日期。稳定ID与依赖的维护源见[领域图谱](../../skills/knowledge-interviewer/references/domains/go-backend/map.md)。个人记录保存在忽略目录 `.local/learning/serve/`。

按值与错误 → 并发与生命周期 → 服务边界 → 数据一致性 → 可观测 → Agent后端阅读；第0章用于建立从TS到Go的语义前提。

| ID | 层级 | 名称 | 核心考点 | 常见误解 |
|---|---|---|---|---|
| `go.lang.value` | L0 | 值语义与零值 | struct 赋值为什么是拷贝；slice 的 ptr/len/cap 三字段；`append` 何时复用底层数组；nil map 写为什么 panic、nil slice 为什么能 append | 用 TS 的引用模型理解赋值；认为「指向同一数组」就一定会被 append 改到；把 nil 当成一个统一的值 |
| `go.lang.error` | L0 | 错误作为返回值 | 错误为什么是值不是异常；`%w` 与 `errors.Is/As` 分别解决什么；错误该在哪一层打日志 | 用 panic/recover 做业务错误；包装时用 `%v` 丢链；每层都打一遍日志 |
| `go.lang.interface` | L0 | 接口与 nil | 隐式实现的方法集；**typed nil ≠ nil** 的机制；接口该定义在消费方还是提供方 | 认为 `var p *T = nil` 传给接口后 `err != nil` 判得住；接口越大越抽象越好 |
| `go.conc.goroutine` | L1 | goroutine 的代价 | 初始栈多大、为什么阻塞的 goroutine 仍占内存；泄漏怎么观测；为什么必须有退出条件 | 认为 `go f()` 和 `Promise.resolve` 一样轻；认为阻塞在 channel 上不占资源 |
| `go.conc.context` | L1 | context 生命周期 | 取消如何沿调用链传播；为什么 DB/HTTP/RPC 都要收 ctx；`WithValue` 该放什么 | 只在 handler 设超时，下游用 `context.Background()`；把业务参数塞进 ctx |
| `go.conc.race` | L1 | 数据竞争 | map 并发写为什么是 fatal 而不是 panic 可恢复；`-race` 能测出什么、测不出什么 | 认为「没崩就是没竞争」；认为加锁一定慢、不加锁靠运气 |
| `go.conc.backpressure` | L1 | 背压与并发上限 | 队列为什么必须有界；满了拒绝还是阻塞；worker 数、信号量、连接池、队列长度四个上限从哪来 | 认为加机器能解决无限并发；用无界 channel 当缓冲 |
| `go.svc.timeout` | L2 | 超时预算 | 每层超时如何相加；`http.Server`/`http.Client` 零值意味着什么；为什么网关 504 不等于有超时 | 认为设了 504 就有超时；每层各设一个拍脑袋的值，不做预算 |
| `go.svc.pool` | L2 | 连接池与排队 | `maxOpen × 副本数 ≤ DB max_connections`；池满时请求去哪；为什么池越大不一定越快 | 认为连接池越大吞吐越高；忽略副本数导致总连接打满 |
| `go.svc.idempotency` | L2 | 幂等 | 超时为什么不等于没执行；幂等键、请求指纹、处理中状态怎么配合；不可逆动作重试前先查什么 | 认为重试是安全的默认动作；只用「查一下有没有」而不加唯一约束，仍有并发窗口 |
| `go.svc.shutdown` | L2 | 优雅关闭 | readiness 摘流量、等在途、关依赖的顺序；K8s grace period 和 preStop 怎么配 | 收到 SIGTERM 直接退出；先关 DB 再等在途请求 |
| `go.data.tx` | L2 | 事务边界 | 为什么一个业务动作一个事务；事务内为什么不能调网络；长事务持锁与 WAL 增长的代价 | 认为「包在事务里就安全」，包括外部调用；事务里做批量导入、逐条提交 |
| `go.data.index` | L2 | 查询与索引 | 索引是否生效只由 `EXPLAIN (ANALYZE, BUFFERS)` 回答；最左前缀；索引列上做函数为什么失效 | 认为加了索引就一定走；只看 `EXPLAIN` 不看 ANALYZE/BUFFERS |
| `go.data.consistency` | L3 | 至少一次与最终一致 | 至少一次 + 幂等消费 = 事实上的恰好一次；Outbox 为什么必须同库同事务；对账兜底 | 认为「发了消息就一定被处理一次」；业务提交成功后再发消息，丢了没人知道 |
| `go.obs.log` | L3 | 结构化日志 | 关键节点打哪几条；request_id/trace_id/tenant_id 的作用；为什么错误只打一次 | 认为日志越多越好；靠 grep 两百万行破案；每层都打一遍错误 |
| `go.obs.trace` | L3 | 指标与追踪 | RED/USE 各自回答什么；为什么看 P95/P99 不看均值；trace 怎么串起依赖与工具调用 | 认为有监控大盘就等于可归因；只看平均延迟 |
| `go.obs.slo` | L3 | SLO 与告警 | SLI 怎么定义；错误预算怎么算；为什么按 burn rate 告警而不是瞬时错误率 | 认为告警越多越安全；CPU 80% 但 P95 正常也叫醒人 |
| `go.agent.gateway` | L4 | LLM Gateway | 多供应商抽象；SSE 的首 token 分界线；为什么首 token 后不能 failover；usage 缺失怎么计费；租户 RPM/TPM/配额 | 认为流式响应可以随便重试；只按客户端上报计费 |
| `go.agent.runtime` | L4 | 持久化任务运行时 | 状态机落库；租约/心跳接管失联 worker；checkpoint/resume；审批是持久化状态；Outbox 通知 | 认为内存 map 就是任务状态；把审批做成一次弹窗 |

## 跨卷连接

[前端图谱](../frontend/knowledge-map.md)将任务恢复、工具副作用、授权与评测连接到浏览器状态、审批和用户旅程。各领域各自记录学习状态，不因读过另一卷就自动判掌握。

## 自检与陪练

从[本卷目录](README.md)进入正文，每次用一个知识点的判据验证理解。需要陪练时使用[knowledge-interviewer](../../skills/knowledge-interviewer/SKILL.md)，初次运行 `python3 skills/knowledge-interviewer/scripts/learning_state.py init` 生成本地空白档案；成绩和错题不写回本图。

## 36 项自检（0 / 1 / 2 分，满分 72）

0 = 没做过；1 = 跟教程做过；2 = 能独立设计、排障、讲清取舍。

**A. Go 语言与并发（8 项，16 分）**
- [ ] 能用接口解耦外部依赖并写 fake
- [ ] 错误链可追溯（`%w` / `errors.Is` / `errors.As`）
- [ ] 能解释 slice/map/string 的底层行为
- [ ] 能写 worker pool 并限制并发
- [ ] 能用 context 做全链路取消与超时
- [ ] 能定位 goroutine 泄漏与数据竞争
- [ ] 能读 pprof（CPU/heap/block/mutex）
- [ ] 单测 + `-race` + 基准测试是习惯

**B. API 与服务（6 项，12 分）**
- [ ] 统一错误模型与错误码
- [ ] 输入校验、分页上限、幂等键
- [ ] JWT/OIDC + RBAC
- [ ] 优雅关闭与健康检查
- [ ] OpenAPI/契约测试
- [ ] 结构化日志带 request_id/tenant_id

**C. 数据与一致性（6 项，12 分）**
- [ ] 能设计表并解释范式取舍
- [ ] 事务与隔离级别能讲清
- [ ] 会用 EXPLAIN 定位慢查询
- [ ] 迁移可回滚、可重复执行
- [ ] Redis 缓存三问题有方案
- [ ] 幂等 + 去重 + Outbox 能落地

**D. 稳定性与可观测（5 项，10 分）**
- [ ] RED/USE 指标与看板
- [ ] OTel trace 能串起一次 Agent 调用
- [ ] 超时/重试/熔断/降级有边界
- [ ] 能写 SLO 与告警规则
- [ ] 能做故障注入与无责复盘

**E. 部署与安全（5 项，10 分）**
- [ ] Docker 多阶段 + 非 root
- [ ] K8s Deployment/Probe/HPA/Secret
- [ ] CI/CD 自动到预发
- [ ] SSRF/注入/密钥/多租户有基线
- [ ] 工具执行有沙箱与审计

**F. Agent 后端（6 项，12 分）**
- [ ] 多供应商 + SSE + 故障转移
- [ ] token 计费与租户配额
- [ ] 工具注册表 + schema 校验
- [ ] 长任务 checkpoint/resume
- [ ] 评测服务（数据集/断言/回归）
- [ ] Agent 可观测（step/tool/token/成本）

分档：0–24 基础缺口明显（先 L0–L1）｜25–48 能写服务扛不住生产（主攻第 2–3 章）｜
49–60 能独立交付生产服务（补第 4–6 章）｜61–72 可负责 Agent 平台后端（做架构与团队影响）。

**按板块看短板比看总分有用。** 任何板块得分率 < 50% 就是本轮主攻方向。
