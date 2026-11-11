# 领域包：go-backend — 知识图谱

跨领域应用：客户端的任务状态、SSE 续流与审批交互见[frontend 图谱](../frontend/map.md)。服务端负责权威状态、业务幂等与授权；前端负责正确投影和交互，两域分开判档。

覆盖Go后端19个稳定点：值与错误、并发与生命周期、服务边界、数据与一致性、可观测性、Agent后端。题库questions.md逐点覆盖，变体按references/question-design.md设计。版本边界见sources.md，更新流程见maintenance.md。

按依赖排序。**L0 是语言前提，L1 是并发，L2 是服务与数据，L3 是可观测，L4 是 Agent 后端。** 跳级出题会让用户只能背书——没搞懂 slice 的 cap，问「为什么 append 改到了调用方的数据」只能得到「共享底层数组」这句半对的话。

每个知识点带稳定 ID，写状态文件时用这个 ID，不要用中文名（中文名可能被改写，ID 不会）。

「常见误解」一栏是出题时的靶子：如果用户的回答命中了这些，说明他停在了一个具体的错误模型上，值得针对性追问。

这个图谱的阅读版在 `handbook/go-backend/`，规则版在 `go-backend-expert` skill。三处不重复：图谱管考什么，小册管为什么，skill 管写代码时怎么判。

---

## 0. 语言前提（L0）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `go.lang.value` | L0 | 值语义与零值 | struct 赋值为什么是拷贝；slice 的 ptr/len/cap 三字段；`append` 何时复用底层数组；nil map 写为什么 panic、nil slice 为什么能 append | 用 TS 的引用模型理解赋值；认为「指向同一数组」就一定会被 append 改到；把 nil 当成一个统一的值 |
| `go.lang.error` | L0 | 错误作为返回值 | 错误为什么是值不是异常；`%w` 与 `errors.Is/As` 分别解决什么；错误该在哪一层打日志 | 用 panic/recover 做业务错误；包装时用 `%v` 丢链；每层都打一遍日志 |
| `go.lang.interface` | L0 | 接口与 nil | 隐式实现的方法集；**typed nil ≠ nil** 的机制；接口该定义在消费方还是提供方 | 认为 `var p *T = nil` 传给接口后 `err != nil` 判得住；接口越大越抽象越好 |

## 1. 并发与生命周期（L1）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `go.conc.goroutine` | L1 | goroutine 的代价 | 初始栈多大、为什么阻塞的 goroutine 仍占内存；泄漏怎么观测；为什么必须有退出条件 | 认为 `go f()` 和 `Promise.resolve` 一样轻；认为阻塞在 channel 上不占资源 |
| `go.conc.context` | L1 | context 生命周期 | 取消如何沿调用链传播；为什么 DB/HTTP/RPC 都要收 ctx；`WithValue` 该放什么 | 只在 handler 设超时，下游用 `context.Background()`；把业务参数塞进 ctx |
| `go.conc.race` | L1 | 数据竞争 | map 并发写为什么是 fatal 而不是 panic 可恢复；`-race` 能测出什么、测不出什么 | 认为「没崩就是没竞争」；认为加锁一定慢、不加锁靠运气 |
| `go.conc.backpressure` | L1 | 背压与并发上限 | 队列为什么必须有界；满了拒绝还是阻塞；worker 数、信号量、连接池、队列长度四个上限从哪来 | 认为加机器能解决无限并发；用无界 channel 当缓冲 |

## 2. 服务边界（L2）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `go.svc.timeout` | L2 | 超时预算 | 每层超时如何相加；`http.Server`/`http.Client` 零值意味着什么；为什么网关 504 不等于有超时 | 认为设了 504 就有超时；每层各设一个拍脑袋的值，不做预算 |
| `go.svc.pool` | L2 | 连接池与排队 | `maxOpen × 副本数 ≤ DB max_connections`；池满时请求去哪；为什么池越大不一定越快 | 认为连接池越大吞吐越高；忽略副本数导致总连接打满 |
| `go.svc.idempotency` | L2 | 幂等 | 超时为什么不等于没执行；幂等键、请求指纹、处理中状态怎么配合；不可逆动作重试前先查什么 | 认为重试是安全的默认动作；只用「查一下有没有」而不加唯一约束，仍有并发窗口 |
| `go.svc.shutdown` | L2 | 优雅关闭 | readiness 摘流量、等在途、关依赖的顺序；K8s grace period 和 preStop 怎么配 | 收到 SIGTERM 直接退出；先关 DB 再等在途请求 |

## 3. 数据与一致性（L2→L3）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `go.data.tx` | L2 | 事务边界 | 为什么一个业务动作一个事务；事务内网络调用为何增加持锁与跨资源一致性风险；长事务持锁与 WAL 增长的代价 | 认为「包在事务里就安全」，包括外部调用；事务里做批量导入、逐条提交 |
| `go.data.index` | L2 | 查询与索引 | 结合数据库类型、数据分布与实际执行计划判断索引收益；ANALYZE会执行语句；表达式索引的边界 | 认为加了索引就一定走；只看 `EXPLAIN` 不看 ANALYZE/BUFFERS |
| `go.data.consistency` | L3 | 至少一次与最终一致 | 至少一次交付与明确去重边界内的业务效果幂等；Outbox 为什么必须同库同事务；对账兜底 | 认为「发了消息就一定被处理一次」；业务提交成功后再发消息，丢了没人知道 |

## 4. 可观测性（L3）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `go.obs.log` | L3 | 结构化日志 | 关键节点打哪几条；request_id/trace_id/tenant_id 的作用；为什么错误只打一次 | 认为日志越多越好；靠 grep 两百万行破案；每层都打一遍错误 |
| `go.obs.trace` | L3 | 指标与追踪 | RED/USE 各自回答什么；为什么看 P95/P99 不看均值；trace 怎么串起依赖与工具调用 | 认为有监控大盘就等于可归因；只看平均延迟 |
| `go.obs.slo` | L3 | SLO 与告警 | SLI 怎么定义；错误预算怎么算；为什么按 burn rate 告警而不是瞬时错误率 | 认为告警越多越安全；CPU 80% 但 P95 正常也叫醒人 |

## 5. Agent 平台后端（L4）

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `go.agent.gateway` | L4 | LLM Gateway | 多供应商抽象；SSE 的首 token 分界线；为什么未定义修订/重放协议时首 token 后不能透明failover；usage 缺失怎么计费；租户 RPM/TPM/配额 | 认为流式响应可以随便重试；只按客户端上报计费 |
| `go.agent.runtime` | L4 | 持久化任务运行时 | 状态机落库；租约/心跳接管失联 worker；checkpoint/resume；审批是持久化状态；Outbox 通知 | 认为内存 map 就是任务状态；把审批做成一次弹窗 |

---

## 依赖链条

```
go.lang.value ─┬─→ go.conc.race
               ├─→ go.data.tx
               └─→ go.svc.idempotency（请求指纹与去重记录）
go.lang.error ─┬─→ go.svc.idempotency（超时错误 ≠ 失败）
               └─→ go.obs.log
go.lang.interface ─→ go.agent.gateway / go.data.tx
go.conc.context ─┬─→ go.svc.timeout
                 ├─→ go.svc.pool
                 └─→ go.agent.runtime（取消与恢复）
go.conc.backpressure ─→ go.svc.pool ─→ go.agent.gateway
go.data.consistency ─→ go.agent.runtime
go.obs.trace ─→ go.obs.slo ─→ go.agent.gateway / runtime
```

## 组题建议

**一次会话的合理配比**：到期复习 2–3 题 + 同一模块内相邻知识点 2–3 题 + 一个 L4 设计评审题。

**不要在一次会话里横跨 5 个模块。** 服务后端的知识链条是「值 → 并发 → 边界 → 数据 → 归因」，
跳着问只能测出零散记忆。

**首次定位的三题建议**：

1. `go.lang.value`（L0）：给一段 `all[:2]` 后 append 的代码，问调用方数据会不会被改，以及为什么。测的是**值/描述符模型**，不是语法。
2. `go.svc.idempotency`（L2）：下游超时后重试，会不会重复扣款？怎么保证？测的是**失败语义与边界设计**。
3. `go.agent.runtime`（L4）：进程被 kill -9 后，正在执行的任务会怎样？测的是**状态落库与恢复**，能直接区分「写过 demo」和「上过生产」。

三题里第 1 题答错，先补 L0，不要继续问 L2；第 2 题答不出唯一约束，说明幂等只停在概念；第 3 题答「重启后重新跑」就追问「已经发出的外部副作用怎么办」。

## 判档提示

- **A**：能说出机制、能给出约束条件、能指出反例与失败模式。
- **B**：结论对，但问「谁在保证」时开始含糊，或只能给一种方案。
- **C**：命中了图谱里的常见误解，结论半对、机制错。
- **D**：不知道，或答案停留在「加锁/加重试/加机器」这类动作名。
