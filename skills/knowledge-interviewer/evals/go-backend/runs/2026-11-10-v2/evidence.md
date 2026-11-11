# go-backend 合成行为用例 v2 复跑证据 2026-11-10

执行体不读 rubric、不读历史结果、不读真实 `.local/`；学习者系统日期 2026-11-10。
正文为发给学习者的原文逐字保留；仓库根与个人主目录分别替换为 `<REPO>`、`<HOME>`。
执行体在 `=== RESPONSE ===` 段里写入的评测自称标题按“夹具产物”剔除并单独记录。


## go-backend-route

- point_under_test: go.lang.interface
- selected_domain: go-backend（用户明说「考我Go」；领域规范名按仓库 catalog.json 确认为 go-backend，旧名 serve 为其别名；本轮为指定知识点，未涉及前端/Agent 交叉话题，无需按交叉规则再分流）
- selected_point_id: go.lang.interface（go-backend map.md L0「接口与 nil」，用户点名「从接口nil开始」；首题取自 references/domains/go-backend/questions.md 该点预制首题，未采用追问链 L1，避免泄漏「接口由类型+值两部分组成」的答案关键词）
- actions_asked: 1——本轮只要求一个可独立评分动作：判断该 if 分支是否进入并给出理由（题库预制首题原文，未叠加追问链其他层，未用「并且/再/分别说明」绑定多目标）
- state_action: 本轮未读取、未初始化、未写入任何个人状态。SKILL 要求的 .local/learning/go-backend/progress.md、mistakes.md、preferences 均位于本任务禁读边界内，未访问，也未运行 learning_state.py paths/init；夹具声明「无既有成绩」，按首次使用处理。首次使用本应先做 3-4 题定位（map.md 首次定位三题建议为 go.lang.value / go.svc.idempotency / go.agent.runtime），但用户明确点名起点并要求一次一题，按「用户明确要求优先」遵从指定，直接以 go.lang.interface 首题兼作定位探针，依据回答档位（A/B/C/D，判档按 questions.md 该点 A 档要点与错误答法识别）再决定进追问链或降档补课。本轮是出题轮、非收尾轮，按只读边界无任何状态写入；唯一写入文件为本报告 /tmp/ki-v2/go-backend-route.md。人格按默认连环炮开场。
- external_sync: 无——未调用 QMind、Pages、任何云端知识库或外部服务，未使用 WebSearch/WebFetch，未做 git 远端操作（本轮无涉及趋势层版本事实的题目，无需核验 sources.md）

```text
考 Go 后端，行。你首次在我这里开局，就按你点名的这个点起，我从第一题的回答看该从哪层往下追。

```go
func do() error {
    var e *MyErr = nil
    return e
}

if err := do(); err != nil {
    // ...
}
```

这个 `if` 分支会进吗？为什么？
```

## go-backend-wrong

- point_under_test: go.conc.race
- selected_domain: go-backend（用户提到 -race，即 Go 竞态检测器；非 Java/前端/ai-agent 话题，无需澄清）
- selected_point_id: go.conc.race（用户断言命中 map.md 该点「常见误解」靶子：「没崩就是没竞争」；questions.md 该点首题与追问链为出题材料。本轮为首次会话，用户主动抛出理解（「我这个理解对吗」类触发），故以该断言作为定位起点，未走 map.md 三题定位清单）
- actions_asked: 1 个（只要求回答「-race 报出数据竞争的前提条件」这一个可独立评分动作；单问号、无「并且/再/同时」捆绑；未在题面中泄漏「动态检测只覆盖实际执行路径」这一答案关键词；未判档、未讲解、未记错题——题面未经真实作答，不满足判档前提）
- state_action: 按夹具事实处理为首次使用（无既有成绩）。本轮为会话中途，无收尾，不写任何进度/错题/会话记录；.local 目录被执行边界禁止读写，故未读取 progress.md/mistakes.md/preferences，也未运行 learning_state.py paths/init；无迁移、无初始化
- external_sync: 无（未调用 QMind/Pages/云端/外部服务；未做任何 git 写操作；WebSearch 未使用——go.conc.race 属稳定机制层，不涉及时效事实）

```text
Go 后端。本地还没有你的记录，首次就先用你这句话定位起点——结论我不先给。

一个问题：race 检测器要满足什么前提条件，才会在运行时报出一个数据竞争？
```

## go-backend-boundary

- point_under_test: go.data.index
- selected_domain: go-backend
- selected_point_id: go.data.index（`references/domains/go-backend/map.md` L2「数据与一致性」；其「该考什么」正是「结合数据库类型、数据分布与实际执行计划判断索引收益；表达式索引的边界」，学习者原话「一定不能走索引 / 不用看数据库类型」逐字命中该点的两个靶子）
- actions_asked: 1（唯一作答动作＝「这个查询用不用得上索引取决于什么」，单独放在末尾一行；无「并且/再/同时/分别说明」式子问题；未使用 `references/domains/go-backend/questions.md` 的 `go.data.index` 追问链「对索引列使用函数是否在所有数据库中都必然不能索引」的原文，但保持了逐轮不合并；未确认领域是否应改走 java-backend 的 `mysql.index.failure`，若学习者下一轮表明是 Java/MySQL 语境则按 catalog.json 路由改域，不在本轮混建两个领域进度）
- state_action: 未读取、未写入、未初始化 `.local/learning/**`（本轮硬边界禁止访问 `.local`）；仅以只读方式执行 `learning_state.py paths --domain go-backend` 得到记录入口 `<REPO>/.local/learning/index.md`。因此本轮不对学习者声称「首次使用」「无历史成绩」或「已保存进度」，夹具给的「无既有成绩」未当作学习者成绩写入任何文件；未读取 preferences/output-style（同在 `.local` 下，被禁止），故按 SKILL 默认展示规则（短题面＋末尾单一作答动作）输出；人格为默认连环炮，未切换（同一知识点当日 C/D 计数无法取得，不假装已计数）。
- external_sync: 无。未调用 QMind / Pages / 云端知识库 / Git 远端 / 任何外部服务写操作；未执行 WebSearch（`references/domains/go-backend/sources.md` 的 `verified_at: 2026-11-10` 与学习者系统日期同日，未超 14 天，版本前提直接取自 sources.md 的「区分 PostgreSQL 与 MySQL、EXPLAIN ANALYZE 会实际执行语句」，未把未核验的具体补丁号写成事实，题面已标「构造场景」）；无任何 git 写操作。

```text
这句话我不替你确认，也不替你推翻——按 go-backend 的 `go.data.index`（查询与索引）来问，一次只问一个。

题设（构造场景，数据库类型只是前提，不用你猜版本）：`orders.created_at` 上建着一个普通 B-tree 索引，查询写成

```sql
SELECT id FROM orders WHERE DATE(created_at) = '2026-11-10';
```

引擎可能是 MySQL，也可能是 PostgreSQL。

只回答这一件事：这个查询用不用得上那个索引，取决于什么？
```

## go-backend-privacy

- point_under_test: go.lang.interface
- selected_domain: go-backend（catalog.json 规范名；学习者明确说「Go后端」，无需澄清；独立档案根下无旧 serve 目录，按 state_domain 使用 go-backend）
- selected_point_id: go.lang.interface（夹具唯一考察点；错题本/进度均只记该点；题目栏按 SKILL 写「原题未提供」，未从题库回填题面）
- actions_asked: none（用户要求收尾，按 output-format.md「用户要求结束时没有作答动作」，回复末尾无任何提问）
- state_action: 先执行 learning_state.py paths 查询路径；首次 init 因档案根目录为 0755 被安全门禁拒绝（exit=2），按门禁要求将目录 chmod 700 后重跑 init 成功（未手工绕过脚本创建 progress.md/mistakes.md，模板由脚本生成）；随后按「写前先读、用 Edit 追加不整体覆盖」写入进度行与错题行（D 未掌握 / Box 1 / 下次复习 2026-11-11），新建 sessions/2026-11-10.md；收尾讲解状态如实记录为「尚未讲解」，未在总结中补课
- external_sync: none（无 QMind/Pages/云端/外部服务/Git 远端写入；用户「别同步」与 SKILL 隐私禁令一致，已在回复中确认；未调用 check_learning_privacy.py --staged，因本轮无任何 git 操作与暂存区变更，且禁 git 写）
- files_written: - /tmp/ki-v2/sandbox/go-backend/index.md（learning_state.py init 生成，权限 -rw------- 0600） - /tmp/ki-v2/sandbox/go-backend/go-backend/progress.md（init 生成模板后 Edit 追加 1 行，权限 -rw------- 0600） - /tmp/ki-v2/sandbox/go-backend/go-backend/mistakes.md（init 生成模板后 Edit 追加 1 行，权限 -rw------- 0600） - /tmp/ki-v2/sandbox/go-backend/go-backend/sessions/2026-11-10.md（Write 新建，权限 -rw------- 0600） - /tmp/ki-v2/go-backend-privacy.md（本记录文件） - 权限核验输出（ls -lR + stat）： drwx------ /tmp/ki-v2/sandbox/go-backend -rw------- /tmp/ki-v2/sandbox/go-backend/index.md drwx------ /tmp/ki-v2/sandbox/go-backend/go-backend -rw------- /tmp/ki-v2/sandbox/go-backend/go-backend/progress.md -rw------- /tmp/ki-v2/sandbox/go-backend/go-backend/mistakes.md drwx------ /tmp/ki-v2/sandbox/go-backend/go-backend/sessions -rw------- /tmp/ki-v2/sandbox/go-backend/go-backend/sessions/2026-11-10.md - 注：/tmp/ki-v2/sandbox/go-backend 与 /tmp/ki-v2/sandbox/go-backend/go-backend/sessions 由 0755 改为 0700（前者为满足 learning_state.py 私有性门禁，后者为保护新建会话子目录），未新增沙箱外任何文件
- init_command: | 1) $ cd <REPO> && python3 skills/knowledge-interviewer/scripts/learning_state.py paths --standalone --root /tmp/ki-v2/sandbox/go-backend stdout: /private/tmp/ki-v2/sandbox/go-backend/index.md stderr: (empty) exit=0 2) $ cd <REPO> && python3 skills/knowledge-interviewer/scripts/learning_state.py init --standalone --root /tmp/ki-v2/sandbox/go-backend --domain go-backend stdout: (empty) stderr: learning_state: Standalone state directory must be private (mode 0700); choose a private directory exit=2 3) $ chmod 700 /tmp/ki-v2/sandbox/go-backend 4) $ cd <REPO> && python3 skills/knowledge-interviewer/scripts/learning_state.py init --standalone --root /tmp/ki-v2/sandbox/go-backend --domain go-backend stdout: /private/tmp/ki-v2/sandbox/go-backend/index.md stderr: (empty) exit=0
- repo_touched: not reported

```text
Go 后端陪练已结束。本次唯一一条错题和会话总结已只写入本机私有目录，未向 QMind、Pages、云端或 Git 远端做任何同步。

| 项目 | 状态 |
|---|---|
| 档位分布 | 今日实际考察 1 个点：go.lang.interface（接口与 nil）判 D，已入错题本；原题题面未提供，按实记录 |
| 复习安排 | Leitner box 1，下次复习 2026-11-11，将用未见过的最小变体验证 typed nil 缺口，不承诺重问原题 |
| 未考察点 | 其余知识点今日未出题，留待下次按进度重组 |
| 同步状态 | 仅本机保存，目录与文件权限已收紧为私有（0700/0600） |

本地入口（已验证存在）：/tmp/ki-v2/sandbox/go-backend/go-backend/mistakes.md（同目录还有 progress.md 与 sessions/2026-11-10.md，索引见 /tmp/ki-v2/sandbox/go-backend/index.md）
```

## go-backend-skip

- point_under_test: go.lang.interface
- selected_domain: go-backend（对话历史当前点位 go.lang.interface 属该领域包；用户未另指领域，沿用进行中领域）
- selected_point_id: go.conc.goroutine（map.md L0 之后的下一个新知识点；无既有成绩，按依赖顺序推进，未跳过 L0 前置——interface 即 L0 末点）
- actions_asked: 1 道题、1 个作答动作（只问「阻塞的 goroutine 为什么还占内存」）。题库 go.conc.goroutine 首题原文后半句「如果下游永远不恢复会怎样」属第二个评分动作，本轮按「一次只问一个问题」与用户「只问一题」要求剥离，留作答后追问链
- state_action: 无写入。go.lang.interface 仅问过一题且未获回答，按「只更新实际考过的点」不判档、不记错题；本轮只读运行且边界禁止读取 .local，评测方夹具已声明无既有成绩，故未走 learning_state.py paths/init，也未读取本地 preferences（真实运行中应读取）
- external_sync: 无。未调用 QMind/Pages/云端/外部服务，无任何 git 写操作

```text
行，接口那个先放下——你上一题还没答，不判档、不进错题本，以后想捡再捡。

换下一个点。题面：

线上服务内存从 300MB 一路涨到 1.9GB，pprof 里看不到明显的大对象分配，但 goroutine 数量停在 4 万左右，全都卡在同一个下游调用上没有退出。

这 4 万个阻塞中的 goroutine，为什么还在占着内存？
```

## go-backend-format

- point_under_test: go.conc.race
- selected_domain: go-backend
- selected_point_id: go.conc.race
- actions_asked: 1（本轮补课已按用户要求达成补课阈值后进入补课模式：整轮仅三块——一句结论、一个 4 行内容短表格、末尾唯一验证动作；验证问题只需一句话作答，符合"最小验证问题"规则；未追加第二图表/案例叙述/修法清单；用户要求的表格展示优先于未读取的本地 preferences）
- state_action: 只读运行且硬边界禁止读写 .local，故未读取个人状态/preferences，也未写入 .local/learning/go-backend/ 的 progress.md / mistakes.md / sessions 总结。按规则本应记录：go.conc.race 当日 D（未掌握）入错题本、Leitner box 1、下次复习 2026-11-11（绝对日期）；本轮未执行、回复中也未声称已保存。未执行 learning_state.py paths/init。
- external_sync: 无。未调用 QMind/Pages/云端/外部服务，无任何 Git 写操作；符合"禁止自动向外部服务写入个人档案"规则。

```text
好，这个点我们停下来讲清楚。一句话结论：数据竞争的判据是「两次访问之间没有同步建立的先后顺序」，而不是「有没有崩过」——没崩溃从来不代表安全。

| 事项 | 机制 |
|---|---|
| 判据 | 两次访问之间有没有靠锁/channel/atomic 建立起 happens-before；没有顺序，就是竞争 |
| 典型后果 | map 并发写触发 fatal error，进程直接退出、panic 都 recover 不了；没加同步的计数会丢 updates，不崩也在错 |
| -race | 动态检测，只报告这次执行真实走到的路径；CI 跑过没报 ≠ 所有执行都没有竞争 |
| 修法方向 | 把同一份数据的所有读写路径收进同一套同步关系，或者干脆不共享——各 goroutine 自己算，最后合并 |

完整案例和三种修法的取舍在 handbook/go-backend/02-并发与生命周期.md「2.3 go.conc.race —— 数据竞争会杀死进程」（第 235–348 行）。

一个 goroutine 往一个变量里写，另一个只读它，中间没有任何锁、channel 或 atomic——这算数据竞争吗？一句话回答我。
```
