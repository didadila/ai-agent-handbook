# Java后端来源与版本边界

> verified_at: 2026-11-10

基线：Java21的规范与JDK API，MySQL InnoDB8.4；Spring官方参考页访问时为7.0系列，涉及6起方法可见性变化时明确给版本。Redis与Broker差异按实际目标版本核验。这里不声明Java21是最新JDK，也不把HotSpot实现当Java语言规范。CMS保留为历史ID，JDK14已移除；偏向锁旧优化路径不作为当前JDK必答步骤。OpenJDK JEP页面本次返回403，版本事实改由Oracle迁移指南核验，不记为已读JEP。

## 知识点证据映射

注意：下表大部分沿用按主题分组的来源入口，不能视为64条结论均已逐条得到直接证据支持。访问核验只证明当时读到对应文档；精确断言仍需定位到文档段落，无法直接支持的应用设计应标为设计推论。分布式ID、限流等不能仅靠Raft/CAP论文背书，需继续补专题来源。本轮对redo单独补了直接来源。

| ID | 证据 | 适用边界 |
|---|---|---|
| `jvm.memory.areas` | [J01][J02][J03][J04] | 逃逸分析可优化分配，不能据此保证所有对象都在栈上。 |
| `jvm.memory.stack` | [J01][J02][J03][J04] | 帧大小和可用栈受实现、编译与参数影响，不背固定递归次数。 |
| `jvm.object.layout` | [J01][J02][J03][J04] | 对象头不是跨JDK永不变化的格式；紧凑对象头等变化不写成语言定律。 |
| `jvm.gc.reachability` | [J01][J02][J03][J04] | 引用处理和终结机制有额外语义，不以是否执行finalize证明存活。 |
| `jvm.gc.generational` | [J01][J02][J03][J04] | 大对象路径、晋升年龄与Region阈值依实现和参数，先给出环境。 |
| `jvm.gc.algorithms` | [J01][J02][J03][J04] | 算法名称不能直接推出整次GC是否并发或是否全程停顿。 |
| `jvm.gc.stw` | [J01][J02][J03][J04] | 长循环是否延迟安全点取决于编译和轮询实现，不把所有循环一概而论。 |
| `jvm.gc.cms` | [J01][J02][J03][J04] | 保留旧ID用于旧系统迁移；不把历史阶段细节当当前默认收集器能力。 |
| `jvm.gc.g1` | [J01][J02][J03][J04] | Region化不等于取消分代；极端情况下仍可能出现Full GC。 |
| `jvm.gc.crossgen` | [J01][J02][J03][J04] | 卡表、记忆集、并发标记屏障解决的问题相关但不完全相同。 |
| `jvm.classload.process` | [J01][J02][J03][J04] | 解析时机可有实现选择；不要把类加载顺序误作业务依赖编排。 |
| `jvm.classload.parent` | [J01][J02][J03][J04] | 自定义加载器不等于任意绕过平台约束；区分加载失败与初始化失败。 |
| `jvm.tuning.oom` | [J01][J02][J03][J04] | 本书不要求线上无条件抓全量dump，先评估影响与数据处理范围。 |
| `conc.jmm.model` | [J05][J06][J07][J08][J09][J10][J11] | 主内存/工作内存只作抽象解释，不与每级CPU缓存一一对应。 |
| `conc.jmm.happensbefore` | [J05][J06][J07][J08][J09][J10][J11] | 关系是规范约束，不是要求所有机器指令严格按同一时间顺序执行。 |
| `conc.volatile` | [J05][J06][J07][J08][J09][J10][J11] | 需要精确实时总量时，不把LongAdder的并发求和当作事务快照。 |
| `conc.thread.state` | [J05][J06][J07][J08][J09][J10][J11] | Java状态不与操作系统状态逐项一一对应。 |
| `conc.sync.upgrade` | [J05][J06][J07][J08][J09][J10][J11] | 不承诺同一对象在所有JDK只升不降，内部优化不等于语言契约。 |
| `conc.cas.problems` | [J05][J06][J07][J08][J09][J10][J11] | LongAdder适合统计吞吐，不保证任意跨字段精确一致读。 |
| `conc.aqs` | [J05][J06][J07][J08][J09][J10][J11] | 队列思想可以借用，但不能把实现简化为教科书CLH的逐行拷贝。 |
| `conc.lock.compare` | [J05][J06][J07][J08][J09][J10][J11] | 不把ReentrantLock或synchronized绝对判为更快，需给出负载与版本。 |
| `conc.threadlocal` | [J05][J06][J07][J08][J09][J10][J11] | 不能把ThreadLocal当跨线程共享数据库，也不把弱引用当自动资源管理。 |
| `conc.chm` | [J05][J06][J07][J08][J09][J10][J11] | 不要用size是否达到阈值来原子控制并发容量。 |
| `conc.threadpool.params` | [J05][J06][J07][J08][J09][J10][J11] | 关闭和资源耗尽也会拒绝；调用者执行策略可能阻塞入口线程。 |
| `conc.threadpool.sizing` | [J05][J06][J07][J08][J09][J10][J11] | 虚拟线程也不消除DB连接、配额和副作用并发上限。 |
| `conc.tools` | [J05][J06][J07][J08][J09][J10][J11] | 同步工具不自动收集任务错误或处理取消，需显式设计结果路径。 |
| `mysql.index.bplustree` | [J12][J13][J14][J15][J16][J17] | 不要背三层必容纳某个固定记录数，需给页和键的假设。 |
| `mysql.index.clustered` | [J12][J13][J14][J15][J16][J17] | 聚簇组织是InnoDB条件，不推广为所有数据库表结构。 |
| `mysql.index.covering` | [J12][J13][J14][J15][J16][J17] | 不把最左前缀简化为任何缺首列查询都绝对不使用索引。 |
| `mysql.index.failure` | [J12][J13][J14][J15][J16][J17] | 函数表达式匹配和数据库版本需明确，不能跨产品照搬。 |
| `mysql.tx.isolation` | [J12][J13][J14][J15][J16][J17] | 跨事务业务流程不会因每步都开事务而自动串行化。 |
| `mysql.tx.mvcc` | [J12][J13][J14][J15][J16][J17] | 不把所有读取都当MVCC快照读；锁定读还有锁和新状态语义。 |
| `mysql.lock.types` | [J12][J13][J14][J15][J16][J17] | 先给索引与SQL，再画范围，不背所有RR查询都锁全表。 |
| `mysql.lock.deadlock` | [J12][J13][J14][J15][J16][J17] | 超时和死锁不是相同证据；数据库回滚不撤回外部HTTP效果。 |
| `mysql.log.redo` | [J31] | redo的崩溃恢复机制；binlog、两阶段提交和刷盘组合需另查相应条目，不以本条作完整背书。 |
| `mysql.explain` | [J12][J13][J14][J15][J16][J17] | 执行分析语法与支持范围依产品版本，不能把PostgreSQL输出当MySQL输出。 |
| `mysql.slowquery` | [J12][J13][J14][J15][J16][J17] | 跨页期间数据变化的可见性和跳页需求是方案代价。 |
| `mysql.sharding` | [J12][J13][J14][J15][J16][J17] | 分片不是自动水平扩展，倾斜键仍可能形成单点热点。 |
| `redis.ds.impl` | [J18][J19][J20][J21] | 旧ziplist经验不直接当作新版本全部类型的编码事实。 |
| `redis.thread.model` | [J18][J19][J20][J21] | 模块及新版本实现必须给具体条件，不背全生态绝对线程模型。 |
| `redis.persist` | [J18][J19][J20][J21] | 恢复目标需与刷盘、复制和备份同时说明，不靠配置名作保证。 |
| `redis.expire` | [J18][J19][J20][J21] | LRU/LFU可用近似采样，不把淘汰顺序当精确全局排序。 |
| `redis.cache.problems` | [J18][J19][J20][J21] | 布隆过滤器的误判与更新流程需纳入数据可见性契约。 |
| `redis.cache.consistency` | [J18][J19][J20][J21] | 不要说缓存场景绝对不可能强一致；代价取决于选择的完整协议。 |
| `redis.lock` | [J18][J19][J20][J21] | 锁正确性取决于故障模型、时钟和受保护资源，不把任何单方案当通用证明。 |
| `redis.cluster` | [J18][J19][J20][J21] | 多副本确认也需说明确认代表接收还是持久化。 |
| `spring.ioc.lifecycle` | [J22][J23][J24][J25][J26] | 精确钩子顺序需要给Spring版本、Bean作用域和处理器配置。 |
| `spring.ioc.circular` | [J22][J23][J24][J25][J26] | Boot允许循环引用的默认策略与Framework内部能力分开说明。 |
| `spring.aop.proxy` | [J22][J23][J24][J25][J26] | final/private等方法与代理方式有关，不能只背两种代理类名。 |
| `spring.tx.propagation` | [J22][J23][J24][J25][J26] | NESTED不等于独立事务，支持情况必须核对资源与事务管理器。 |
| `spring.tx.failure` | [J22][J23][J24][J25][J26] | 代理类型、方法可见性、版本与全局回滚配置都属于题目前提。 |
| `spring.boot.autoconfig` | [J22][J23][J24][J25][J26] | 声明配置与执行装配有先后，版本差异按官方参考核验。 |
| `mq.usecase` | [J27][J28] | MQ不是消除工作量，只是改变执行时间与失败边界。 |
| `mq.reliability` | [J27][J28] | 确认必须对应具体Broker和配置，不能泛化为所有队列零丢失。 |
| `mq.idempotent` | [J27][J28] | Broker内部exactly-once不自动覆盖任意外部HTTP或数据库副作用。 |
| `mq.order` | [J27][J28] | 局部顺序和全局顺序成本不同，不能为了口号无限串行化。 |
| `mq.backlog` | [J27][J28] | 扩大并行度也可能破坏顺序与热点控制，需复验契约。 |
| `dist.cap` | [J29][J30] | CAP不是任意环境下自由三选二，也不替代事务隔离或持久性分析。 |
| `dist.idgen` | [J29][J30] | 不能笼统说所有UUID都随机或所有雪花参数固定相同。 |
| `dist.tx` | [J29][J30] | 2PC、TCC和Saga的协调代价及故障恢复条件不可混称。 |
| `dist.consensus` | [J29][J30] | Raft复制日志不是跨任意数据库的业务2PC，也不替代应用幂等。 |
| `dist.limiting` | [J29][J30] | 降级答案可能不完整，必须向用户表达承诺变化。 |
| `sys.design.estimate` | [J29][J30] | 平均QPS不能代替峰值并发，缓存命中也不自动保护写入路径。 |
| `sys.design.case` | [J29][J30] | 方案评审需要具体量级与失败输入，不把架构图复杂度当正确性。 |

## 官方与原始来源

- **[J01]** [JVM21运行时结构](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html)，核验2026-11-10。
- **[J02]** [JVM21加载链接初始化](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html)，核验2026-11-10。
- **[J03]** [G1调优与逻辑分代](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector1.html)，核验2026-11-10。
- **[J04]** [JDK移除与弃用组件](https://docs.oracle.com/en/java/javase/21/migrate/removed-tools-and-components.html)，核验2026-11-10。
- **[J05]** [JLS21内存模型](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html)，核验2026-11-10。
- **[J06]** [ThreadPoolExecutor](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html)，核验2026-11-10。
- **[J07]** [ConcurrentHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)，核验2026-11-10。
- **[J08]** [ThreadLocal](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html)，核验2026-11-10。
- **[J09]** [Atomic包](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/atomic/package-summary.html)，核验2026-11-10。
- **[J10]** [AQS](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/AbstractQueuedSynchronizer.html)，核验2026-11-10。
- **[J11]** [ReentrantLock](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html)，核验2026-11-10。
- **[J12]** [InnoDB多版本](https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html)，核验2026-11-10。
- **[J13]** [InnoDB锁](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html)，核验2026-11-10。
- **[J14]** [聚簇与二级索引](https://dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html)，核验2026-11-10。
- **[J15]** [联合索引](https://dev.mysql.com/doc/refman/8.4/en/multiple-column-indexes.html)，核验2026-11-10。
- **[J16]** [EXPLAIN](https://dev.mysql.com/doc/refman/8.4/en/explain.html)，核验2026-11-10。
- **[J17]** [死锁处理](https://dev.mysql.com/doc/refman/8.4/en/innodb-deadlocks.html)，核验2026-11-10。
- **[J18]** [Redis持久化](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)，核验2026-11-10。
- **[J19]** [Redis租约锁](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)，核验2026-11-10。
- **[J20]** [Redis淘汰](https://redis.io/docs/latest/develop/reference/eviction/)，核验2026-11-10。
- **[J21]** [Redis集群](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/)，核验2026-11-10。
- **[J22]** [Spring代理机制](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)，核验2026-11-10。
- **[J23]** [Transactional边界](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)，核验2026-11-10。
- **[J24]** [回滚规则](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html)，核验2026-11-10。
- **[J25]** [事务传播](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html)，核验2026-11-10。
- **[J26]** [自动配置](https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html)，核验2026-11-10。
- **[J27]** [RabbitMQ确认](https://www.rabbitmq.com/docs/confirms)，核验2026-11-10。
- **[J28]** [RabbitMQ队列与顺序](https://www.rabbitmq.com/docs/queues)，核验2026-11-10。
- **[J29]** [Raft原始论文](https://raft.github.io/raft.pdf)，核验2026-11-10。
- **[J30]** [Gilbert与Lynch：Perspectives on the CAP Theorem](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf)，核验2026-11-10。
- **[J31]** [InnoDB8.4 Redo Log](https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html)，核验2026-11-10。

来源支持各节的稳定机制，不证明每种实现都相同。对象大小、线程池吞吐、GC停顿等数字需在给定环境实测。跨资源幂等、fencing与补偿是应用设计约束，不将其包装成框架自动提供的能力。需研究具体产品时继续核验该产品官方文档；不把单次实验或面经答案直接写成永久标准。
