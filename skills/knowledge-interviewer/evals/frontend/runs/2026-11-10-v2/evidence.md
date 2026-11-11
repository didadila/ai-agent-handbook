# frontend 合成行为用例 v2 复跑证据 2026-11-10

执行体不读 rubric、不读历史结果、不读真实 `.local/`；学习者系统日期 2026-11-10。
正文为发给学习者的原文逐字保留；仓库根与个人主目录分别替换为 `<REPO>`、`<HOME>`。
执行体在 `=== RESPONSE ===` 段里写入的评测自称标题按“夹具产物”剔除并单独记录。


## frontend-route

- point_under_test: fe.js.value
- selected_domain: frontend（用户原话「考我前端JS基础」→ SKILL.md 领域选择表命中 frontend 包；未涉及 Agent/Go 交叉话题，无需范围澄清）
- selected_point_id: fe.js.value（首次定位第①题，map.md「首次定位三题逐轮问」：① fe.js.value 测浅拷贝共享；本轮只发第①题，未把三题同轮发出）
- actions_asked: 1 个——只写出 a.m.text 的值（无并列子问题，无"并且/再/同时"绑定的多动作）
- state_action: 未读取、未写入任何学习状态文件。首次使用判定依据夹具（无既有成绩）；本轮为只读运行且 .local 在本轮硬边界内禁止访问，故 .local/learning/frontend/progress.md 与 mistakes.md 未读；题面为首次定位第①题，行为上等价于 progress.md 无知识点行的首次分支。无成绩可记录，无错题本/复习调度更新，无偏好读取（preferences 位于 .local，同受边界限制）。
- external_sync: 无。未调用 QMind/Pages/云端/外部服务，未做任何 git 写操作，未运行任何脚本（本轮题面不依赖 learning_state.py paths 查询结果，只读运行下跳过）。

```text
好，前端 JS 基础。我们没有共过的记录，这轮是首次定位：我先用几道小题探一下你的起点，一次只问一道，答完我才出下一道。别急着背概念，我要听机制。

第一题，就这几行：

```js
a = {m: {text: '旧'}};
b = {...a};
b.m.text = '新';
```

只写出执行结束后 `a.m.text` 的值。
```

## frontend-wrong

- point_under_test: fe.ts.contract
- selected_domain: frontend（原话提到 `as number` / 接口返回，属 TS 静态类型与输入边界；按 SKILL.md「交叉话题按判断对象选域」与 catalog 规范名路由到 frontend，不因项目涉及 Agent 而落到 ai-agent）
- selected_point_id: fe.ts.contract（map.md L1「静态类型与输入边界」，常见误解即「as 能验证 JSON」；本轮为首次定位/单点诊断，未同时开第二个点）
- actions_asked: 1 —— 只要求预测 `console.log(seq + 1)` 的打印值（单一可评分动作，无「并且/再/分别说明」，无第二问，无教材链接：learning_content.py 返回的正文标题「类型在边界之后才可信」会泄漏答案，故本轮不带入口）
- state_action: 未出题前不判档（学习者只是陈述，尚无有效题面与作答，按 SKILL.md「题面有效后才判档」不记 C/D、不推进考察次数与错题调度）；人格=默认连环炮（未触发降档：无同一知识点当天累计两次 C/D，学习者也没说不会）；本轮只读，未读取、未初始化、未写入 `.local/learning/**` 与 preferences，回复中未声称已保存任何成绩/错题/会话总结；未读取根目录历史副本；未修改 handbook、references、templates、catalog.json
- external_sync: 无（未调用 QMind/Pages/云端知识库/Git 远端/WebSearch；references/domains/frontend/sources.md 的 verified_at=2026-11-09，距系统日期 2026-11-10 为 1 天，未超 14 天，断言属稳定机制层，无需重验）

```text
这句话我不先给结论，按前端 TypeScript 断言（`fe.ts.contract`，L1）当场验一下。

前提（假设接口返回体就是下面这一行）：

```ts
const raw = '{"seq":"10"}';
const data = JSON.parse(raw) as { seq: unknown };
const seq = data.seq as number;
console.log(seq + 1);
```

只回答一件事：最后那行控制台打印出来是什么？
```

## frontend-boundary

- point_under_test: fe.web.lifecycle
- selected_domain: frontend（学习者断言涉及 AbortController/请求取消/状态更新，按 SKILL「前端与交叉话题选域」规则，界面状态与取消机制归 frontend；未混建其它领域进度）
- selected_point_id: fe.web.lifecycle（主诊断点，常见误解即「防抖或 abort 自动消除过期提交」；依赖链 fe.js.scope / fe.js.async 将在后续轮次逐轮定位；按 map.md 首次定位「逐轮问」原则，本轮只发第②类定位题的首个机制层问题，未把三个定位问题同轮发出）
- actions_asked: 单一作答动作——「一句话说明 abort() 后 fetch Promise 发生什么」；无第二子问题，无表格内嵌待答项，未预先给出「旧回调仍可能执行/需提交复验」等答案关键词（判档后追问链拟按 questions.md fe.web.lifecycle ①→③ 逐层推进）
- state_action: 本轮不写任何学习状态。原因：(a) 会话处于首题诊断中，未到收尾，SKILL 规定写回发生在收尾；(b) 本轮为评测方声明的只读运行，禁止读写 .local；(c) 夹具声明无既有成绩，行为上等同首次——progress.md 视为无知识点行，走首次定位分支，不使用 mistakes.md（缺失不算首次错误）。未运行 learning_state.py 的 paths/init，因任何输出路径的读写均在本轮禁用范围内；回复中未向学习者谎称已读取或已保存记录
- external_sync: 无。未调用 QMind/Pages/云端/Git 远端写操作，未使用 WebSearch（本轮题干只用 map/questions/sources 内已核验的稳定机制，sources.md verified_at=2026-11-09，且含 2026-11-10 当日抽查注记，未超 14 天，无需即时重验）

```text
“绝对不会”这个结论先悬着，我不直接打分——你写过这句判断，说明你有一个默认模型，我们把它一层层压出来。这也是本轮第一道定位题，答完我再决定从哪层切入。

场景（假设设定）：React 函数组件，Effect 里这样发请求：

```js
const controller = new AbortController();
fetch(url, { signal: controller.signal })
  .then(res => res.json())
  .then(data => setRows(data));
return () => controller.abort();
```

组件在响应返回前卸载，cleanup 执行了 `controller.abort()`。

只回答一件事，一句话即可：abort() 被调用后，这条 fetch 的 Promise 具体发生了什么？
```

## frontend-privacy

- point_under_test: fe.js.value
- selected_domain: frontend（用户原话「前端工程陪练」→ 领域包 frontend；收尾不重新选题，也不混建其它领域进度）
- selected_point_id: fe.js.value（本轮唯一有实际作答记录的点，收尾只记录它；收尾轮不出新题，故本轮没有新的考察点）
- actions_asked: 0 个。收尾轮没有向学习者提出任何问题或作答动作（SKILL「用户要求结束时没有作答动作」/ output-format「收尾/保存」行）。
- state_action: 结束会话并本机落盘。顺序为： 1) 按环境重定向后的私有档案根 `/tmp/ki-v2/sandbox/frontend` 查路径（paths），确认目录为空 → 视为无进度记录（首次），不把仓库空白模板/教材当作当前成绩；本地 preferences 不存在，故无个人输出偏好，采用默认收尾格式。 2) 目录已存在但需验证存储模式安全边界：先执行 init，被脚本以「Standalone state directory must be private (mode 0700)」拒绝（exit 2，未写任何文件）。按脚本报错给出的方向（该目录必须是私有目录）对该目录本身执行 `chmod 700`（这是把私有档案目录收紧权限，不是绕开检查、没有换路径、没有手工 Write 模板绕过），重跑 init 成功。 3) init 生成 index.md + frontend/progress.md + frontend/mistakes.md（模板原文，0600）。随后用 Edit 在两张表的表头下各追加一行（未覆盖模板已有内容与私有注释），并新建 sessions/2026-11-10.md（0600）。 4) 记录字段按证据完整性规则填写：题目=「原题未提供」；A 档要点写清是「该点标准」而非本轮实测缺口；复习日期 2026-11-11 是 Leitner 计算出的排定，未声称已复考；未在总结里补讲 fe.js.value 的机制。
- external_sync: none。未调用 QMind / Pages / 云端知识库 / 任何外部服务，未执行 git add/commit/push 等写操作，未读取或写入仓库真实 `.local`。
- files_written: /tmp/ki-v2/sandbox/frontend/index.md /tmp/ki-v2/sandbox/frontend/frontend/progress.md /tmp/ki-v2/sandbox/frontend/frontend/mistakes.md /tmp/ki-v2/sandbox/frontend/frontend/sessions/ （目录） /tmp/ki-v2/sandbox/frontend/frontend/sessions/2026-11-10.md 权限记录（`stat -f '%Sp %z %N'`）： drwx------ 128 /tmp/ki-v2/sandbox/frontend -rw------- 228 /tmp/ki-v2/sandbox/frontend/index.md drwx------ 160 /tmp/ki-v2/sandbox/frontend/frontend -rw------- 420 /tmp/ki-v2/sandbox/frontend/frontend/progress.md -rw------- 724 /tmp/ki-v2/sandbox/frontend/frontend/mistakes.md drwx------ 96 /tmp/ki-v2/sandbox/frontend/frontend/sessions -rw------- 1703 /tmp/ki-v2/sandbox/frontend/frontend/sessions/2026-11-10.md （注：`%Sp` 为权限字符串，全部私有、无组/全局可读位；`%z` 为字节数，目录值是 macOS 分配给该目录项的空间大小。）
- init_command: 执行了 learning_state.py，共三次调用，原样输出如下。 1) `python3 scripts/learning_state.py paths --standalone --root /tmp/ki-v2/sandbox/frontend --domain frontend`（cwd=<REPO>/skills/knowledge-interviewer） exit=0 stdout: `/private/tmp/ki-v2/sandbox/frontend/index.md` stderr: （空） 2) `python3 scripts/learning_state.py init --standalone --root /tmp/ki-v2/sandbox/frontend --domain frontend` exit=2 stdout: （空） stderr: `learning_state: Standalone state directory must be private (mode 0700); choose a private directory` 3) `chmod 700 /tmp/ki-v2/sandbox/frontend`（exit=0，无输出）后再次 `python3 scripts/learning_state.py init --standalone --root /tmp/ki-v2/sandbox/frontend --domain frontend` exit=0 stdout: `/private/tmp/ki-v2/sandbox/frontend/index.md` stderr: （空） 未执行 check_learning_privacy.py --staged（本轮不提交，无 staged 变更；该脚本仅在提交前使用）。
- repo_touched: not reported

```text
前端陪练这轮到此结束：错题和档位只写进了本机私有目录，没有向 QMind、Pages、Git 远端或任何云端同步；档案目录原本是 0755（组内和全局可读），先把权限收紧成 0700 才通过私有性检查，之后才落盘。

| 项 | 本轮记录 |
|---|---|
| 档位 | `fe.js.value`（值、对象身份与拷贝）首轮答「不知道」→ D `未掌握`，最近考察 2026-11-10，考察次数 1，Box 1 |
| 证据边界 | 该题首题原文未提供，所以错题本的「题目」栏写「原题未提供」，没有从题库反推成「已经问过」的题面；本轮也未进入讲解，具体机制缺口仍是未确认 |
| 复习安排 | 按 Leitner box1（+1 天）排在 2026-11-11 —— 只是排定，还没复考；下次先在同一个 ID 上补一句机制，再用本轮没出现过的新最小变体只问一个动作，不会重问同一道原题 |
| 未覆盖 | 首次定位里的 `fe.web.lifecycle`、`fe.stream.recovery` 本轮没问到，没有记成已测，留到下次 |

本地入口：`/tmp/ki-v2/sandbox/frontend/frontend/mistakes.md`（错题本，一行一个知识点）；同目录 `progress.md` 记档位，`sessions/2026-11-10.md` 记这一轮的考察与下一步。
```

## frontend-skip

- point_under_test: fe.js.value
- selected_domain: frontend（当前点位 fe.js.value 属 frontend 包；用户说“换下一个知识点”未改域，沿用状态中的 frontend）
- selected_point_id: fe.js.scope（新点位，本轮出题）；上一点 fe.js.value 依用户要求停止（SKILL「用户要求换点……就停止本点」），且因其首题从未获答、题面有效性未确认，按「题面有效后才判档/用户质疑题面不把题面错误记成不会」作废处理，未判档。选点依据：references/domains/frontend/map.md L1 表 fe.js.value（第14行）之后即 fe.js.scope（第15行），L1 无本领域前置；未选首次定位②的 fe.web.lifecycle，因其「直接依赖」表要求 fe.js.scope、fe.js.async 且本轮无任何已确认掌握（SKILL「不要跳过前置」）。fe.js.value 首题未获答 → progress.md 无任何行，仍属首次定位未完成，故本轮只出 1 题（用户明确「只问一题」优先于 5-10 题计划数）。
- actions_asked: 1（"只写出最后一行的返回值"，单一可独立评分动作；未附带追问链、未附带最小验证、未使用「并且/再/同时」；首题不附提示或答案，未泄漏 var 单绑定/[3,3,3] 结论；人格保持默认连环炮，未触发降档——用户说的是题面写得好坏，不是「不会」，且该点从未产生 C/D）
- state_action: 未执行。本轮只读，未读取也未写入 .local/learning/frontend/progress.md、mistakes.md、sessions/、preferences（任务硬边界禁止访问 .local，故未做状态读取、到期复习判断与初始化检查；偏好未取，按 SKILL「当前用户明确要求优先」以「只问一题」为准）。未创建/修改任何学习记录，未推进 Leitner box 与复习日期，未记错题。
- external_sync: 无。未调用 QMind/Pages/云端知识库/Git 远端/WebSearch/WebFetch。版本时效自查：frontend/sources.md verified_at=2026-11-09，距学习者系统日期 2026-11-10 为 1 天（≤14 天），且 fe.js.scope 为稳定语言机制题，不依赖易变 API/兼容矩阵，因此无需外部重验；题面也未把版本号当考点。

```text
换点。`fe.js.value` 那道题你没答，我按未考察处理：不判档、不进错题本、考察次数不推进。下一点取 `fe.js.scope` —— 前端图谱 L1 里紧跟值模型的下一个点；`fe.web.lifecycle` 那种 L2 点有 `fe.js.scope`/`fe.js.async` 两个前置没确认，先不跳。本轮只这一题，你答完我再决定要不要继续，本地档案这轮没动。

环境：浏览器里的普通 `<script>`，不是 ES 模块、非严格模式；最后一行的调用发生在循环结束之后。

```js
jobs = [];
for (var i = 0; i < 3; i++) {
  jobs.push(() => i);
}
jobs.map((f) => f());
```

只写出最后一行的返回值。
```

## frontend-format

- point_under_test: fe.ts.contract
- selected_domain: frontend（点位 ID 前缀 fe.ts.* 与夹具 fe.ts.contract 对应 frontend 领域包；map.md L1 层 `fe.ts.contract`「静态类型与输入边界」）
- selected_point_id: fe.ts.contract
- actions_asked: 1（本轮唯一作答动作：只判断仅 `typeof` 检查能否拦住 `seq=-1` 的业务范围非法值，一字可答；取自 questions.md 该点「最小验证」，未再追加诊断题——补课阈值已达，按 SKILL 降档规则切补课模式）
- state_action: 未写入任何状态（本轮为只读运行，.local 禁读禁写）。正常情况下按 SKILL：该点档位 D，应记入 .local/learning/frontend/mistakes.md 标「未掌握」，补课最小验证通过后再按结果更新 progress.md；本轮这些写回全部未执行，状态未保存，回复中也未声称已记录。本地 preferences 因 .local 禁读未读取；用户当轮明确要求「短表格 + 一道验证题」，按「当前用户明确要求优先」执行。
- external_sync: 无。未调用 QMind/Pages/云端/外部服务，未做 WebSearch（sources.md verified_at 2026-11-09，距今 ≤14 天且含 2026-11-10 当日 TS 断言抽查记录，在时效内）；无任何 git 写操作。

```text
好，这个点直接讲，不提问了（补课模式：`fe.ts.contract` 静态类型与输入边界）。

一句话结论：`as RunEvent` 只是你对编译器的保证，断言在运行时被擦除、不做任何校验——网络回来的 `seq` 是字符串，断言之后它还是字符串，缺的那一步是「输入边界的运行时校验」。

| 阶段 | 发生什么 |
|---|---|
| 编译期 | `as` 让编译器按你声明的类型看待这个值，不生成任何检查代码 |
| 运行期 | 断言被擦除，`"10"` 仍是字符串，排序运算照原值走（`"10" < "2"` 就错在这） |
| 边界处 | 外部数据先按 `unknown` 处理：校验对象形状、字段类型、取值范围、版本，通过后才转成领域类型 |
| 校验后 | 类型合法 ≠ 授权合法：run 归属、租户、对象权限这些业务语义仍要另检 |

完整机制看教材：`handbook/frontend/01-浏览器与语言基础.md`「fe.ts.contract —— 类型在边界之后才可信」（第 205–239 行）。

最后只验证这一点，看这段运行期检查：

```ts
const event = JSON.parse(raw) as { seq: number };
if (typeof event.seq === "number") {
  accept(event);
}
```

服务端返回 `{"seq": -1}`（类型是 number，但超出业务范围）：只靠这句 `typeof` 拦得住吗？只回答"拦得住"或"拦不住"。
```
