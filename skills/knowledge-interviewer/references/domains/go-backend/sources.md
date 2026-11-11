# Go领域来源与版本边界

verified_at: 2026-11-10

2026-11-10准确性补充：[Go Memory Model](https://go.dev/ref/mem)明确数据竞争的冲突位置、读写种类和happens-before条件；两个只读访问不能因没有锁就判为竞争。同步来源包括goroutine启动等规范关系，不仅是显式互斥锁。

2026-11-10版本入口复查：[Go发布历史](https://go.dev/doc/devel/release)已列Go1.27主版本，教学中不能把本机Go1.26工具链称为最新版。稳定语言机制仍按明确目标版本判断，不要求只为追新而改写示例。

Go语言机制以官方规范为准；连接池、HTTP与context按所用工具链API核对。数据库示例区分PostgreSQL与MySQL，EXPLAIN ANALYZE会实际执行查询，生产写语句不可直接照搬。跨资源的幂等、补偿与授权仍由应用实现，不宣称库自动提供恰好一次。

|覆盖ID|主要来源|
|---|---|
|go.lang.value、go.lang.interface、go.lang.error|[Go规范](https://go.dev/ref/spec) · [Effective Go](https://go.dev/doc/effective_go)|
|go.lang.error|[errors包与错误树](https://pkg.go.dev/errors)，2026-11-10复核；含Is/As/Unwrap，不靠错误字符串判断身份。|
|go.conc.goroutine、go.conc.context、go.conc.backpressure|[context](https://pkg.go.dev/context) · [诊断](https://go.dev/doc/diagnostics)|
|go.conc.race|[Race detector](https://go.dev/doc/articles/race_detector)|
|go.svc.timeout、go.svc.shutdown、go.agent.gateway|[net/http](https://pkg.go.dev/net/http)|
|go.svc.pool、go.data.tx|[database/sql](https://pkg.go.dev/database/sql) · [事务](https://go.dev/doc/database/execute-transactions)|
|go.data.index|[PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)|
|go.svc.idempotency、go.data.consistency、go.agent.runtime|[事务边界](https://go.dev/doc/database/execute-transactions) · [Agent工程来源](../ai-agent/sources.md)|
|go.obs.log|[log/slog](https://pkg.go.dev/log/slog)|
|go.obs.trace|[Go诊断](https://go.dev/doc/diagnostics) · [Agent可观测来源](../ai-agent/sources.md)|
|go.obs.slo|[SRE错误预算告警](https://sre.google/workbook/alerting-on-slos/)|

上述映射提供机制入口，不证明每个业务架构的适用性。索引有无收益取决于执行计划、数据分布和负载；“至少一次+幂等”仅能在明确去重范围、持久状态和失败边界内保证业务效果，不等价于跨所有资源的原子交付。
