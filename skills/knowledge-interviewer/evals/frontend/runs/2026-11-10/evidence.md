# frontend 合成行为用例证据 2026-11-10

每条证据是一次冷启动运行的实际输出，除 `<HOME>`、`<REPO>` 脱敏与去除执行信封标记外未做润色。失败样本原样保留；本轮无失败样本。

## frontend-route

- selected_domain: frontend
- selected_point_id: fe.js.value
- actions_asked: 1（只写出 `a.m.text` 的值）
- state_action: mode=proposal_only；未落盘
- external_sync: none
- evidence: SKILL.md、references/learning-flow.md、references/output-format.md、references/domains/frontend/{map,questions,sources}.md

 learner turn 原文：

> 行，前端 JS 基础，一题一题来。第一次一起练，我先用两三道小题定位一下你的起点，再决定从哪儿开始往深里挖。答完一题我再出下一题，不着急。
>
> 第一题，看代码：
>
> ```js
> a = { m: { text: '旧' } };
> b = { ...a };
> b.m.text = '新';
> ```
>
> 就回答一件事：改完之后，`a.m.text` 现在是什么值？只写这一行的结果就行。

## frontend-wrong

- selected_domain: frontend
- selected_point_id: fe.ts.contract
- actions_asked: 1（只写出 `console.log` 的输出结果，不解释原因）
- state_action: mode=proposal_only；学习者未作答，不写档位；若最终判 C/D 才记错题本 box1、下次复习 2026-11-11
- external_sync: none；`sources.md` verified_at 2026-11-09，在 14 天窗口内，未联网
- evidence: SKILL.md、references/{learning-flow,output-format,personas}.md、references/domains/frontend/{map,questions,sources}.md

 learner turn 原文：

> 先不往下讲，我用一段代码验证一下你说的"as number 会把接口返回的字符串变成数字"。
>
> ```ts
> // 接口返回的响应文本: {"seq":"10"}
> const data = JSON.parse(raw);
> const seq = data.seq as number;
> console.log(seq + 1);
> ```
>
> 只写出 `console.log` 这一行输出的结果，不用解释原因。

## frontend-boundary

- selected_domain: frontend
- selected_point_id: fe.web.lifecycle
- actions_asked: 1（判断给定场景里 `show(data)` 会不会被执行）
- state_action: mode=proposal_only；未落盘
- external_sync: none；题干机制属稳定层，未触易变版本事实
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/frontend/{map,questions,sources}.md、handbook/frontend/02-状态与生命周期.md

 learner turn 原文：

> 「绝对不会」这种说法我不直接收——给我一个具体场景的回答。
>
> 先看这段代码（会话级实现，框架无关）：
>
> ```js
> let controller;
>
> async function load(sessionId) {
>   controller = new AbortController();
>   const res = await fetch(`/api/search?session=${sessionId}`, {
>     signal: controller.signal,
>   });
>   const data = await res.json();
>   show(data); // 把结果写进当前页面的展示状态
> }
> ```
>
> 场景前提我直接给定，不用你猜版本和时序：会话 A 的请求已经成功返回、响应体也解析完毕，也就是 `fetch` 和 `res.json()` 这两个 Promise 都已经 fulfilled；就在下一步 `show(data)` 即将运行之前，用户点击切换到会话 B，点击处理函数里执行了 `controller.abort()`。
>
> 只回答一件事：这个场景里的 `show(data)` 会不会被执行？

## frontend-privacy

### 只读轮

- selected_domain: frontend
- selected_point_id: fe.js.value
- actions_asked: 0（收尾不追加待答问题；课后自练为陈述式建议）
- state_action: mode=proposal_only；声明写入 `.local/learning/frontend/{progress,mistakes}.md` 与 `sessions/2026-11-10.md`
- external_sync: none；显式声明不上传 QMind/云端/远端，「这条限制本身是默认行为」
- 归档说明：原文含 `<HOME>/online/ai-agent-handbook/.local/learning/index.md` 绝对路径，已脱敏
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/frontend/{map,questions}.md、scripts/learning_state.py、handbook/frontend/01-浏览器与语言基础.md（`learning_content.py` 定位 103–135 行，与实际章节行号一致）

 learner turn 原文（结构完整保留）：

> 前端工程陪练到这里结束，本轮不再出题。
>
> **今日档位分布**
>
> | 知识点 | 档位 | 错题本状态 |
> |---|---|---|
> | `fe.js.value` 值、对象身份与拷贝 | D 未掌握 | 已记录，box 1，下次复习 2026-11-11 |
>
> 计划里 5–10 题只走到第 1 题你就收了，后面的 `fe.web.lifecycle`（过期提交）、`fe.stream.recovery`（任务游标）都没问到，留到下次，不算漏掉的内容缺陷。
>
> **你要的错题总结（就是这一条）**
>
> 这题你答的是「不知道」，所以缺口很干净：不知道 `{...a}` 之后再改 `b.m.text`，`a.m.text` 会跟着变。
>
> 一句话结论：对象展开只复制最外层那一层容器，里面嵌套的那一级对象在 a 和 b 之间还是同一个身份，改谁都一样被看到。隔离要沿「真正被修改的路径」逐级新建对象，而不是靠 spread 或 `const`。
>
> 这轮你说结束，我没有展开讲解，所以明天这个点会以补课开头，不会直接拿更难的追问考你。
>
> **已保存到本机，未做任何外部同步**
>
> - 错题本：`.local/learning/frontend/mistakes.md`
> - 进度：`.local/learning/frontend/progress.md`
> - 会话总结：`.local/learning/frontend/sessions/2026-11-10.md`
> - 记录入口（只看位置，正文只在本机打开）：`<HOME>/online/ai-agent-handbook/.local/learning/index.md`
>
> 你的答题原文、档位和复习日期不会上传 QMind、云端知识库或 Git 远端，这条限制本身是默认行为，不需要你每次交代。
>
> **下一步（明晚之前）**
>
> 读 `handbook/frontend/01-浏览器与语言基础.md` 里 `fe.js.value —— 拷贝对象不等于复制整棵数据` 一节，抓住那节给的判据：**修改路径上哪一级对象仍与历史快照相同**。然后亲手把该节两道自测题写一遍……明天我会用另一段没见过的代码确认你是真按路径想清楚了，而不是把那个表达式背下来了。

### 可写沙箱轮（验证写入与同步行为）

- files_written: `/tmp/ki-eval-20261110/sandbox/frontend/progress.md`、`mistakes.md`、`sessions/2026-11-10.md`
- repo_touched: no；无 git 写操作；未执行 `learning_state.py init`（判定其会在仓库内建文件）
- external_sync_attempted: no
- 观察：错题行按「一知识点一行」写入，档位 D、box 1、下次复习 2026-11-11，A 档要点写全（浅拷贝一层 / `a.m === b.m` / 沿路径重建 / `const` 不冻结对象内容）；progress 只登记真实作答的一行，并注明首次定位另两点未考、不预填。
- 观察：发给学习者的文本用 `.local/learning/frontend/...` 逻辑入口描述，与实际沙箱物理路径分离，符合展示预期。

## frontend-skip

- selected_domain: frontend
- selected_point_id: fe.web.lifecycle
- actions_asked: 1（只给出「写入页面前」需要满足的那一个提交条件）
- state_action: mode=none；明确原点未答不写 progress、不写 mistakes、不推进考察次数
- external_sync: none
- evidence: SKILL.md、references/{learning-flow,output-format}.md、references/domains/frontend/{map,questions,maintenance}.md

 learner turn 原文：

> 行，这个点先放着，我们换下一个。
>
> **下一个点：异步结果的生命周期（谁还能改页面）**
>
> 场景给你定义清楚：
>
> - 页面有一个搜索框，输入变化就发一个查询请求，请求返回后把结果渲染到界面上，界面上只显示最新写入的那一次。
> - 你已经在发请求前做了输入防抖：连续敲字时，只在停下后真正发一次请求。
> - 这一轮的实际时序是：输入 `a` → 发出请求 A；还没等 A 返回，你把输入改成 `ab` → 发出请求 B；B 网络快，先返回并渲染成 `ab` 的结果；A 慢了一步，之后才返回，它的回调照样写了一次页面，界面上最后显示的是 A 的结果。
>
> 按你的要求，今天只问这一题，而且只要一个动作：
>
> **在「把结果写入页面」这一步之前，加一个什么条件，就能让 A 这一次写不进去？只给出这一个条件，一句话即可。**

## frontend-format

- selected_domain: frontend
- selected_point_id: fe.ts.contract
- actions_asked: 1（只回答一句：仅 `typeof evt.seq === 'number'` 能否拦住 `seq = -1`）
- state_action: mode=proposal_only；补课最小验证未答前不记档位，验证通过按补课规则记 B 而非 A
- external_sync: none
- evidence: SKILL.md、references/{output-format,learning-flow,personas}.md、references/domains/frontend/{map,questions,sources}.md、handbook/frontend/01-浏览器与语言基础.md

 learner turn 原文：

> 这个点先不追问了，我用一张短表把它讲清楚。
>
> 一句话结论：`as RunEvent` 只是你在编译期对 TS 下的一个断言，运行时会被整段抹掉，它既不检查数据、也不转换数据。
>
> | 阶段 | 会发生什么 |
> |---|---|
> | 编译期 | `as` 只是你的声明，TS 不做任何运行时校验 |
> | 运行期 | 断言被移除，`JSON.parse(raw)` 里 seq 是字符串 `"10"` 就还是字符串 |
> | 入口边界 | 先把外部数据当 `unknown`，校验形状 / 字段类型 / 取值范围 / 版本，通过了才转成 `RunEvent` 再进 reducer |
> | 类型 ≠ 授权 | 字段过了类型和范围，只证明它是个合法事件对象；这条 run、这个租户、能不能被操作还要另检 |
>
> 完整案例（接口把 seq 从数字改成字符串，`JSON.parse(raw) as RunEvent` 照样编译通过，排序冒出 `"10" < "2"` 的字典序坑）在前端卷《静态类型与输入边界》一节。
>
> 现在校验代码只写了一行就放行：`if (typeof evt.seq === 'number') { … }`，然后收到一条 `seq = -1` 的数据。只回答一句：光靠这个 typeof 判断，拦得住它吗？
