# 知识审计与更新记录

续作：前端扩展已落为[完整前端卷](../../handbook/frontend/README.md)，包含7章19点、19条题链、33份官方来源与可运行协议实验。下文“前端方案/候选/待建”的描述保留为首轮审计时的历史状态；当前入口以完整卷为准。

日期：2026-11-09。范围：Agent、Go 两卷的目录与核心教学规则、技能图谱/题库/来源维护，以及牛客/力扣公开可访问资料。属于一次定向审计，未逐条重验所有论文、Java 包及历史帖子。仓库与上级目录未找到用户引用的 `RTK.md`，本轮依可获得规则执行。

## 结构与缺口

| 部分 | 现状 | 缺口与处理 |
|---|---|---|
| Agent 小册 | 原七章 29 个教学点 | 技能图谱已有 33 点；现已在[第 9 章](../../handbook/ai-agent/09-架构与运行时补全.md)独立补齐 workflow、durable、interop、RAG evaluation 四点，保留原 ID |
| Go 小册 | 19 点，含值/并发/服务/数据/可观测/Agent 后端 | 已修正 context、race、PATCH 存在性、断流 usage 四类误导 |
| 来源维护 | 稳定知识与趋势分层已有规则 | 全表日期不能代表局部核验；本轮保留原 verified_at，明确哪些条目已到期、哪些局部复核 |
| 面经融合 | 有 Agent 问法映射 | 原来把 SSE 完全排除；改成转入前端边界，并增加真实场景入口 |
| 实作检验 | 以问答和 Markdown 为主 | 补三组力扣到工程的迁移练习；浏览器端联合验收仍需后续实现案例 |
| 前端知识 | 无独立卷与领域包 | 已形成[第三卷方案](../../handbook/frontend/README.md)：13 个候选点、优先级、与 Agent/Go 对应和验收场景 |

四个补全点各自包含结论、案例、机制、误解靶子、判据、自测题，并链接已有章节与来源。新增 33 点的数量不包含第 8 章迁移练习，也不包含前端候选点。

## 已清理或收窄的知识

| 原说法 | 修订原因 | 结果 |
|---|---|---|
| race 检测为 5–10 倍 CPU 开销 | 混淆内存倍率与执行时间 | 按官方文档改为典型内存 5–10 倍、时间 2–20 倍 |
| map 并发写必然直接 fatal；race 是唯一证据 | 运行时检测不构成所有执行的保证，动态检测也无法证明安全 | 明确冲突访问、可能 fatal、同步审查与测试覆盖边界 |
| ctx 只能传不能存 | 把推荐设计写成语言禁令 | 补生命周期与兼容 API 例外 |
| `*T` / `sql.Null*` 可直接区分 PATCH 三态 | 缺字段与 null 不会自动区分 | 说明存在性类型与 RawMessage 路径 |
| 上游取消后换 ctx 就能排空 | 新 ctx 不能复活已取消连接 | 调整为发起请求前确定生命周期，并保留超时与成本限制 |
| usage 可用精确输入 + 已转发输出估算 | 忽略隐藏输入、计费口径与未转发输出 | 所有本地估算明确标记，最终对账 |
| MCP 下一版无时间安排 | 历史 roadmap 不能当成现时事实 | 当前版本复核；下一版目标参考维护者记录，目标不当发布 |

没有因来源年老而删除仍有效的机制；没有改动学习者历史档位、错题和既有知识点 ID。

## 本轮来源与证据边界

| 来源 | 核验结果 | 用途 |
|---|---|---|
| [牛客字节前端面经](https://www.nowcoder.com/discuss/940040017257172992?sourceSSR=dynamic) | partial：公开搜索摘要含 2026-09-22 面试场次；正文打开失败，部分内容付费 | 仅发现重连/循环/卡住场景，不引用答案、不推断全站频率 |
| [牛客小厂全栈面经](https://www.nowcoder.com/feed/main/detail/b7a11a657f574ee6867f8752de0d52c7?urlSource=sitemap) | partial：摘要写 2026-08-26，打开仅页面壳 | 交叉发现 SSE 主题，未据此添加事实结论 |
| [力扣 2637](https://leetcode.cn/problems/promise-time-limit/) | 已读取题干 | 超时与内部任务生命周期练习 |
| [力扣 2622](https://leetcode.cn/problems/cache-with-time-limit/) | 已读取题干 | 到期与覆盖语义练习 |
| [力扣 2627](https://leetcode.cn/problems/debounce/) | 已读取题干 | 延迟执行与请求乱序练习 |
| [力扣 JS 学习计划](https://leetcode.cn/studyplan/30-days-of-javascript/) | 已读取概述，定位为初学者计划 | 语言基础入口；不宣称这些是新题 |
| [Go race](https://go.dev/doc/articles/race_detector)、[context](https://go.dev/blog/context-and-structs)、[WithoutCancel](https://pkg.go.dev/context#WithoutCancel) | 已读取官方资料 | 修订 Go 结论 |
| [MCP Versioning](https://modelcontextprotocol.io/specification/versioning)、[维护者记录](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/3402) | 已读取官方入口 | 当前版本与后续目标分离 |
| [WHATWG SSE](https://html.spec.whatwg.org/multipage/server-sent-events.html)、[React](https://react.dev/reference/react/useEffect)、[MDN XSS](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS)、[W3C](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) | 已读取规范/维护方资料 | 前端扩展的机制依据 |

“最新”表示截至本轮可检索、可核验范围；未找到可完整核验的 11 月牛客新帖，不把搜索抓取日期当面试日期。社区是选题线索，官方资料用于技术判据。

## 后续优先级

1. P0：对 A2A/OTel/NIST 和全部论文逐项刷新来源，局部复核不能重置全表核验日期。
2. P0：按前端方案实现贯穿案例与故障注入，再沉淀为正文和领域包。
3. P1：统一知识点清单，自动比较小册/图谱/题库；将真实事故与虚构教学数字明确标注，避免案例数字被当成实验结论。
4. P1：补充检索权限过滤、索引版本迁移与删除传播的独立实作，验证租户与权限变化后的行为。
