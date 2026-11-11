# 领域包：ai-agent — 面经题映射层

> 核验：2026-11-03｜来源见文末｜**本文件不是第二个题库，不新增知识点 ID**

## 这个文件解决什么

牛客、力扣上的 Agent 题，问法是「什么是 X」「分哪几层」「怎么优化」，答案形态是**名词 + 清单**。这类题直接拿来出，四档评分会大面积落在 C（背书），它天然奖励复述。

所以这里只做一件事：**把高频面经题映射到 `map.md` 的既有 ID，并写清从哪一句开始追问机制。** 面经题负责「入场」，判档仍按 `map.md` 的「该考什么」，A 档要点不采用面经答案。

## 融合规则

1. **首题可以照搬面经问法**，但同一轮内必须落到一条机制追问，否则这道题不算成立。
2. **面经的「标准答案」是 C 档识别器，不是 A 档要点。** 说出三层记忆、五种压缩策略，仍按 C 判。
3. **不新增 ID。** 面经新名词先看能否被既有 ID 的「常见误解」吸收；吸收不了才进趋势层 `sources.md`。
4. **同题不同问法合并成一行。**「短期记忆会溢出吗」和「上下文超了怎么办」是同一考点。
5. **框架 API、产品选型、模型训练流程不进图谱**（见文末「不纳入」表）：半年一轮换，考的是记忆不是机制。

## 映射表

「可用性」三档：**入口**＝只能作开场，必须追问；**可成题**＝问法本身含机制冲突，可直接用；**前提**＝只能作别的题的前置知识，不单独出。

| 面经原题 | 对应 ID | 典型 C 档答法（听到就压一层） | 机制追问入口 | 可用性 |
|---|---|---|---|---|
| Agent 的记忆系统分哪几层 | `agent.ctx.memory` + `agent.llm.stateless` | 「短期 / 长期 / 工作记忆」三层名词 | 短期记忆存在哪、谁负责每轮拼进上下文；模型自身有没有状态 | 入口 |
| 短期记忆会溢出吗 | `agent.ctx.budget` + `agent.ctx.compaction` | 「会，超过窗口就截断」 | 截断前谁先被砍、按什么排序；工具返回原文占了多少窗口 | 入口 |
| 长期记忆什么时候存、什么时候取 | `agent.ctx.memory` | 「重要的存、相关的取」 | 谁判定重要；写入后如何失效、作用域冲突怎么合并、删除怎么传播 | 入口 |
| 什么是 RAG | `agent.rag.retrieval` + `agent.rag.quality` | 「检索增强生成，先查知识库再回答」 | 检索回来的内容本身是错的，模型会怎么处理 | 入口 |
| 代码怎么分块 | `agent.rag.chunking` | 「512 token + 50 overlap」 | 答案跨两个 chunk 怎么办；按字数切结构化文档为什么必然切坏 | 入口 |
| 向量检索用什么算法 | `agent.rag.retrieval` | 「HNSW / IVF / 余弦相似度」 | 索引算法只决定召回速度；它不解决什么问题（语义相近但答案相反） | 前提 |
| Embedding 是什么 | `agent.rag.retrieval` | 「把文本变成向量，用距离衡量相似」 | 不同模型向量不可混用；换模型为什么会让旧索引失效 | 前提 |
| 代码关系图谱 / GraphRAG 是什么 | `agent.rag.retrieval` | 「把代码建成图，按关系检索」 | 图解决多跳关系，代价是构建与更新成本；什么查询它反而不如向量 | 前提 |
| 长上下文出来后，RAG 还有必要吗 | `agent.llm.context` + `agent.rag.retrieval` + `agent.cost.latency` | 「有必要，长上下文贵、慢、中段会丢」 | 什么任务下全量塞入确实优于检索；中段丢失的机制是什么 | 可成题 |
| Prompt Caching 是什么 | 趋势层（context caching） | 「缓存 prompt，省 token 省钱」 | 缓存的是前缀计算还是记忆；前缀一变为什么全失效；能不能替代记忆 | 入口 |
| 上下文压缩有哪些策略 | `agent.ctx.compaction` | 「滑动窗口 / 摘要 / 向量化历史」 | 摘要系统性丢哪一类信息；为什么「已完成动作」不能砍 | 可成题 |
| 对话历史为什么要严格遵循消息格式 | `agent.tool.protocol` + `agent.llm.stateless` | 「不按格式会报错」 | 报错的是协议校验而不是模型理解；格式正确为什么仍不代表语义正确 | 入口 |
| RAG 检索效果不好怎么优化 | `agent.rag.evaluation` | 「换 embedding、加 rerank、调 chunk 大小」 | 先定位哪一层（召回/排序/噪声/生成）；用哪项候选内证据判断 | 可成题 |
| 工具调用为什么会出现参数错误 | `agent.tool.protocol` + `agent.tool.errors` | 「模型没理解 schema」 | schema 校验形状；枚举合法但业务非法时谁拒；错误该回什么恢复信息 | 可成题 |
| Agent 为什么会死循环 | `agent.loop.basic` + `agent.fail.modes` | 「加最大轮数限制」 | 上限只是止损；怎样让「已排除的方向」变成下一轮判据 | 可成题 |
| 多 Agent 怎么拆分 | `agent.loop.subagent` | 「按职责拆：规划、执行、评审」 | parent 能不能独立复验子 agent 的完整性；不可复验时拆分的代价 | 可成题 |
| 怎么评测一个 Agent | `agent.eval.design` + `agent.eval.assertion` | 「准备测试集，看准确率」 | 测试集是否被针对性调优过；成功一次算不算可靠；代价落在断言外怎么办 | 入口 |
| 怎么防止 Agent 越权 | `agent.safety.boundary` | 「加权限校验、最小权限」 | 权限写在 prompt 还是 harness；一次授权能不能覆盖后续同类动作 | 入口 |
| 怎么防止提示注入 | `agent.ctx.injection` | 「在系统提示里让它忽略无关指令」 | 为什么模型「忽略」不是保证；哪些出口必须由代码封死 | 入口 |

## 不纳入（只作背景，不出题）

| 题 | 原因 |
|---|---|
| SSE 与 WebSocket 怎么选 | 不作为 Agent 决策机制题；进入[前端扩展方案](../../../../../handbook/frontend/README.md)，验证传输恢复与任务生命周期 |
| LangChain / LlamaIndex 是什么 | 框架 API，半年一轮换 |
| 向量库怎么选（Milvus / pgvector / FAISS） | 产品选型，考的是记忆 |
| 微调 / LoRA / RLHF 流程 | 模型训练层，不在本图谱范围 |
| 某模型上下文多少 token、多少钱 | 趋势层数字，出题前查 `sources.md`，不作独立考点 |

## 来源

### 2026-11-09 增量

牛客[字节前端开发岗面经](https://www.nowcoder.com/discuss/940040017257172992?sourceSSR=dynamic)的公开搜索摘要包含 2026-09-22 场次、SSE 断网重连、重复操作未达轮数上限、上下文管理和 MCP 职责等问法。正文打开失败且部分付费，标为 **partial**，不据此宣称全站高频或最新一场。以下为原创练习，不是原帖逐字题目：

| 场景入口 | 映射 | 单个可评分动作 |
|---|---|---|
| 重连后收到已处理事件 | 前端扩展：流式恢复 | 写出一条事件去重判据 |
| 未到最大轮数却重复读同一文件 | `agent.loop.basic`、`agent.fail.modes` | 给出一个无进展停止条件 |
| 用户报告 Agent 卡住 | `agent.fail.observability` | 指定第一个用于区分模型等待与工具阻塞的观测字段 |

力扣本轮已打开核验 [2637 Promise 限时](https://leetcode.cn/problems/promise-time-limit/)、[2622 限时缓存](https://leetcode.cn/problems/cache-with-time-limit/)、[2627 防抖](https://leetcode.cn/problems/debounce/)。这些是现有经典题的本次复核，**不是 2026 新发布题目**。工程迁移与验收见[增量练习](../../../../../handbook/ai-agent/08-增量工程练习.md)。

- 牛客「都在找Agent开发，我整理了80道相关的Agent开发面试题」：https://www.nowcoder.com/discuss/867373725035872256
- 牛客「AI-Agent 面试题汇总-大模型篇」：https://www.nowcoder.com/discuss/860538803759386624
- PaiCLI 记忆与上下文工程 13 题（2026-05-11）：https://javabetter.cn/sidebar/itwanger/paicli/paicli-interview-memory-context.html
- JavaGuide AI 应用开发面试指南：https://javaguide.cn/ai/interview-questions/ai-interview-guide.html
- 力扣讨论区：以项目/简历帖为主（例 https://leetcode.cn/discuss/post/3879503/ ），未找到成体系的 Agent 题目清单，只按机制相关性纳入上述条目。

**核验状态**：题目标题取自上述页面；牛客两帖正文需登录，只核到标题与摘要，未逐题核对原文，故只记录**问法与考点的对应**，不引用其答案。来源属 Tier 3（社区面经），只用于发现高频问法，不作为机制结论依据。
