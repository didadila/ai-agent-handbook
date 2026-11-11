# AI Agent 证据索引

> verified_at: 2026-10-30  
> 下次例行核验：2026-11-06（已到期；2026-11-09 仅局部复核，不代表全表重新核验）
> 原则：稳定机制可进入 `map.md`；协议版本、模型能力、实验数字只进入趋势层，出题时保留适用条件。

2026-11-10再次核验：MCP、A2A、OTel、NIST、OWASP的当前入口和关键版本断言已复查，结果见下表。不改全表verified_at：研究论文、统计数字及未逐段复查的细节仍属于历史快照。核验入口不等于认证全部关联结论。

| 核验项 | 2026-11-10结果 | 处理 |
|---|---|---|
| MCP版本与弃用 | current为2026-07-28；弃用仍在规范内 [S30] | 保留 |
| A2A规范/补丁 | 规范页Latest Released 1.0.0，仓库Latest v1.0.1 [S7][S25] | 保留两层版本，不合并 |
| OTel manifest | Development，GenAI schema仍为1.42.0-dev，核心依赖已到1.45.0 [S32] | 更新旧1.44.0；删除“最新提交停在10-28”的现时说法 |
| OTel版本固定 | releases页无已发布release；可固定Git commit | 修正“没有release就无法pin”的错误推论 |
| OTel一致性矩阵 | reference入口已按Span链接到分项报告 [S33] | 3/11、2/11仅保留历史条件，不作当前生态比例 |
| NIST文档状态 | CSRC入口仍为Initial Public Draft Concept Paper，评论期关闭 [S14] | 不称正式标准；Summary of Comments仍属原partial记录 |
| OWASP入口 | 旧URL缺少for，返回404；正确官方页可读，日期2025-12-09 [S35] | 修复链接，不据此宣称风险清单完备 |


## 稳定结论

| 结论 | 证据 | 教学边界 |
|---|---|---|
| Workflow 走预定义路径，Agent 动态决定过程；应从简单方案起步 | [S1] | 不用“任务复杂”代替“下一步依赖运行时未知事实” |
| 长任务需要外部状态、checkpoint、幂等和恢复，长上下文不能替代运行时 | [S1][S2] | 不宣称任何框架自动提供 exactly-once |
| 最小充分上下文优于填满窗口；长期任务应按当前决策重建上下文 | [S3][S4][S38] | `context rot` 的具体衰减率不外推；长度是放大器，证据分散度与推理深度才是主要难度来源，不要把"变长"单独当成退化原因 |
| 记忆必须有失效、作用域和冲突处理 | [S5][S40][S41] | 单一基准不能证明某类记忆框架普遍无效；"召回到了新事实"不等于"会照着新事实行动"，失效判定的瓶颈常在遵守而不是检索 |
| schema 校验参数形状，不保证主体归属、业务授权和副作用安全 | [S6][S7] | 协议提供能力表达，不替代业务控制 |
| 混合召回、rerank 和分层评测比单一端到端分数更可诊断 | [S8][S9][S27] | 厂商实验降幅不得写成普适收益；答案正确或引用存在都不等于引用忠实 |
| Agent eval 同时验证最终状态和轨迹，并对随机系统多次运行 | [S10][S11][S12][S28][S37] | pass@k 不等于持续可靠；裁判会受表面特征影响，安全门不能被总分抵消；"安全停止"要作为独立结果维度记录，预算耗尽不能和任务失败并成一个计数 |
| Prompt injection 防御必须落在模型外的权限、策略和数据流边界 | [S13][S14][S29][S36][S37] | 提示词防护只能降概率；攻击未完成也可能只是能力不足，不能当成安全边界——攻击失败要拆成"显式拒绝"与"根本没理解"，单一 ASR 不是安全能力指标；破坏半径取决于环境实际允许的越界副作用，不只取决于声明的权限范围 |
| 成本以成功任务为单位，延迟看端到端尾部；缓存/路由/并行都有前提 | [S15][S16][S17][S18] | 产品定价、TTL 和收益数字随版本变化；缓存研究的账单/TTFT 结果不等于端到端尾延迟 |

## 2026 趋势快照

### 2026-11-09 局部复核与失效覆盖

- MCP 官方 [Versioning](https://modelcontextprotocol.io/specification/versioning) 仍将 `2026-07-28` 标为 current；新增弃用生命周期说明：通常至少保留 12 个月，加速例外至少 90 天后才具备移除资格，不能把弃用当成已经移除。
- **清理下表 MCP 行中“没有日期、没有移除时间表”的现时结论**：那只是旧 roadmap 的历史描述。官方 [2026-09-15 维护者会议记录](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/3402) 已把下一版目标调整到 2027 年 3 月；目标日期不等于已发布版本，也不证明任何单项功能一定随版发布。
- A2A、OTel、NIST和OWASP的2026-11-10核验覆盖上方列出的断言；其余研究数字与详细字段仍是历史快照，使用时核验具体来源。

| 趋势 | 当前证据 | 出题要求 |
|---|---|---|
| MCP 2026-07-28（GA 仍是现行版本；取代 2025-11-25） | **已移除**：`initialize`/`notifications/initialized` 握手、协议级会话与 `Mcp-Session-Id` 头。**仅弃用、仍在规范中**：Roots、Sampling、Logging、OAuth 2.0 Dynamic Client Registration（转向 Client ID Metadata Documents, CIMD）、HTTP+SSE 传输、`includeContext` 的 `thisServer`/`allServers`。**移出核心成为扩展**：Tasks（`io.modelcontextprotocol/tasks`），阻塞式 `tasks/result` 改为 `tasks/get` 轮询。`server/discover`：服务端 MUST 实现以声明支持的协议版本。`_meta` 按请求携带**协议版本**；客户端 SHOULD 用 `io.modelcontextprotocol/clientInfo` 自述身份，服务端 SHOULD 在每个 result 的 `_meta` 自述——是 SHOULD 不是 MUST，且版本不等于身份 [S6][S22][S24][S30]。"MCP Apps / Tasks / 企业托管授权被正式化为扩展"这一表述来自 Tier 2 生态文章，不是规范原文 [S31] | 明说版本；**区分"已移除"与"仅弃用"**，弃用项仍可在实现中出现；旧 roadmap 的时间安排描述已失效，下一版目标与弃用生命周期见本节 2026-11-09 复核说明 [S30]；生态 SDK 迁移进度不等于规范发布；"业务授权、幂等、恢复仍需实现"仍是推论而非规范原文 |
| A2A 规范页 1.0.0；仓库补丁 v1.0.1 | 规范页仍标注 **Latest Released Version `1.0.0`**（2026-03-12），而 GitHub 最新 tag 已是 `v1.0.1`——两处官方入口本身不一致，这个不一致就是可教的证据。v1.0.1 的日期在两处官方页面也不一致（tag 页显示 05-28，releases 列表渲染 2026-05-26），记作 2026-05-26/28。1.0 规范定义 Agent Card、任务生命周期、Artifact、流式/推送和安全方案声明；v1.0.1 是 bug-fix patch，不是新规范代际。roadmap 的 v1.1（双向流式、A2A CLI、elicitation/多轮）**尚未发布** [S7][S25] | 区分规范页的 latest released specification 与仓库 patch release；不把 roadmap 条目当成已发布能力；不说成自动互操作、事务或恢复保证 |
| 多 Agent 扩展 | 并行任务可能受益，顺序依赖任务可能退化；拓扑影响错误放大 [S19][S20]。独立第二来源：在**同等 token 预算**下单 agent 在多跳推理上可与多 agent 持平或更好，多 agent 的优势出现在单 agent 上下文利用已经退化时 [S42] | 数字只作为实验案例，判据落在任务依赖、同等预算条件和 parent 可复验性 |
| 长期记忆基准 | 过时、冲突和演化事实成为显式评测维度 [S5]。进一步证据：失效判定的瓶颈常在**遵守**而不是检索——召回到更新后的证据不等于照着它行动，隐式冲突尤其难 [S40]；"该存什么"与"该用什么"是两个独立判据，同槽位替换关系要显式建模 [S41] | 不宣布"记忆问题已解决"；[S40][S41] 的具体数字条件不全，只用机制不用数字 |
| 上下文压缩与约束衰减 | 压缩会静默擦除上下文内的安全约束：基线 0% 违规，压缩后升至 30%，最差 59%；软约束的衰减速度约为硬约束的 8.3×；把约束 pin 住可恢复到 0%，但朴素 pinning 不能阻止 operator 冒充 [S39] | 单一预印本、ConstraintRot 9 任务/1,323 episode/7 模型的条件下结果；只用来说明"压缩是安全相关操作"，不外推为通用违规率 |
| OpenTelemetry GenAI | 2026-11-10：manifest仍标Development、GenAI schema为`gen-ai-dev/1.42.0-dev`，核心semconv依赖更新为v1.45.0；CHANGELOG仍为Unreleased，releases页无已发布版本 [S32]。reference已按Span链接到分项报告 [S33] | 不称稳定标准；采用前固定commit和SDK版本，并运行兼容测试。无release不等于不能固定Git提交；旧字段比例和提交日期不当现时结论 |
| Agent 身份与委托 | NIST 将身份、授权、委托列为待研究和标准化问题；当前材料仍是 Initial Public Draft **Concept Paper**（2026 年 2 月，PDF 仍标 DRAFT），不是正式标准 [S14]。评论期已于 2026-04-02 关闭，NCCoE 于 2026-09-29 发布 Summary of Comments 与在线资源中心，下一步才是 draft project description；此条取证路径为 snippet（NCCoE 页面返回 Cloudflare 403），记作 partial [S34] | 评论期关闭不等于标准定稿；没有 NIST SP 草案或终稿就不要说"已有标准"；不要把项目页标题的措辞差异当成范围变更 |
| Agentic 安全威胁分类 | OWASP **Top 10 for Agentic Applications 2026**（ASI01–ASI10）已成为旗舰清单，Agentic AI – Threats and Mitigations v1.0 被定位为其底层分类法 [S13][S35]。局限证据：已有同行工作指出该威胁建模指南存在分类空白 | 分类法是出题脚手架，不是完备性保证；不把清单编号当成防御措施 |

## 来源

- **[S1]** Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), 2024-12-19, Tier 1, foundational.
- **[S2]** Microsoft Azure, [Durable Task for AI Agents](https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents), 2026-05-05, Tier 1.
- **[S3]** Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29, Tier 1.
- **[S4]** Chroma Research, [Context Rot](https://www.trychroma.com/research/context-rot), 2025-07-14, Tier 2.
- **[S5]** Uddin et al., [From Recall to Forgetting](https://aclanthology.org/2026.findings-acl.1337/), Findings of ACL 2026, Tier 1.
- **[S6]** MCP Project, [Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28), 2026-07-28, Tier 1（取代 [2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)）.
- **[S7]** A2A Project / Linux Foundation, [A2A v1.0 Specification](https://a2a-protocol.org/latest/specification/), 2026-03-12, Tier 1.
- **[S8]** Anthropic, [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval), 2024-09-19, Tier 1.
- **[S9]** Park et al., [MIRAGE](https://aclanthology.org/2025.findings-naacl.157/), 2025-04, Tier 1.
- **[S10]** OpenAI, [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), accessed 2026-10-08, Tier 1.
- **[S11]** Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), 2026-01-09, Tier 1.
- **[S12]** Google Cloud, [A methodical approach to agent evaluation](https://cloud.google.com/blog/topics/developers-practitioners/a-methodical-approach-to-agent-evaluation), 2025-11-18, Tier 1.
- **[S13]** OWASP GenAI, [Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/), updated 2025-04-28, Tier 1.
- **[S14]** NIST NCCoE, [Software and AI Agent Identity and Authorization](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd), 2026-02-05, Tier 1.
- **[S15]** OpenAI, [Prompt Caching](https://developers.openai.com/api/docs/guides/prompt-caching), accessed 2026-10-08, Tier 1.
- **[S16]** OpenAI, [Batch API](https://platform.openai.com/docs/guides/batch), accessed 2026-10-08, Tier 1.
- **[S17]** Lumer et al., [Don’t Break the Cache](https://arxiv.org/html/2601.06007v2), 2026-01-31, Tier 2.
- **[S18]** Jiang et al., [Survey on Routing Strategies](https://arxiv.org/html/2502.00409v3), 2025-02, Tier 2.
- **[S19]** Google Research, [Towards a science of scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/), 2026-01-28, Tier 1.
- **[S20]** Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/html/2503.13657v1), 2025-03-17, Tier 1.
- **[S21]** OpenTelemetry, [GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/), 2026-05-14, Tier 1.
- **[S22]** MCP Blog, [The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/), 2026-07-28, Tier 1.
- **[S23]** OpenTelemetry, [GenAI agent and framework spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md), accessed 2026-10-16, Tier 1.
- **[S24]** MCP Project, [Deprecated features in 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/deprecated), accessed 2026-10-16, Tier 1.
- **[S25]** A2A Project, [A2A v1.0.1 release](https://github.com/a2aproject/A2A/releases/tag/v1.0.1), GitHub published 2026-05-28, Tier 1.
- **[S26]** OpenTelemetry, [semantic-conventions-genai commit feed](https://github.com/open-telemetry/semantic-conventions-genai/commits/main.atom), accessed 2026-10-16, Tier 1.
- **[S27]** Wallat et al., [Correctness is not Faithfulness in RAG Attributions](https://dl.acm.org/doi/10.1145/3731120.3744592), SIGIR 2025, Tier 1.
- **[S28]** Shi et al., [Safer or Luckier? LLM Evaluators Are Easily Manipulated by Non-Safety Related Artifacts](https://aclanthology.org/2025.acl-long.970/), ACL 2025, Tier 1.
- **[S29]** Debenedetti et al., [WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks](https://neurips.cc/virtual/2025/poster/121728), NeurIPS 2025, Tier 1.
- **[S30]** MCP Project, [Versioning](https://modelcontextprotocol.io/specification/versioning) 与 [The New MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-08-22-roadmap/), accessed 2026-10-30, Tier 1（草案页无日期、changelog 为空；roadmap 未给下一版本日期或弃用移除时间表）.
- **[S31]** agentgateway, [What's new in MCP 2026-07-28](https://agentgateway.dev/blog/mcp-2026-07-28/), 2026-08-03, Tier 2（"扩展被正式化"的表述来源，非规范原文）.
- **[S32]** OpenTelemetry, [manifest](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/model/manifest.yaml)、[CHANGELOG](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/CHANGELOG.md)与[releases](https://github.com/open-telemetry/semantic-conventions-genai/releases)，2026-11-10复核：Development，GenAI schema 1.42.0-dev，核心依赖1.45.0，无已发布release；未核验tag数量，不作0 tags断言。
- **[S33]** OpenTelemetry, [semantic-conventions-genai 一致性矩阵 `reference/README.md`](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/reference/README.md), accessed 2026-10-30, Tier 1（逐库上报情况与 `conformance.yaml` 的 `expected_violations`）.
- **[S34]** NIST NCCoE, Software and AI Agent Identity and Authorization 项目页与 Summary of Comments, 2026-09-29, Tier 1 内容 / **partial**：页面返回 Cloudflare 403，取证仅基于搜索 snippet.
- **[S35]** OWASP GenAI, [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), 页面日期 2025-12-09/10, Tier 1.
- **[S36]** Zarif et al., [Ignored, Not Refused: What Low Prompt-Injection Success Rates Hide in Small Tool-Using Agents](https://arxiv.org/abs/2610.23254), 2026-10-16, Tier 2 预印本（33,000 条轨迹、11 个 2–14B 开源 agent、InjecAgent + AgentDojo；仅小开源模型，不外推前沿模型）.
- **[S37]** Bouke, [A Competing-Hazards Systematization of Loss of Control in Autonomous Agents](https://arxiv.org/abs/2609.23817), 2026-09-29, Tier 2 预印本（22 份事故报告 + 102 份评测，2025-01..2026-09）.
- **[S38]** Qin et al., [Beyond Context Length: Rethinking What Makes Long-Context Reasoning Hard](https://arxiv.org/abs/2610.22067), 2026-10-15, Tier 2 预印本（LURCH，17 个数据集、6,550 实例）.
- **[S39]** Chen, [Governance Decay: Silent Erosion of In-Context Safety Constraints under Compaction](https://arxiv.org/abs/2606.22528), v2 2026-06-27, Tier 2 预印本（ConstraintRot，9 任务、1,323 episode、7 模型）.
- **[S40]** Chao et al., [STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?](https://arxiv.org/abs/2605.04412), 2026-05-07, Tier 2 预印本（400 场景 / 1,200 查询 / 150K 上下文；数字条件不全，只用机制）.
- **[S41]** Li & Li, [What Should an Agent Forget? Separating What Is Stored from What Is Used](https://arxiv.org/abs/2609.07731), 2026-09-09, Tier 2 预印本（数字条件不全，只用机制）.
- **[S42]** Tran & Kiela, [Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning](https://arxiv.org/abs/2604.09812), 2026-04, Tier 2 预印本（同等 token 预算条件；数字条件不全，只用机制）.

## 历史实验数字及使用边界

| 数字 | 可用表述 | 禁止表述 |
|---|---|---|
| Contextual Retrieval 5.7%→2.9%→1.9% | 在 Anthropic 特定语料、top-20 和配置下，失败率相对下降 49%/67% [S8] | “混合检索普遍提升 67%” |
| RAG 引用事后合理化最高 57% | 在 Command-R+、NaturalQuestions 的对抗文档插入实验中，相关但原未引用文档的可比案例最高 57% 出现事后引用 [S27] | “57% 的 RAG 引用都是伪造的” |
| 多 Agent 80.9%、-39%~-70%、17.2× | Google 该实验显示收益取决于任务结构和拓扑 [S19] | “多 Agent 一定提升 80%” |
| Judge 偏好偏移最高 98%、位置偏差 4%–30% | ACL 2025 在 11 个裁判、576 个提示和 5 个安全域中观察到的表面特征敏感性 [S28] | “所有 LLM judge 都有 98% 偏差” |
| Prompt injection partial hijacking 最高 86% | WASP 的 84 个网页任务中，部分攻击目标最高达到 86%；完整目标常因 agent 能力不足未完成 [S29] | “86% 的网页 agent 会完整泄密” |
| 缓存 41%–80%、TTFT 13%–31% | 独立预印本在 500 个长任务中的条件性结果；不代表任务端到端 p95/p99 [S17] | “开启缓存就能省 80%” |
| 注入失败构成：被忽略 76%–80%，显式拒绝 17%–18%；ASR 仅因系统提示改动就从 0.2% 漂到 43% | 在 2–14B 开源小模型、InjecAgent + AgentDojo、33,000 条轨迹下，低 ASR 多数来自"没理解"而不是"拒绝"，且单一 ASR 对提示配置极敏感 [S36] | “小模型有 80% 的注入防御率”；把该结论外推到前沿模型 |
| 失控事故 20/22；102 份评测中 87 记录越界、26 把安全停止当一等结果、20 两者都记、79 把预算耗尽与任务失败并计 | 在该文献综述的 22 份事故报告与 102 份评测样本中，破坏半径主要由环境实际允许的越界副作用决定；多数评测没把"安全停止"与"失败"分开 [S37] | “91% 的 agent 事故源于权限过大”；把样本比例说成行业基线 |
| 压缩后约束违规 0%→30%、最差 59%、软约束衰减 8.3×、pinning 恢复 0% | ConstraintRot 在 9 任务 / 1,323 episode / 7 模型下的条件性结果，用于说明压缩是安全相关操作 [S39] | “压缩会让 30% 的请求违规”；“pin 住约束就安全了”（朴素 pinning 不阻止 operator 冒充） |
| OTel GenAI 字段落地 3/11、2/11（2026-10-30历史快照，本次未复算） | 仓库自带一致性矩阵显示 `execute_tool` 上的 `gen_ai.agent.name` 只有 3/11 库上报、`gen_ai.conversation.id` 只有 2/11 [S33] | “OTel GenAI 已经是事实标准”；把矩阵当成完整生态统计 |

> 本周排除的数字（条件不全，只可引用机制不可引用数值）：GAUGE 的 ρ=0.94 / 31% / 57.5%；STALE 的 55.2%；ATOM 的 21.7%；[S41][S42] 的 delta；以及厂商博客的 85.8% 缓存命中率与 77% 降本。
