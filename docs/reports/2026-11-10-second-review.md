# 目录、知识质量与学习流程二次检查

## 已发现并处理

1. Skill原有教材链接没有形成按ID读取正文的统一流程，学习者只走Skill时可能绕过教材。增加learning-flow和公共定位脚本，135个ID均可定位到真实章节的起止行；用户无需手动切换产品入口。
2. 根目录个人反馈与输出偏好已被Git忽略，但仍有历史副本，且当前Skill没有清晰读取约定。确认两份文件与.local/learning/preferences中的对应文件逐字节一致后清除根目录副本；保留本地原偏好、忽略规则，Skill改读本地preferences。
3. 公共PRIVACY是全项目发布与存储契约，保留在根目录；Skill包含执行规则，脚本部分落实防护，三者职责不同。
4. Skill用“说不出内存屏障就判C”作为volatile判据，混淆规范理解与实现术语。改为按具体场景、同步关系和复合操作边界判定，接受正确的替代解释。
5. Java来源映射存在按主题整组挂链接的粗粒度问题，不能声称逐点有直接证据。已标记限制，redo补入MySQL8.4专门来源；其余分布式ID、限流等证据细化列入待办。

## 官方资料抽查

|切面|入口与结果|
|---|---|
|MCP|[Versioning](https://modelcontextprotocol.io/specification/versioning)：current仍为2026-07-28；Deprecated不等于Removed|
|Java历史机制|[Oracle迁移指南](https://docs.oracle.com/en/java/javase/21/migrate/removed-tools-and-components.html)：CMS于JDK14移除，偏向锁在后续版本禁用并弃用；保留历史边界|
|Java判档|[JLS17](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html)：用规范同步关系评价理解，不要求唯一机器实现术语|
|Spring|[Transactional](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)：6起类代理可支持protected/package方法，接口代理仍要求public；需明确代理模式|
|TypeScript|[Type Assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)：无运行时校验或数据转换|
|React|[useEffect](https://react.dev/reference/react/useEffect)：cleanup及过期响应防护机制仍成立|
|Go|[发布历史](https://go.dev/doc/devel/release)列1.27主版本；[errors](https://pkg.go.dev/errors)支持错误树上的Is/As语义，不能只比字符串|
|MySQL|[Redo Log](https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html)：补直接来源；不据此声称已核验全部binlog与提交协议|
|Redis|[Distributed Locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)保留故障模型与有效期讨论，不构成任意业务副作用安全的通用证明|

这是风险切面抽查，不是全库逐句审计。Agent趋势表例行复核已到期，除MCP外其余依旧是历史快照；不更新整表日期制造全量已刷新印象。新增20个行为用例仍未运行。

## 验证与剩余工作

四域135点/135题链、公共链接、两域原检查及Skill结构检查通过。19项Python测试通过，包含所有135点能定位到真实章节、节范围不越过下一节、别名与跨域拒绝。未重跑没有变动的前端代码测试；上轮26项通过记录仍见前一报告。

测试证明定位程序及静态契约，不证明模型每轮都已执行教材读取。优先级是行为评测、可执行实验、断言级来源、公共基础与跨卷项目，详见[学习系统说明](../learning-system.md)。Java教材当前是64点核心讲义，各域深度、实验和评测成熟度并不相等；目录一致不是完整性证明。
