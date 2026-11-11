# 知识新鲜度、目录与展示规则复核

## 范围与结果

本次复核官方版本入口、关键机制断言及已知失效引用，不声称逐句认证全部教材，也不将未重验论文数字刷新成当前事实。全表verified_at保留原范围，在sources逐项记录本次结果。

|领域/切面|来源|2026-11-10结果与处理|
|---|---|---|
|MCP版本|[Versioning](https://modelcontextprotocol.io/specification/versioning)|current仍为2026-07-28，弃用不等于移除|
|A2A版本|[规范](https://a2a-protocol.org/latest/specification/) · [发布页](https://github.com/a2aproject/A2A/releases)|规范页标1.0.0，仓库Latest v1.0.1，继续分层记录|
|OTel状态|[manifest](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/model/manifest.yaml) · [CHANGELOG](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/CHANGELOG.md)|仍Development，GenAI schema为1.42.0-dev；核心依赖已从旧快照1.44.0变为1.45.0，已修正|
|OTel版本固定|[releases](https://github.com/open-telemetry/semantic-conventions-genai/releases)|无已发布release，不等于不能固定Git commit；修正旧推论|
|OTel字段覆盖|[reference](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/reference/README.md)|现按Span链接分项报告，不再把旧3/11、2/11和10-28提交日期当当前生态状态|
|NIST状态|[CSRC](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd)|仍为Initial Public Draft Concept Paper、评论关闭；不能称正式标准。旧Summary of Comments取证不升级|
|OWASP来源|[正确官方页](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)|修复缺少for导致404的旧URL，页面日期为2025-12-09|
|Java历史机制|[Oracle迁移指南](https://docs.oracle.com/en/java/javase/21/migrate/removed-tools-and-components.html)|CMS移除与偏向锁历史边界仍成立，Java21作为教学基线保留|
|Spring事务|[Transactional](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)|6起类代理可支持protected/package方法，接口代理仍要求public；保留前提|
|Go版本|[发布历史](https://go.dev/doc/devel/release)|页面列1.27系列及补丁；不把本机1.26工具链称为最新版|
|MySQL|[InnoDB MVCC](https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html)|保留InnoDB8.4条件，MVCC基于多版本，不把全部读取都视为同类快照读|
|Redis|[分布式锁](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)|仍需有效期与故障模型边界，不把租约锁当通用外部副作用证明|
|React|[useEffect](https://react.dev/reference/react/useEffect)|cleanup与过期响应防护仍成立；文档入口显示19.3，不批量修改教学目标版本|
|TypeScript|[Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)|断言编译移除、无运行时转换/校验仍成立|

## 目录与展示

- handbook/ai-agent是当前公共教材；handbook/agent只剩本机未跟踪旧学习记录，不是另一卷。确认四份旧Agent/Go记录与.local对应副本逐字节相同后清除重复文件及空目录；本地权威档案正文未改。
- 新增docs/README说明设计文档与历史报告的读者、职责；根README详述产品形态、四域入口、学习流程、目录、数据边界和验证限制。
- 用户原有本地输出偏好仍然有效，内容未改；主Skill明确实际读取偏好，用短表格承载判档/缺口、流程承载因果。图表替代重复段落，唯一作答动作置末尾；“表单”按语境理解为结构化表格，不生成填写问卷。
- 修复“追问到底”和“到期复习不能因想学新内容跳过”的绝对规则，尊重换点、结束与当前学习目标；personas不再凌驾用户明确要求。
- 四域各补1个合成表格补课场景及rubric；共24个新增行为用例，状态not_run。格式示例不等于实际模型行为通过。
- 区分仓库Skill与全局安装实例：优化作用于当前仓库。独立副本需另行更新，软链需核对实际目标；本轮未改其他工具的全局安装配置。

## 验证边界

运行全项目一致性、Python单元测试、两域原校验、历史评测证据检查、Skill结构和隐私检查。结果在提交前重新验证；正文定位覆盖135点。没有重跑新的冷启动模型评测，不报告24例通过。Java来源粒度与跨域实验等已知缺口仍见学习系统说明。

研究论文和旧统计比例仍按历史样本解释，未在本轮重新复算；没有把批量访问成功当作所有断言被支持。
