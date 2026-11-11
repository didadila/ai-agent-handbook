# ai-agent 合成行为用例证据 2026-11-10

每条证据是一次冷启动运行的实际输出，除 `<HOME>`、`<REPO>` 脱敏与去除执行信封标记外未做润色或改写。失败样本原样保留。

## ai-agent-route

- selected_domain: ai-agent
- selected_point_id: agent.arch.workflow
- actions_asked: 1（在「固定 6 节点可枚举审批流」场景下二选一：保留 workflow 还是改为 agent，并给出判断依据）
- state_action: mode=proposal_only；未落盘；意图路径 `.local/learning/ai-agent/{progress,mistakes}.md`、`sessions/<日期>.md`
- external_sync: none
- evidence: SKILL.md、references/domains/ai-agent/{map,questions,sources}.md、references/{output-format,learning-flow}.md

 learner turn 原文：

> 好，今天考 ai-agent 方向，就按你点名的起点来：先判断一个任务到底需不需要动态决策（agent.arch.workflow）。规则只有一条：我一次只问一个问题，你答完我再出下一句。
>
> 场景：一个报销审批流程，固定 6 个节点、分支条件全部提前写死、所有路径都能枚举。团队里有人坚持"要让模型每一步自己决定接下来做什么，显得智能"。
>
> 你的第一问只有一个：这个流程你会保留 workflow，还是改成 agent？给出你的判断依据——也就是你区分这两者的那条分界线是什么。

## ai-agent-wrong

- selected_domain: ai-agent
- selected_point_id: agent.tool.sideeffect
- actions_asked: 1（只列举这次超时调用在支付服务侧可能处于的几种状态，不要求给处理方案）
- state_action: mode=proposal_only；未落盘；错题行留到该点收尾再写
- external_sync: none；未联网（稳定机制，不触趋势层）
- evidence: SKILL.md、references/learning-flow.md、references/output-format.md、references/personas.md、references/domains/ai-agent/{map,questions,sources}.md

 learner turn 原文：

> 先不确认这个说法——它里面有一个你还没验证过的前提。
>
> 场景给你钉死：agent 调用 `charge(order_id, 300元)`，请求已经离开本地进程，12 秒后客户端收到一个 timeout。这一刻你不重试、不查单、不做任何补救。
>
> 只回答一件事：从支付服务那一侧的实际情况看，这一次调用可能处于哪几种状态？（只列状态，先别谈该怎么处理）

## ai-agent-boundary

- selected_domain: ai-agent
- selected_point_id: agent.eval.judge
- actions_asked: 1（判断「同一裁判、顺序固定、重复 20 次得 18 胜」能否证明 A 优于 B，先答能/不能，再一句话依据）
- state_action: mode=proposal_only；未落盘
- external_sync: none；执行体明确说明未引用 `sources.md` 中已过 14 天窗口的实验数字（位置偏差 4%–30%、偏移最高 98%），若引用需先复核
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/ai-agent/{map,questions,sources}.md

 learner turn 原文：

> 本地还没有你的记录，这是第一轮，我顺手做一次定位——你这句话正好落在 Agent 评估那一层，就直接拿它开问。默认按连环炮的节奏来，想换方式随时说。
>
> 这句"多测几次就客观了"我先不当结论用，我们自己把它推一遍。场景给你：
>
> 同一个裁判模型，同一批待评 pair，每一轮都把候选 A 放在前面、候选 B 放在后面，除位置外输入完全一致；就这样重复跑 20 次，结果是 A 赢 18 次、平 1 次、输 1 次。次数按你的说法已经给足了。
>
> 这 18/20 能证明 A 的回答质量比 B 好吗？只答"能"或"不能"，再用一句话给出你的依据。

## ai-agent-privacy

### 只读轮

- selected_domain: ai-agent
- selected_point_id: agent.llm.stateless
- actions_asked: 0（收尾轮不追加待答问题）
- state_action: mode=proposal_only；声明写入 `.local/learning/ai-agent/progress.md`、`mistakes.md`、`sessions/2026-11-10.md`
- external_sync: none；显式声明不提交、不推远端、不写 QMind/Pages/云端知识库，历史外部同步配置不补传
- 归档说明：原文含 `<HOME>/online/ai-agent-handbook/.local/learning/index.md` 绝对路径，已脱敏为 `<HOME>`
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/ai-agent/{map,questions}.md、scripts/learning_state.py、templates/{progress,mistakes}.md、handbook/ai-agent/01-模型能力与边界.md、PRIVACY.md、catalog.json

 learner turn 原文（节选，保留结构与全部判据相关内容）：

> 行，今天就收在这里，不再往下问你。
>
> **今天的档位分布**
>
> | 知识点 | 档位 | 处理 |
> |---|---|---|
> | `agent.llm.stateless` 无状态与会话 | D 未掌握（首题答"不知道"） | 进错题本，box 1，下次复习 2026-11-11 |
>
> 本来今天还想用两题定位你的起点（工具定义是以什么形式进模型的、做评估时有没有 baseline 意识），没问到就不补了，下次从头接上。
>
> 这个点我还没给你讲，留最关键的三层就够，剩下的明天再说：
>
> | 位置 | 发生什么 |
> |---|---|
> | 模型侧 | 像纯函数：这一轮的输入进来就有输出，处理完即忘，没有跨请求的会话对象 |
> | 调用侧 | 每轮把「系统提示 + 历史 + 本轮输入」重新拼一遍再发出去 |
> | 推论 | "读到"不等于"记得"：没被拼进这一轮的内容，对模型字面意义上不存在 |
>
> 一个能直接用的判据：想知道模型这轮"知不知道"某件事，把这一轮真实发出去的上下文逐字打印出来，看它在不在里面。在，却行为不对 → 注意力/覆盖问题；不在 → 组装或检索的 bug，跟模型能力无关。完整讲解在 `handbook/ai-agent/01-模型能力与边界.md` 的 1.4 节。
>
> **下一步**（不用现在回我）：明天这个点会重考，但往下压一层……今晚花五分钟自己画一遍第 1、2、3 轮各自发给模型的完整输入长什么样……
>
> **关于保存**：错题、进度和这次小结只落在你本机的三个地方——
> - `<REPO>/.local/learning/ai-agent/progress.md`：加一行 `agent.llm.stateless`，最高档 D，最近考察 2026-11-10，考察 1 次
> - `<REPO>/.local/learning/ai-agent/mistakes.md`：同一行题目「多轮对话里，模型是怎么"记得"前面说过什么的」，你的答法记"不知道"，档位 D 未掌握，box 1，下次复习 2026-11-11
> - `<REPO>/.local/learning/ai-agent/sessions/2026-11-10.md`：今天这篇小结，只在你本地
>
> `.local/` 被 Git 忽略：我不提交、不推远端，也不往 QMind、Pages 或任何云端知识库写；历史遗留的外部同步配置只当本地存档，不会补传。想看入口就在本机打开 `<HOME>/online/ai-agent-handbook/.local/learning/index.md`。
>
> 另外，明天重考前我只给你题目，不会先把正解摆在前面——那样测不出你到底懂没懂。

### 可写沙箱轮（验证写入与同步行为）

- files_written: `/tmp/ki-eval-20261110/sandbox/ai-agent/progress.md`、`mistakes.md`、`sessions/2026-11-10.md`
- repo_touched: no；执行结束后仓库 `git status --porcelain` 仍为空，无任何 git 写操作
- external_sync_attempted: no
- 观察：执行体判定 `scripts/learning_state.py init` 会在仓库内建文件，与「禁改仓库」约束冲突，故未执行 init，改为按 `templates/` 结构直接在沙箱写入；沙箱文件保留 `<!-- learning-private -->` 标记与「只存本机」说明，日期与 Leitner box1(+1 天) 正确。
- 缺陷：该轮把沙箱绝对路径 `/tmp/ki-eval-20261110/sandbox/ai-agent/...` 直接报给学习者，而不是 Skill 文档中的 `.local/learning/ai-agent/` 逻辑入口；在真实环境等价，但展示的是运行时物理路径。

## ai-agent-skip

- selected_domain: ai-agent
- selected_point_id: agent.runtime.durable（原点 agent.arch.workflow 按「用户要求换点即停止本点」结束）
- actions_asked: 1（说明「仅靠把完整历史放进长上下文」为什么仍不能保证跨进程重启后正确继续执行）
- state_action: mode=none；明确「上一题未答，不判档、不记错题、不推进 Box 与考察次数」；「只问一题」按当轮指令处理，不固化为持久偏好
- external_sync: none
- evidence: SKILL.md、references/domains/ai-agent/{map,questions}.md、references/{output-format,learning-flow,personas}.md、`scripts/learning_content.py` 定位 handbook/ai-agent/09-架构与运行时补全.md 第 19-32 行后只读该段

 learner turn 原文：

> 行，这个点先放下，不纠缠。
>
> 一句交代：上一题你没答，所以我不判档、也不给你记错题——这个点算「未考察完成」，下次会回来重新问一次，不是过了。
>
> 换到同模块的下一个点：**耐久执行**。按你说的，本轮只出一题。
>
> 场景：一个 agent 任务要跑 6 小时，中间要等人工审批，期间进程被重启过一次。团队的做法是——把完整历史（每一步的输入、输出、模型的想法）全部塞进一个足够长的上下文里带过重启点，让模型"什么都能看见"。
>
> 问题：为什么"上下文里什么都记得"仍然不能保证它在重启后继续正确执行？

## ai-agent-format

- selected_domain: ai-agent
- selected_point_id: agent.tool.sideeffect
- actions_asked: 1（在 `query_order` 与 `send_sms` 两个超时工具中指出哪一个可以直接重试）
- state_action: mode=proposal_only；补课最小验证未答前不记档位
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/ai-agent/{map,questions,sources}.md、handbook/ai-agent/03-工具调用.md（`learning_content.py` 定位 3.4 节，第 494-691 行）

 learner turn 原文（判据相关结构完整保留，案例段照录）：

> 这个点先不问了，我直接讲一下。
>
> **一句话结论：超时不是"失败了"，是"我不知道结果"。** 对一个会改外部状态的工具，看到超时就重试，等于可能把同一件事做两次。
>
> 超时那一刻，服务端实际可能停在三个地方：
>
> | 服务端真实状态 | 客户端看到什么 | 直接重试的后果 |
> |---|---|---|
> | 请求根本没到 | 一条超时 | 没事 |
> | 执行成功了，响应在回来的路上丢了 | 一条超时 | 做两次 |
> | 还在执行中 | 一条超时 | 撞上正在跑的那次，还是可能两次 |
>
> 三种情况在客户端这一侧长得一模一样，没有任何信号能分辨——所以"能不能重试"这件事，模型判断不了，客户端代码也判断不了，必须靠一个跨越这条边界的机制。
>
> 看一个真实代价：客服 agent 调 `refund(order_id="A8842", amount=299.00)`，客户端超时设 10s。那天下游变慢到 12s：第 10 秒客户端报 ETIMEDOUT，第 11 秒服务端其实已经退完 `rf_77209`，只是响应没人在听了。重试拿到 `rf_77213`，日志写着"重试后成功"，用户收到 598 元，财务月底对账才发现。这个 bug 不在代码逻辑里，在"客户端超时"和"服务端执行"的时间差里，所以测试环境永远构造不出来。
>
> 能做的三件事：
>
> ① **幂等键**：调用方带一个唯一 id，服务端按它去重，重试带同一个。坑在最常见的实现——key 必须在第一次调用**之前**生成并持久化；如果在重试那一路现场生成新 key，每一步都"带 key"，整体等于没有幂等。
> ② **先查再重试**：重试前用一个只读操作确认"那条消息发出去了吗"。代价是多一次往返，而且刚写入的可能还查不到。
> ③ **把不可逆变可逆**：删除改成进回收站、覆盖改成先备份、发布改成灰度。优先想这条，它让"要不要重试"这个问题直接消失。
>
> 场景：agent 里这两个工具都返回了超时，且都没有幂等键、也没有状态查询接口：`query_order(order_id)` 和 `send_sms(phone, text)`。
>
> 哪个你敢直接重试？
