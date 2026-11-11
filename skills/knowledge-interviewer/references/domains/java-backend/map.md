# 领域包：java-backend — 知识图谱

64个稳定ID全部保留。正文见[Java卷](../../../../../handbook/java-backend/README.md)，题库逐点覆盖，版本与来源见[sources.md](sources.md)。个人成绩只存本地忽略目录，不进入图谱。

| ID | 层级 | 名称 | 该考什么 | 常见误解 |
|---|---|---|---|---|
| `jvm.memory.areas` | L1 | 运行时数据区 | 此故障应先检查线程栈还是扩大Java堆？ | 认为「基本类型存栈，对象存堆」（忽略逃逸分析和对象头） |
| `jvm.memory.stack` | L1 | 栈帧结构 | 为什么加大堆不能直接修复这里的栈溢出？ | 把栈溢出和堆溢出混为一谈 |
| `jvm.object.layout` | L2 | 对象内存布局 | 比较对象大小前先固定哪一类运行条件？ | 不知道 Mark Word 是锁升级的存储位置 |
| `jvm.gc.reachability` | L2 | 可达性分析 | 什么引用证据能解释该缓存仍不能回收？ | 说 Java 用引用计数 |
| `jvm.gc.generational` | L2 | 分代假说 | 为什么不能把8:1:1当作所有收集器的标准比例？ | 认为「大对象直接进老年代」是唯一晋升路径 |
| `jvm.gc.algorithms` | L2 | 标记-清除/复制/整理 | 高存活率为什么会放大复制成本？ | 只能背名字，说不出为什么新生代用复制算法不浪费 |
| `jvm.gc.stw` | L2 | STW 与安全点 | 应先把这次延迟拆成哪两类时间？ | 认为 GC 全程都 STW |
| `jvm.gc.cms` | L2 | CMS（历史） | 在Java21上能否把切到CMS作为调优方案？ | 认为 CMS 全程不停顿 |
| `jvm.gc.g1` | L2 | G1 | 为什么目标停顿值不等于绝不会超过的上限？ | 认为 G1 取消了分代 |
| `jvm.gc.crossgen` | L2 | 跨代引用 | 只扫描年轻代内部为什么可能漏掉存活对象？ | 完全没意识到这个问题存在 |
| `jvm.classload.process` | L2 | 加载流程 | 默认零值赋予与初始化代码执行分别属于同一阶段吗？ | 混淆准备阶段和初始化阶段 |
| `jvm.classload.parent` | L2 | 双亲委派 | 为什么同名类仍可能不能互相转换？ | 只会背三层加载器名字 |
| `jvm.tuning.oom` | L2 | OOM 排查 | 为什么单看Java堆曲线不能排除进程内存问题？ | 一律建议「加大堆」 |
| `conc.jmm.model` | L1 | Java 内存模型 | 这里应寻找哪一类跨线程同步关系？ | 把 JMM 和 JVM 内存区域搞混 |
| `conc.jmm.happensbefore` | L2 | happens-before | 日志上的时间先后能否单独证明可见性？ | 以为是「时间上先发生」 |
| `conc.volatile` | L2 | volatile | volatile为什么不能独立保证这次计数准确？ | 认为 volatile 保证原子性 |
| `conc.thread.state` | L2 | 线程状态 | 持锁线程执行sleep后，另一线程能因此获得该监视器吗？ | 说不清 `WAITING` 和 `TIMED_WAITING` 靠什么区分 |
| `conc.sync.upgrade` | L2 | synchronized 锁升级 | 为什么旧版四级锁图不能作为Java21的必经路径？ | 认为 synchronized 永远是重量级锁（JDK 5 时代的知识） |
| `conc.cas.problems` | L2 | CAS | 竞争加剧时CAS会把成本转移到哪里？ | 认为 CAS 无锁所以一定更快 |
| `conc.aqs` | L2 | AQS | AQS中的state由框架统一解释还是同步器定义？ | 说不出 AQS 到底存了什么状态 |
| `conc.lock.compare` | L2 | ReentrantLock vs synchronized | 这类请求需要哪一种获取锁的能力？ | 无脑推荐 ReentrantLock |
| `conc.threadlocal` | L2 | ThreadLocal | 哪个生命周期边界必须清理当前请求的ThreadLocal？ | 认为 key 弱引用就不会泄漏（漏了 value） |
| `conc.chm` | L2 | ConcurrentHashMap | 为什么get后put仍有竞态窗口？ | 停留在分段锁的答案 |
| `conc.threadpool.params` | L2 | 线程池七参数 | 无界队列为什么可能使最大线程数配置失去预期作用？ | 认为「核心满了就立刻加线程」 |
| `conc.threadpool.sizing` | L2 | 线程池调参 | 设置线程数时为什么必须考虑下游连接上限？ | 只会背 `2N+1` 不知道为什么 |
| `conc.tools` | L2 | 并发工具类 | 限制同时访问下游的数量应由哪类工具表达？ | 分不清前两个 |
| `mysql.index.bplustree` | L2 | B+ 树 | 主键变宽为何可能增加索引读取成本？ | 只说「B+ 树查询快」 |
| `mysql.index.clustered` | L2 | 聚簇索引 | 这次索引命中后仍访问聚簇记录的原因是什么？ | 不知道二级索引叶子存的是主键值 |
| `mysql.index.covering` | L2 | 覆盖索引与最左前缀 | 能扫描索引是否等于能按b快速定位少量记录？ | 背规则但说不出跟 B+ 树有序性的关系 |
| `mysql.index.failure` | L2 | 索引失效 | 只看SQL里出现OR能否判定索引一定不用？ | 只会列清单 |
| `mysql.tx.isolation` | L2 | 隔离级别 | 两次读取差异为什么不能仅用RR三个字否定？ | 分不清不可重复读和幻读 |
| `mysql.tx.mvcc` | L2 | MVCC | 为什么只用行事务ID小于当前事务ID会误判可见性？ | 只说「快照读」，讲不出 ReadView 判断规则 |
| `mysql.lock.types` | L2 | 锁类型 | 结果为空为什么不能推出没有任何锁范围？ | 认为 RR 靠 MVCC 完全解决了幻读（漏了当前读） |
| `mysql.lock.deadlock` | L2 | 死锁 | 为什么只重试事务中最后一条SQL可能不正确？ | 只知道「加锁顺序一致」这一条 |
| `mysql.log.redo` | L2 | redo/undo/binlog | redo存在为什么不等于不再需要binlog？ | 混淆 redo 和 binlog 的职责 |
| `mysql.explain` | L2 | 执行计划 | 为什么只看key列非空不能证明查询成本很低？ | 只看 `key` 有没有值 |
| `mysql.slowquery` | L2 | 慢查询优化 | 游标分页为什么需要稳定且可区分记录的排序条件？ | 一律建议加索引 |
| `mysql.sharding` | L2 | 分库分表 | 为什么分片前必须先定位单库瓶颈？ | 认为分表是性能问题的第一解法 |
| `redis.ds.impl` | L2 | 底层数据结构 | 为什么不能只根据zset类型名估算所有规模的内存？ | 只知道五种对外数据类型 |
| `redis.thread.model` | L2 | 单线程模型 | 为什么增加网络I/O并行不一定解除慢命令阻塞？ | 认为 6.0 之后命令也并行执行了 |
| `redis.persist` | L2 | 持久化 | AOF已开启为什么仍可能丢最近写入？ | 认为开了 AOF 就绝对不丢 |
| `redis.expire` | L2 | 过期与淘汰 | TTL到期为什么不等于立即完成所有内存回收？ | 认为过期就立刻被删 |
| `redis.cache.problems` | L2 | 缓存三问题 | 这个随机不存在ID场景首先对应哪一类故障？ | 三个概念互相说反 |
| `redis.cache.consistency` | L2 | 双写一致性 | 为什么延迟双删不能独立证明强一致？ | 认为延迟双删能保证强一致 |
| `redis.lock` | L2 | 分布式锁 | 防误删token为什么不能阻止过期持有者写入？ | 认为 `SETNX` + 过期时间就完事了 |
| `redis.cluster` | L2 | 集群 | 为什么有副本和自动切换仍不等于零丢失？ | 说不清主从复制的全量/增量切换条件 |
| `spring.ioc.lifecycle` | L2 | Bean 生命周期 | 为什么构造完成不能证明整个Bean已经可对外服务？ | 顺序说不全或说反 |
| `spring.ioc.circular` | L2 | 循环依赖 | 三级缓存为什么不能通用解决构造器循环依赖？ | 说三级缓存但讲不出第三级存 ObjectFactory 的原因（AOP 代理） |
| `spring.aop.proxy` | L2 | AOP | 这次调用在哪个位置绕开了代理？ | 不知道自调用失效这个坑 |
| `spring.tx.propagation` | L2 | 事务传播 | 外层回滚为什么不能自动撤销独立新事务？ | 分不清 `REQUIRES_NEW` 和 `NESTED` |
| `spring.tx.failure` | L2 | 事务失效场景 | 在判断回滚规则前应先验证哪一个调用边界？ | 只知道最后一条 |
| `spring.boot.autoconfig` | L2 | 自动配置 | 依赖在类路径上为什么仍不保证默认Bean生效？ | 说不出条件装配的执行时机 |
| `mq.usecase` | L2 | 为什么用 MQ | 为什么入队成功不能直接显示业务已完成？ | 只说优点不说代价 |
| `mq.reliability` | L2 | 不丢消息 | 消费者提交业务后未ack，恢复时应防哪类问题？ | 只覆盖其中一段 |
| `mq.idempotent` | L2 | 重复消费 | 为什么先查去重表再更新业务仍可能重复？ | 认为 MQ 能提供 exactly-once |
| `mq.order` | L2 | 顺序消息 | 本地加一把锁为什么不能证明跨分区全局顺序？ | 认为加锁就能保证顺序 |
| `mq.backlog` | L2 | 积压处理 | 下游已饱和时为什么扩消费者会放大排队？ | 只会说「加机器」 |
| `dist.cap` | L3 | CAP / BASE | 这组分区条件下两个要求为何不能同时兑现？ | 认为可以「三选二」自由选 |
| `dist.idgen` | L3 | 分布式 ID | 时钟回拨时继续沿用旧时间与序列为何危险？ | 不知道 UUID 做主键对聚簇索引的伤害 |
| `dist.tx` | L3 | 分布式事务 | 为什么数据库回滚不能撤销已完成的外部扣款？ | 认为 2PC 是通用解 |
| `dist.consensus` | L3 | 一致性协议 | 为什么自认为leader不足以证明可以提交新写入？ | 把 Raft 和 2PC 混为一谈 |
| `dist.limiting` | L3 | 限流熔断降级 | 依赖已大量超时，应先用哪类机制阻止持续施压？ | 分不清限流和熔断 |
| `sys.design.estimate` | L3 | 容量估算 | 缺少对象大小时为什么无法直接估算存储容量？ | 完全不做量级估算就上架构 |
| `sys.design.case` | L3 | 综合设计 | 对这个系统应先写出哪一条可检查的业务不变量？ | 只画框图不谈数据量和失败路径 |

## 版本边界

- CMS和偏向锁相关ID是兼容入口，不能用旧路径判Java21机制的对错。
- G1不是取消分代；8:1:1不是所有收集器的固定比例。对象布局需固定VM、架构和选项。
- CHM在并发修改时的size不是事务快照，不等于静止时也不准确；线程池容量不能只背2N+1。
- Spring事务先查代理调用和配置；默认回滚还包括Error，非public能否拦截依代理与版本。
- MySQL索引访问要看具体计划；OR或函数出现不构成永不使用索引的证明。

## 依赖与首次定位

JVM区域→可达性与收集；JMM→happens-before→volatile与锁→线程池；B+树→聚簇/联合→执行计划→事务与锁；本地事务→消息幂等→分布式协调。先逐轮定位volatile、索引计划、缓存失效，每轮只一个动作；前置未建立就回基础。复习先命中最近错因，不用同ID的另一个问题冒充复习。

CMS题需明确旧JDK条件；用户要求新JDK时直接转到当前可用收集器机制，不强迫背已移除工具。跨到Go时使用go-backend领域，稳定ID不同，不自动共享成绩。
