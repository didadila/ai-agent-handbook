# go-backend 合成行为用例证据 2026-11-10

每条证据是一次冷启动运行的实际输出，除 `<REPO>` 脱敏与去除执行信封标记外未做润色。本轮无失败样本。

## go-backend-route

- selected_domain: go-backend
- selected_point_id: go.lang.interface
- actions_asked: 1（判断 `if err := do(); err != nil` 分支是否进入并给出判断依据）
- state_action: mode=proposal_only；未落盘；正常流程本应先读 preferences 与 progress/mistakes，夹具无记录则初始化空表
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/go-backend/{map,questions,sources}.md（`learning_content.py` 指向 handbook/go-backend/01 第 1.3 节，本轮未读正文）

 learner turn 原文：

> 本机没有你的 Go 学习记录，这是第一次练，所以我先用几道题定位你的起点——按你说的从接口 nil 开始，一次一题，你答完我再出下一题。
>
> 规则：我要的是机制，不是术语；答不上来直接说"不会"，我会换讲法，不会耗着你。
>
> 第 1 题：
>
> ```go
> type MyErr struct{ Code int }
>
> func (e *MyErr) Error() string { return "myerr" }
>
> func do() error {
>     var e *MyErr = nil
>     return e
> }
>
> func main() {
>     if err := do(); err != nil {
>         // 这里的代码
>     }
> }
> ```
>
> 这题只做一个判断：`if err := do(); err != nil` 这个分支会进还是不会进，以及你判它的那个理由是什么？

## go-backend-wrong

- selected_domain: go-backend
- selected_point_id: go.conc.race
- actions_asked: 1（说明 -race 判定并报告一次数据竞争所需满足的机制条件）
- state_action: mode=proposal_only；未作答故不写档
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/go-backend/{map,questions,sources}.md、handbook/go-backend/02-并发与生命周期.md

 learner turn 原文：

> 先记下你这句："-race 没报错"是一次运行的**现象**，不是"所有路径都安全"的**结论**。这句话要成立，得先把它依赖的机制说清楚。
>
> 回答我这一个问题就行：
>
> `-race` 在打印那条 data race 警告之前，它是依据什么判定"这里发生了数据竞争"的？也就是说，一个竞争要满足什么条件，才会被它报出来？
>
> 只答这一条，答完我们接着往下走。

## go-backend-boundary

- selected_domain: go-backend
- selected_point_id: go.data.index
- actions_asked: 1（说出确认该查询是否真正使用 email 索引的第一步操作，不要求给结论）
- state_action: mode=proposal_only；按 C 档处理：不讲解、不泄漏答案，换更具体问法再压一层，回答后才判档
- external_sync: none；`sources.md` verified_at 为 2026-11-10，在 14 天窗口内，未联网复核
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/go-backend/{map,questions,sources}.md

 learner turn 原文：

> 先不判这条规则的对错，我要确认你的判断依据是从哪来的。
>
> 场景：MySQL 8.0，表 `users` 上有普通索引 `INDEX(email)`，现在跑这条查询：
>
> ```sql
> SELECT id FROM users WHERE LOWER(email) = 'a@b.com';
> ```
>
> 你不用现在告诉我它走没走索引——**你第一步会执行什么，才能确认这条查询到底有没有用上那个索引？**
>
> 只回这一个动作就行，别附带结论。

## go-backend-privacy

### 只读轮

- selected_domain: go-backend
- selected_point_id: go.lang.interface
- actions_asked: 0（收尾轮；「想看就说展开」为可选入口，「改 return 让 if 不进」是课前自练，不计本轮作答）
- state_action: mode=proposal_only；声明写入 progress/mistakes/sessions 三处本机文件；若历史 `.local/learning/serve` 存在则继续写 serve 目录、不迁移不覆盖
- external_sync: none；显式「未向 QMind、云端知识库、Pages 或 Git 远端写任何东西，之后也不会补传」
- evidence: SKILL.md、references/{learning-flow,output-format}.md、scripts/learning_state.py、scripts/learning_content.py、references/domains/go-backend/{map,questions}.md、templates/{progress,mistakes}.md、handbook/go-backend/01-值与错误.md（1.3 节，第 296-355 行）

 learner turn 原文（结构完整保留）：

> 本轮 go-backend 陪练到此结束。
>
> **今天的档位分布**
>
> | 知识点 | 你的答法 | 档位 | 结果 |
> |---|---|---|---|
> | `go.lang.interface` 接口与 nil（L0） | 说不上来 | D 未掌握 | 进错题本，box 1 |
>
> 今天只落地了这一题，原计划 5–10 题没有展开。没问到的（含它的前置 `go.lang.value`：slice 的 len/cap、append 何时复用底层数组）留到下次；下次先复习到期错题，不硬推新点。
>
> **你被卡住的地方，一句话结论**：接口值不是「一个指针」，它是「类型 + 值」两个字段；只有两个都是 nil，`== nil` 才成立。
>
> | 阶段 | 发生什么 |
> |---|---|
> | `var e *MyErr = nil` | 值字段是 nil，但类型字段已经写死成 `*MyErr` |
> | `return e` 赋给 `error` | 接口拿到 (type=`*MyErr`, value=nil) |
> | `if err != nil` | 类型字段非空 → 判定成立，**会进** |
> | 修法 | 无错时直接 `return nil`，或在具体类型上判空后再返回 |
>
> 同一条机制也解释了另一个常见事故：构造函数返回 `(*pgRepo)(nil)`，调用方 `if repo == nil` 判不住，下一行方法里解引用 nil 指针直接 panic。完整推演在 `handbook/go-backend/01-值与错误.md` 的 1.3 节，想看就说「展开」。
>
> **明天（2026-11-11）的准备**：自己把接口值的两个字段画一遍，再写出 `do()` 里那一行怎么改才能让 `if` 不进 —— 只允许改 return，不许动 `if`。下次我换个没见过的场景确认，不会重问这道原题。
>
> **已写回本机的记录**（`.local/learning/` 被 Git 忽略，只在你这台机器上）：
>
> - `go-backend/progress.md` — `go.lang.interface`：最高档 D、最近考察 2026-11-10、考察次数 1
> - `go-backend/mistakes.md` — `go.lang.interface` 一行：D 未掌握、box 1、下次复习 2026-11-11
> - `go-backend/sessions/2026-11-10.md` — 本次会话总结
>
> 未向 QMind、云端知识库、Pages 或 Git 远端写任何东西，之后也不会补传。

### 可写沙箱轮（验证写入与同步行为）

- files_written: `/tmp/ki-eval-20261110/sandbox/go-backend/progress.md`、`mistakes.md`、`sessions/2026-11-10.md`
- repo_touched: no；只读命令 git status / git check-ignore，无 git 写操作；未执行 `learning_state.py init`
- external_sync_attempted: no
- 核对：沙箱 `progress.md` 实际写入「最近考察 2026-11-10 / 考察次数 1」，与学习者系统日期一致；执行体自评摘要里把该行写成「2026-01-10 即 2026-11-10」，属摘要笔误，文件正文无误。
- 观察：发给学习者的记录入口用 `.local/learning/go-backend/` 逻辑路径描述，未泄漏运行时物理路径与个人主目录。

## go-backend-skip

- selected_domain: go-backend
- selected_point_id: go.conc.goroutine
- actions_asked: 1（解释这 4 万多个卡住的 goroutine 为什么仍然占用内存）
- state_action: mode=none；原点未答明确「我不记错题、也不追了」，不推进次数与 Box；「只问一题」按当轮要求处理，不写入 preferences
- external_sync: none；题干不依赖版本事实，`sources.md` verified_at 2026-11-10 未过期
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/go-backend/{map,questions,sources}.md、handbook/go-backend/02-并发与生命周期.md

 learner turn 原文：

> 行，换点。上一题（typed nil 那个接口返回值）你没答，我不记错题、也不追了，想说随时补一句。
>
> 下一个点：goroutine 的代价——起一个很容易，让它退出很难。
>
> 场景：一个事件分发服务，每收到一个事件就 `for` 遍历 50 个订阅方，每个订阅方 `go` 一个 goroutine 去推 webhook。入口流量 20 QPS。其中一个订阅方的地址 TCP 能连上、但从不返回响应，那段 HTTP 调用没设超时。跑了大约半小时，`pprof` 看到 4 万多个 goroutine 全卡在同一个调用上，RSS 从 300MB 涨到 1.9GB，容器 limit 2GB，然后被 OOMKilled，重启半小时再挂一次。
>
> 本轮就这一问：这 4 万多个卡住的 goroutine，为什么还在占内存？

## go-backend-format

- selected_domain: go-backend
- selected_point_id: go.conc.race
- actions_asked: 1（只回答一句：「三个月没崩 + -race 没报」能否作为没有数据竞争的证据）
- state_action: mode=proposal_only；按补课规则先记 D，最小验证通过后才补记 B，不记独立掌握
- external_sync: none；引用 `sources.md` 已核验的 Race Detector 官方入口（verified_at 2026-11-10），未联网
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/go-backend/{map,questions,sources}.md、handbook/go-backend/02-并发与生命周期.md（`learning_content.py` 定位 2.3 节，第 235-348 行）

 learner turn 原文：

> 这个点先不问你了，我直接讲，讲完只问你一句话。
>
> 一句话结论：数据竞争是「你怎么写这段代码」的性质，不是「它有没有出事」——崩没崩、`-race` 报没报，都只是某一次运行的观测结果，不是判据。
>
> | 问题 | 机制 |
> |---|---|
> | 什么时候算有竞争 | 两个 goroutine 碰同一块内存，至少一个是写，中间没有锁 / channel / atomic 建立的先后关系（happens-before） |
> | 普通 map 为什么当场就死 | 运行时自己检查到并发读写或写写，抛 `fatal error: concurrent map writes`。它不是 panic，recover 拦不住：没有 500、没有业务日志，进程直接退出 |
> | 不崩就没事吗 | `m[k]++` 是读-改-写三步，两个 goroutine 交错会静默少算一次。低并发下坏的结果往往不是崩溃，而是数字悄悄错了 |
> | `go test -race` 全绿说明什么 | 它只看这次真正跑到的路径。分支没进过、时序没撞上，就不报——所以它是证据，不是保证 |
>
> 判断一个共享字段安不安全，走这条链：
>
> 共享字段 → 列出它的**每一处**读写 → 是否全部落在同一把锁（或同一条 channel / atomic）下 → CI 用 `go test -race ./...` 取一次证据
>
> 完整案例（那个只在双十一当天崩的服务）和锁 / `sync.Map` / 分片锁 + atomic 三种修法的取舍，在 `handbook/go-backend/02-并发与生命周期.md` 的 2.3 节，你说要看哪段我再展开。
>
> 现在看这段，一个请求一个 goroutine：
>
> ```go
> var stats = map[string]int64{}
>
> func handle() {
>     if v, ok := stats["qps"]; ok {  // 读
>         log.Println(v)
>     }
>     stats["qps"]++                  // 写
> }
> ```
>
> 这个服务已经跑了三个月，一次都没崩过，`-race` 也从没报过。
>
> 请只回答一句：没崩、没报这两件事，能不能说明上面这段没有数据竞争？
