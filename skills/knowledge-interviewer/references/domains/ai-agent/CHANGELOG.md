# AI Agent 知识域变更记录

## 2026-11-10 新鲜度复核

- 复核范围：当前官方版本入口与关键断言；不冒充整表或论文数字全量刷新。
- 修订：OTel核心依赖1.44.0→1.45.0；Development与GenAI schema保留；无release也可固定commit，修正旧的不可pin推论。字段比例降为历史快照，不将旧提交日期当当前最新。
- 修复：OWASP Top 10 for Agentic Applications官方URL缺少for导致404的问题。
- 保留：MCP current 2026-07-28；A2A规范1.0.0与仓库补丁v1.0.1分开；NIST为Concept Paper草案，不称正式标准。各项范围见sources本次核验表。
- 教学：明确按本地偏好使用短表格/流程图，唯一问题置末尾，尊重换点与结束。四域增加表格补课合成用例，共24例仍not_run。
- 自测：135点/题链一致性、19项Python测试、两域检查、历史证据结构、Skill结构通过；新行为评测未运行，本轮没有切换其他工具的全局Skill入口；本地学习档案正文未修改。

## 2026-11-09
- 定向研究牛客公开摘要、力扣三题与官方技术资料；未声称覆盖全站最新内容。
- 新增：面经场景映射、三组原创迁移练习、四点架构补全、知识审计、前端扩展方案。
- 修订：SSE 从“不纳入”转到前端边界；MCP 下一版安排以维护者记录覆盖旧结论。
- 来源仅局部复核，保留全表 verified_at；学习状态与已有 ID 不变。
- 静态 PASS（33 ID、21 题链、42 来源，兼容仓库进度中的 27 个旧 ID）；本轮未运行陪练行为 eval，不安装或覆盖外部技能。

## 2026-11-03

- 新增 `interview-bank.md`：牛客/力扣面经高频问法到图谱 ID 的映射层。**不新增 ID、不引用面经答案**；面经题只作入口，判档仍按 `map.md`；同题不同问法合并，框架 API/产品选型/训练流程题明确不纳入。
- 来源为 Tier 3 社区面经（牛客两帖正文需登录，只核标题与摘要），仅用于发现高频问法，不作机制结论依据。
- `map.md` 首段与 `SKILL.md` 参考资料补指针；结构层无变化，`questions.md` 不变。
- 安装方式变更：`~/.qoder/skills/knowledge-interviewer` 改为软链到本仓库 `skills/knowledge-interviewer/`，此后只改仓库内容。

## 2026-10-30

- 研究窗口：2025-04-30..2026-10-30；按「版本先于内容」先开官方版本索引/changelog，检索词不锚定已知版本号。
- 结构层：**无实质变化**。33 个 `agent.*` ID 全部保留，`map.md` 仅更新核验日期。本周所有新机制证据都是 arXiv 预印本，按 `maintenance.md` 规则「预印本最高作为趋势证据，不独立触发结构层修改」；且相关表述已被既有条目覆盖（`agent.ctx.memory` 已含「遵守」、`agent.safety.boundary` 已含「资产集合×出口集合」、`agent.eval.assertion` 已含「哪些维度不能加权抵消」）。
- 版本核验结论：MCP **2026-07-28 仍是现行版本**（草案页无日期、changelog 为空；2026-08-22 roadmap 只提「下一次规范发布」，无日期、无版本名、无弃用移除时间表）。A2A 规范页仍标 `1.0.0`，而仓库最新 tag 已是 `v1.0.1`——两处官方入口不一致，v1.0.1 日期在官方两处也不一致（记作 2026-05-26/28）；roadmap 的 v1.1 尚未发布。
- 修订（趋势层）：MCP 条目拆分「已移除」（initialize/notifications/initialized 握手、协议级会话、`Mcp-Session-Id`）与「仅弃用、仍在规范中」（Roots/Sampling/Logging/OAuth DCR→CIMD/HTTP+SSE/`includeContext` 枚举）；Tasks 移出核心为扩展且 `tasks/result` 改为 `tasks/get` 轮询；`server/discover` 为服务端 MUST。OpenTelemetry GenAI 条目重写：仍 Development、0 releases / 0 tags、`gen-ai-dev/1.42.0-dev`，新增 `invoke_workflow`/`plan`/skill/命令执行 span、transfer 属性、`*_ref` 内容引用、A2A 语义约定（2026-10-27）、embeddings metric breaking 重命名，最新变更 2026-10-28。NIST 条目补评论期 2026-04-02 关闭与 2026-09-29 Summary of Comments。多 Agent 与长期记忆各补一个独立第二来源。
- 新增（趋势层）：压缩与约束衰减条目；Agentic 安全威胁分类条目（OWASP Top 10 for Agentic Applications 2026 成为旗舰，T&M v1.0 为底层分类法）。新增来源 S30–S42。
- 收窄 / 不予写入：`_meta` 由「身份随每个请求传递」收窄为「按请求携带协议版本；客户端/服务端自述身份是 SHOULD 不是 MUST」；「正式扩展框架」改为归因 Tier 2 生态文章，非规范原文；MCP 错误码变更仅 Tier 3 来源，不写入；NIST 项目页标题措辞差异（AI→SI）不支持，不写入；NIST IR 8596 仅 Tier 3，不写入。
- 降级/移除：无。排除的数字（条件不全，只保留机制）：GAUGE ρ=0.94 / 31% / 57.5%、STALE 55.2%、ATOM 21.7%、[S41][S42] 的 delta、厂商博客 85.8% 缓存命中与 77% 降本。成本/延迟、RAG/检索、上下文污染三块本周**无实质变化**，未制造新知识点。
- 来源核验：7 supported / 1 partial / 0 unsupported（partial = NCCoE 页面 Cloudflare 403，仅 snippet 取证，已在 [S34] 标注）。另纠正上周一处：OWASP T&M 的 `dateModified` 确为 2025-04-28，既有记录正确，子代理提出的 2025-02-17 更正有误，未采纳。
- 自测：静态 PASS（33 图谱 ID、21 题链、42 来源锚点、兼容学习记录 27 个旧 ID、sources age 0 天）；行为 19/19 断言通过，覆盖旧学习状态路由、MCP/A2A 版本边界、任务级成本、单题格式；旧状态兼容 pass（`progress.md` / `mistakes.md` SHA-256 与运行前逐字节一致，未修改）。
- 测试规格修正：eval 4 的断言「题干没有直接陈述 initialize/Mcp-Session-Id 已被移除」与 `SKILL.md` 的「版本事实是题目前提，不是额外考点」直接冲突，正确行为无法通过。改为保护其真实意图——题干不得泄漏被考机制（哪些状态仍须跨请求延续、会话粘性结论是否成立），版本事实可作前提给出；并补一条「已移除 vs 仅弃用」断言。这是收紧而非放宽：断言数从 4 增至 5。
- 教学层：`questions.md` 仅在 `agent.protocol.interop` 的版本门禁补两条精度要求（两处官方入口不一致时直接说出；区分已移除与仅弃用），题链不变。

## 2026-10-16

- 研究窗口：2025-04-16..2026-10-16；优先核验 2026-10-09 以来的官方版本索引、changelog 与 deprecated 状态。
- 新增：RAG 引用忠实性、LLM 裁判表面特征偏差、网页 agent prompt injection 的失败证据与数字边界。
- 修订：补全 MCP 2026-07-28 弃用清单；区分 A2A 1.0.0 规范与仓库 v1.0.1 补丁发布；记录 OpenTelemetry GenAI 2026-10-14 字段变更；明确 NIST 材料仍是 Initial Public Draft Concept Paper。
- 结构层：双源复核后无实质变化；仅更新 `map.md` 核验日期，33 个既有 `agent.*` ID 全部保留，`questions.md` 不变。
- 降级/移除：无；将 RAG 57% 表述收窄到 Command-R+、NaturalQuestions 的对抗文档插入实验，不外推为普遍引用错误率。
- 来源核验：6 supported / 1 partial / 0 unsupported；partial 已收窄。
- 自测：静态检查通过（33 个图谱 ID、21 条题链、29 个来源锚点、兼容学习记录中的 27 个旧 ID）；最终候选版行为自测 18/18 断言通过，覆盖旧学习状态路由、MCP/A2A 版本边界、任务级成本与单题格式；`progress.md` / `mistakes.md` 未修改。
- 行为修订：首轮评分仍缺 A2A 补丁边界；补跑暴露模糊版本出题后，将精确版本事实固定为题目前提，并同步协议题链，再全量复测通过。

## 2026-10-09

- 触发：安装后复核，发现 2026-10-08 研究漏检两项趋势层更新。
- 修订：MCP 趋势条目 2025-11-25 → 2026-07-28 GA（无状态化、Tasks 扩展化、CIMD、Roots/Sampling/Logging 弃用）；OpenTelemetry GenAI 约定迁至独立仓库，状态 Development。
- 结构层：未变。`map.md` / `questions.md` 均以“MCP 类协议”表述，无版本依赖；“schema 不保证业务授权”结论不受影响。
- 维护流程：新增“版本先于内容”规则，检索不得锚定已知版本号。
- 来源核验：MCP 官方博客 supported；OTel GenAI 仓库 supported；A2A v1.0（2026-03-12）复核 supported；NIST 概念论文仍为概念论文 supported。

## 2026-10-08

- 研究窗口：2025-04-08..2026-10-08；基础来源例外保留并标注。
- 新增：Workflow/Agent 边界、耐久执行、协议互操作、RAG 分层评测。
- 修订：记忆生命周期、schema 与业务语义、规划前提复验、轨迹评测、身份委托、任务级成本与尾延迟。
- 趋势：MCP 2025-11-25、A2A v1.0、多 Agent 扩展、长期记忆基准、OpenTelemetry GenAI。
- 来源核验：8 supported / 2 partial / 0 unsupported；两条 partial 已收窄表述。
- 静态自测：通过；33 个图谱 ID、21 条题链、21 个来源锚点，兼容现有学习记录中的 27 个旧 ID。
- 行为自测：第二轮新版 12/12 断言通过，旧版基线 10/12；修复了“一个问号里绑定多个作答动作”的问题。
- 性能观察：新版平均耗时 52.5 秒，旧版 67.6 秒；新版平均 token 731739，旧版 625164，知识核验开销仍需后续优化。
