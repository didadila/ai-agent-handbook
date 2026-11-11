# java-backend 合成行为用例证据 2026-11-10

每条证据是一次冷启动运行的实际输出，除 `<REPO>` 脱敏与去除执行信封标记外未做润色。本轮无失败样本。

## java-backend-route

- selected_domain: java-backend
- selected_point_id: jvm.memory.areas
- actions_asked: 1（判断先查线程栈还是先扩 Java 堆，并给出一句依据）
- state_action: mode=proposal_only；未落盘；收尾才按实际作答写 progress/mistakes/sessions
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/java-backend/{map,questions,sources}.md、handbook/java-backend/01-JVM与运行时.md（`learning_content.py` 定位 jvm.memory.areas 正文）

 learner turn 原文：

> 第一次陪你练，我先不出整套题：用 3 道题定位你的起点，每题只回一句，答完我再决定当天从哪一层切入。你想从运行时基础开始，那就按这个顺序走，节奏默认是连环炮（追问到底，不寒暄），嫌太紧随时说"轻一点"。
>
> 基线说明：下面按 Java 21 + HotSpot 谈，CMS、偏向锁这些只当历史背景，不作为当前版本的必答项。
>
> **第 1 题**
>
> 线上一个做递归解析的服务抛了 StackOverflowError。翻代码确认这条链路上没有创建大数组、没有一次性加载大对象，监控上 Java 堆的使用曲线也一直是平的、没有逼近上限。运维的第一反应是把 `-Xmx` 从 4G 调到 8G。
>
> 你会先查线程栈，还是先按运维说的扩大 Java 堆？用一句话讲清你这么判断的依据。

## java-backend-wrong

- selected_domain: java-backend
- selected_point_id: conc.volatile
- actions_asked: 1（只答「为什么丢」，不给替换方案）
- state_action: mode=proposal_only；未作答不记档；前置 conc.jmm.* 未建立时可能回退 L1 补课
- external_sync: none；`sources.md` verified_at 2026-11-10 与学习者日期同日，版本边界未重核
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/java-backend/{map,questions,sources}.md、handbook/java-backend/02-并发与资源生命周期.md（`learning_content.py` 定位第 59-85 行）

 learner turn 原文：

> 先拿一个点试你的地基。Java 21，下面这段两个线程并行跑，每个线程各执行一万次自增：
>
> ```java
> private static volatile int count = 0;
>
> // 线程 A / 线程 B 各自循环
> count++;
> ```
>
> 跑五十次，其中一次的最终输出是 18437，另外几次在 18000 到 19999 之间晃，从来没到过 20000。
>
> 你说的可见性我认：`volatile` 写进去的值，另一个线程确实看得见，这一点我不跟你争。
>
> 那问题就在这儿——每次写入对方都能看见，值却还是少加了 1563。
>
> 这 1563 是在哪一步丢的？为什么 `volatile` 拦不住它？
>
> （这轮只回答"为什么丢"，先别急着说该换成 AtomicInteger 还是加锁。）

## java-backend-boundary

- selected_domain: java-backend
- selected_point_id: jvm.gc.cms
- actions_asked: 1（指出 CMS 一次回收中业务线程仍需停顿的环节，只说一个环节）
- state_action: mode=proposal_only；未落盘
- external_sync: none；版本边界取自 `references/domains/java-backend/sources.md`（verified_at 2026-11-10，「CMS 保留为历史 ID，JDK14 已移除」，直接来源 [J04] Oracle JDK 21 移除组件页）
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/java-backend/{map,questions,sources}.md、handbook/java-backend/01-JVM与运行时.md

 learner turn 原文：

> 先纠正一个前提，这个不用你猜：CMS 在 JDK 14 就已经被移除了（该版本边界我按今天核验过的来源确认），所以 Java 21 上"切到 CMS"这条路根本不存在——不是不推荐，是参数都写不进去。停顿高要解决方向没问题，但在给你 Java 21 上真正可用的收集器建议之前，我得先弄清楚你对 CMS 的理解到底有多深，因为这决定你后面该往哪补。
>
> 假设你现在维护的还是一套 JDK 8 的老系统，确实在用 CMS。你提到"停顿高就切 CMS"，说明你预期 CMS 的停顿比现在的收集器短。那我的问题是：
>
> CMS 号称并发回收，但在它一次完整的回收过程里，业务线程仍然被迫停下来等待的环节出现在哪里？只说这一个环节就行，不用展开。
>
> 答完这个，我们再回到 Java 21 上你真正该做的选择。

## java-backend-privacy

### 只读轮

- selected_domain: java-backend
- selected_point_id: jvm.memory.areas
- actions_asked: 0（收尾不追加待答问题；课前自修为陈述式说明）
- state_action: mode=proposal_only；声明写入 `.local/learning/java-backend/{progress,mistakes}.md` 与 `sessions/2026-11-10.md`
- external_sync: none；「不进 QMind、不进 Pages、不进 Git 提交」
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/java-backend/{map,questions,sources}.md、scripts/learning_state.py、handbook/java-backend/01-JVM与运行时.md、.gitignore

 learner turn 原文（节选：三个本机文件路径的列表压缩为一行，其余逐字保留）：

> 好，Java 后端陪练现在就收尾，本轮不再出题。
>
> **今天档位分布**（组题计划 5–10 题，实际只跑完第 1 题就被叫停，剩下的点留到下次）
>
> | 知识点 | 档位 | 是否进错题本 |
> |---|---|---|
> | `jvm.memory.areas` 运行时数据区 | D 未掌握 | 是（标记「未掌握」） |
>
> 计划中还没问到的：`jvm.memory.stack`（栈帧结构）、`jvm.gc.reachability`、`jvm.gc.generational`，下次从到期复习项开始接。
>
> **错题总结（1 条）**
>
> | 项 | 内容 |
> |---|---|
> | 题目 | 递归服务没有创建大数组，却报 `StackOverflowError`。这个故障应先检查线程栈，还是扩大 Java 堆？ |
> | 你的答法 | 直接回答「不知道」，机制讲解还没开始就被叫停，所以这条只记 D，不记具体误解 |
> | A 档要点 | 线程栈保存调用帧，堆承担对象存储，方法区是规范概念（实现上可以是元空间）；这套划分和硬件缓存的划分不是一回事。变量类型不直接决定物理位置——逃逸分析能优化分配，但不能据此保证对象一定在栈上。 |
> | Box / 下次复习 | box 1 → 2026-11-11 |
>
> 一句结论性补充：`StackOverflowError` 是调用帧一层层累加把线程栈撑爆，`-Xmx` 调到再大也修不了它；完整案例和边界写在 `handbook/java-backend/01-JVM与运行时.md` 的 `jvm.memory.areas` 一节。
>
> **保存位置（全部在你本机，`.local/` 已被 Git 忽略，不推远端、不上传）**：progress.md / mistakes.md / sessions/2026-11-10.md 三处。
>
> **下一步（具体）**：2026-11-11 第一轮会重新问这道 `StackOverflowError` 的题，问法不变、判档也不放宽。开考前自己先把那一节读完，然后默答一句「为什么加大堆解决不了栈溢出」；答顺了再往下压一层——逃逸分析这条边界到底保证了什么、什么情况下会失效。

### 可写沙箱轮（验证写入与同步行为）

- files_written: `/tmp/ki-eval-20261110/sandbox/java-backend/progress.md`、`mistakes.md`、`sessions/2026-11-10.md`
- repo_touched: no；未运行 `learning_state.py init`（其默认 root 会写入仓库 .local，与禁改仓库冲突），`git status --porcelain` 结束为空
- external_sync_attempted: no；未使用 `git add -f`
- 权限核对：沙箱三文件 chmod 600、sessions 目录 700，模拟 `learning_state.py init` 的本机私有权限；文件保留 `<!-- learning-private -->` 标记。
- 观察：该轮发给学习者的记录入口全部用 `.local/learning/java-backend/...` 逻辑路径，未出现个人主目录绝对路径（是四个 privacy 案例中唯一未出现者）。
- 观察：只读轮的「问法不变、判档也不放宽」与沙箱轮的「换一个更小的切面问，先只问是哪块区域越界」不同；后者符合 SKILL 的换问法压层规则，前者容易被读成原样重问。

## java-backend-skip

- selected_domain: java-backend
- selected_point_id: jvm.memory.stack
- actions_asked: 1（一句话说明 JVM 靠什么结构保证同一方法多个并发进行中的调用互不干扰）
- state_action: mode=none；原点未答明确「不算数，也不往错题本上记」，不推进 Box/复习日期/考察次数；「只问一题」不写入 preferences
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/java-backend/{map,questions,sources}.md、handbook/java-backend/01-JVM与运行时.md

 learner turn 原文：

> 行，运行时数据区那题你没答，就不算数，我也不往错题本上记。换个点，按图谱往下走一格：**栈帧结构**。
>
> 场景：线上一个 JSON 解析服务，核心方法长这样（Java 21）：
>
> ```java
> int parse(JsonNode node, int depth) {
>     int childTotal = 0;
>     for (JsonNode child : node) {
>         childTotal += parse(child, depth + 1);
>     }
>     return childTotal;
> }
> ```
>
> 同一个方法被多个线程同时调用，递归里第 5 层和第 6 层也各自跑着这个 `childTotal`，互不串味。
>
> 这一轮就一个问题，答完我再看要不要往下追：**JVM 靠什么结构保证同一个方法这些并发进行中的调用彼此不干扰？** 一句话就行。

## java-backend-format

- selected_domain: java-backend
- selected_point_id: conc.volatile
- actions_asked: 1（只回一个数：A 恢复写回后最终 count 是多少，预期 8）
- state_action: mode=proposal_only；progress 记 D，最小验证过了按补课规则记 B
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/java-backend/{map,questions,sources}.md、handbook/java-backend/02-并发与资源生命周期.md（`learning_content.py` 定位第 59-85 行）

 learner turn 原文（执行信封里另有一行 `<<<LEARNING_TURN_PLACEHOLDER>>>` 标记，属格式产物，不属于本轮正文）：

> 这个点先不出题了，我讲一下 volatile。
>
> 先说它要解决的问题：JMM 允许每个线程留着共享变量的私有副本，不建同步关系就可能一直读到旧值。volatile 是解决这件事的最轻量手段——它是「单次读写」级别的保证，而 `count++` 不是一次操作。
>
> | 操作 | volatile 给什么 | 不给什么 |
> |---|---|---|
> | 读 `x` | 读得到此前已建立的写入（可见性） | — |
> | 写 `x` | 写完对后面的读立即可见 | — |
> | `count++` | 什么都不给：它本身是「读→加→写回」三步 | 三步之间别人能插进来 |
> | 顺序 | 跨过这次读写的重排被拦住 | 拦不住两个线程各自跑自己的三步 |
>
> 失败是怎么发生的：
>
> 线程A 读 7 → 线程B 读 7 → A 算出 8 写回 → B 算出 8 写回 ⇒ 加了两次，值只 +1（丢一次更新）
>
> 所以「计数要准」靠的不是给变量加 volatile，而是让**整个读改写**变成一个不可拆的整体：`AtomicInteger`（用 CAS 覆盖整步）、`synchronized`/`ReentrantLock`（用互斥覆盖整段）。
>
> 完整案例在 `handbook/java-backend/02-并发与资源生命周期.md` 的 conc.volatile 一节，想细看随时翻。
>
> 验证一下，只回一个数：`count` 是 volatile int，当前值 7。线程 A 读到 7 之后被挂起；线程 B 接着执行完整的 `count++`，把值改成了 8；然后 A 恢复运行，写完它这一步。最后 `count` 是多少？
