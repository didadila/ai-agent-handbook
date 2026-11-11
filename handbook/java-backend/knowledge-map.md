# Java知识点与依赖

依赖主线：运行时数据区 → 对象与可达性 → 收集器与诊断；JMM → happens-before → volatile/锁 → 容器与线程池；索引结构 → 执行计划 → 事务/MVCC/锁；本地事务 → 消息交付 → 幂等与分布式恢复。

## [JVM与运行时](01-JVM与运行时.md)

- `jvm.memory.areas`：运行时数据区
- `jvm.memory.stack`：栈帧结构
- `jvm.object.layout`：对象内存布局
- `jvm.gc.reachability`：可达性分析
- `jvm.gc.generational`：分代假说
- `jvm.gc.algorithms`：标记-清除/复制/整理
- `jvm.gc.stw`：STW 与安全点
- `jvm.gc.cms`：CMS
- `jvm.gc.g1`：G1
- `jvm.gc.crossgen`：跨代引用
- `jvm.classload.process`：加载流程
- `jvm.classload.parent`：双亲委派
- `jvm.tuning.oom`：OOM 排查

## [并发与资源生命周期](02-并发与资源生命周期.md)

- `conc.jmm.model`：Java 内存模型
- `conc.jmm.happensbefore`：happens-before
- `conc.volatile`：volatile
- `conc.thread.state`：线程状态
- `conc.sync.upgrade`：synchronized 锁升级
- `conc.cas.problems`：CAS
- `conc.aqs`：AQS
- `conc.lock.compare`：ReentrantLock vs synchronized
- `conc.threadlocal`：ThreadLocal
- `conc.chm`：ConcurrentHashMap
- `conc.threadpool.params`：线程池七参数
- `conc.threadpool.sizing`：线程池调参
- `conc.tools`：并发工具类

## [MySQL与事务](03-MySQL与事务.md)

- `mysql.index.bplustree`：B+ 树
- `mysql.index.clustered`：聚簇索引
- `mysql.index.covering`：覆盖索引与最左前缀
- `mysql.index.failure`：索引失效
- `mysql.tx.isolation`：隔离级别
- `mysql.tx.mvcc`：MVCC
- `mysql.lock.types`：锁类型
- `mysql.lock.deadlock`：死锁
- `mysql.log.redo`：redo/undo/binlog
- `mysql.explain`：执行计划
- `mysql.slowquery`：慢查询优化
- `mysql.sharding`：分库分表

## [Redis与缓存](04-Redis与缓存.md)

- `redis.ds.impl`：底层数据结构
- `redis.thread.model`：单线程模型
- `redis.persist`：持久化
- `redis.expire`：过期与淘汰
- `redis.cache.problems`：缓存三问题
- `redis.cache.consistency`：双写一致性
- `redis.lock`：分布式锁
- `redis.cluster`：集群

## [Spring与事务边界](05-Spring与事务边界.md)

- `spring.ioc.lifecycle`：Bean 生命周期
- `spring.ioc.circular`：循环依赖
- `spring.aop.proxy`：AOP
- `spring.tx.propagation`：事务传播
- `spring.tx.failure`：事务失效场景
- `spring.boot.autoconfig`：自动配置

## [消息与异步交付](06-消息与异步交付.md)

- `mq.usecase`：为什么用 MQ
- `mq.reliability`：不丢消息
- `mq.idempotent`：重复消费
- `mq.order`：顺序消息
- `mq.backlog`：积压处理

## [分布式与系统设计](07-分布式与系统设计.md)

- `dist.cap`：CAP与故障条件
- `dist.idgen`：分布式ID
- `dist.tx`：分布式事务
- `dist.consensus`：一致性协议
- `dist.limiting`：限流熔断降级
- `sys.design.estimate`：容量估算
- `sys.design.case`：综合设计


稳定ID与判据以[陪练图谱](../../skills/knowledge-interviewer/references/domains/java-backend/map.md)为准。跨卷入口：[Go](../go-backend/knowledge-map.md) · [Agent](../ai-agent/knowledge-map.md) · [前端](../frontend/knowledge-map.md)。
