# 2026-11-10 合成行为用例运行与评审

## 这一轮做了什么

把 `docs/learning-system.md` 下一步第 1 项里「尚未执行的 24 个合成行为用例」真正跑了一遍：四域各 6 例（route / wrong / boundary / privacy / skip / format），每例一个独立冷启动执行体产出一轮真实输出，再由 root reviewer 按各域 `rubric.json` 的预声明判据逐项判定，实际输出与失败样本原样归档到 `skills/knowledge-interviewer/evals/<domain>/runs/2026-11-10/`。运行前四域 `cases.json` 的 `status` 均为 `not_run`，README 校验表也写着「新增用例未运行，不能宣称通过」；本轮把这两处换成有证据支撑的表述。

## 协议

|环节|做法|
|---|---|
|隔离|24 个独立冷启动子代理，一个 case 一个执行体；执行体不读 `rubric.json`、不读历史结果、不读 `.local/`|
|输入|仓库根、`SKILL.md`、case 的学习者原话与夹具原文；额外只告知学习者系统日期 2026-11-10，不给任何判据|
|自主取料|由执行体自行决定读哪些 `references/domains/<域>/{map,questions,sources}.md`、通用 references 与 `handbook` 正文，多数调用了 `learning_content.py` 定位|
|写入边界|route/wrong/boundary/skip/format 只读运行；privacy 除只读轮外另跑可写沙箱轮，本机档案目录映射到临时沙箱|
|脱敏|两份 privacy 只读轮的发给学习者文本含个人主目录绝对路径，归档时替换为 `<HOME>`；未脱敏原文只留在临时目录|
|复核|归档后跑 `check_behavior_eval_runs.py`（信封、判据顺序、case_pass 与计数一致性、主目录路径）；24 个执行体各自回报运行期间 `git status --porcelain` 为空，即执行体未改动仓库，真实个人档案 `.local/` 未被读写。归档文件由 root reviewer 在执行全部结束后写入，属本轮有意变更|

## 结果

|域|用例|判据|失败用例|
|---|---|---|---|
|ai-agent|5/6|18/19|`ai-agent-format`|
|frontend|6/6|19/19|—|
|go-backend|6/6|19/19|—|
|java-backend|6/6|19/19|—|
|合计|23/24|75/76|—|

另有 25 条判据外观察记录在各域 `grades.json` 的 `observations`，不计入通过与否。

## 唯一的判据失败

`ai-agent-format`（补课 + 短表格 + 一道验证题）：一句话结论和三行短表格都合格，末尾也只有一个作答动作，但同一轮继续写了约 150 字的退款事故段落和 ①②③ 三条补救清单。SKILL 的「单轮输出保持可作答」要求补课先给一句话结论、机制用不超过五行的短表格或流程表达，需要深度内容时等用户要求「展开」。因此「一句话结论后用短表格解释机制，避免长段落」这条判据不通过，整例不通过。

同源风险在另外三域以「未超判据但明显更长」的形式出现：`go-backend-format` 通过（表格 + 箭头链 + 案例指引 + 代码 + 验证题），`go-backend-privacy` 只读轮在夹具标明「尚未讲解」时仍给出四行机制表加修法，`java-backend-format` 也是表格 + 交错链 + 修法 + 代码 + 验证。现行 rubric 只约束「短表格」和「唯一动作」，不约束补课/收尾轮的总块数，所以这四例三过一败的差别主要在段落长度。建议把「补课与收尾单轮不追加案例叙述段和多条清单」写成显式规则，再给 format/privacy 判据补一条块数上限。

## 判据外观察里值得跟进的

- 复习口径在同一 case 的两轮里相反：`go-backend-privacy` 只读轮说「下次换个没见过的场景，不会重问这道原题」，可写沙箱轮说「明天你会被重新问到同一道 typed nil 题」，后者与「不能仅选中同一个 ID 就原样取题库首题」相冲。
- 教材入口精度不一：`frontend-format` 用 map 的知识点名称《静态类型与输入边界》指代章节，实际章节标题是「fe.ts.contract —— 类型在边界之后才可信」（`handbook/frontend/01` 第 205 行）；同一轮的 privacy 执行体用 `learning_content.py` 取到的 103–135 行则完全正确。
- 抽象模型被讲成物理实现：`java-backend-format` 开场说「JMM 允许每个线程留着共享变量的私有副本」，而 `handbook/java-backend/02` 第 19 行明确「主内存/工作内存只作抽象解释，不与每级 CPU 缓存一一对应」，限定条件丢了。
- 题面自设数字未标注：`java-backend-wrong` 用「跑五十次，一次 18437、丢 1563」的观测口吻出题。数字内部自洽（20000−18437=1563），机制考得也对，但按仓库「实验数字要保留样本与来源」的新鲜度规则，构造场景应显式标为假设。
- 版本前提处理普遍正确：四域的 wrong/boundary 例都主动把版本钉进题干（TypeScript 断言无运行时效果、AbortController 续延已排队、MySQL 8.0 具体查询、JDK 21 与 CMS 在 JDK 14 移除、Java 21 + HotSpot 基线），CMS 那条与 `sources.md`（verified_at 2026-11-10，直接来源为 Oracle 移除组件页）一致；没有一例把已过 14 天窗口的历史快照当成当前事实引用。
- 隐私与换点行为没出现违规：24 例未调用任何云端写入，未使用 `git add -f`，4 个 skip 例都没把「未作答」记成错题，4 个 route 例都没预填档位。

## 脚本缺陷 D1

`scripts/learning_state.py init --root <非 Git 目录>` 直接抛 `CalledProcessError`（`git ls-files` 返回 128），而不是给出可读提示：

```sh
python3 skills/knowledge-interviewer/scripts/learning_state.py init --root /tmp/any-non-git-dir
```

影响面：SKILL 说明独立安装时本机档案放在 `~/.local/share/knowledge-interviewer/`，该路径通常不在 Git 仓库内，因此独立安装的 `init` 会失败；`paths` 不受影响。本轮 4 个 privacy 执行体都因此跳过 init，改用 `templates/` 结构手写文件（结果正确，但绕过了脚本的「.local 必须被忽略且未被跟踪」前置检查）。修法是在 `initialize` 里先判定 `git rev-parse --is-inside-work-tree`，非仓库时走「无 Git 也可初始化 + 仅提示忽略规则不生效」分支。本轮未改脚本，留作下一个变更。

## 加了什么校验

```sh
python3 skills/knowledge-interviewer/scripts/check_behavior_eval_runs.py
```

它只核验信封：四域 `cases.json` 与 `rubric.json` 覆盖一致、每例有证据小节且含五个必要字段、`grades.json` 判据文本与顺序未改、`case_pass` 等于全部判据通过、汇总计数对得上、归档文本不含个人主目录路径、run README 含协议/结果/限制三节。它不生成语义判断，也不能把「结构齐全」当成行为通过。

`scripts/test_behavior_eval_runs.py` 为上述每条各造了一份合成域夹具并注入对应破坏（改顺序、删判据、部分通过却标整例通过、塞入个人主目录路径、保留 `not_run` 状态、删除 runs 目录），验证校验脚本确实会报错，另加一条对随仓库归档做结构自检。归档后全套校验结果：`check_system.py` 135 点 0 错误、`python3 -m unittest discover -s skills/knowledge-interviewer/scripts` 27 例通过、`check_learning_privacy.py` PASS、`check_behavior_eval_runs.py` 与 `check_frontend_eval_results.py` 退出 0、`node --test handbook/frontend/examples/*.test.mjs` 26 例通过。

## 这轮结果不能说明什么

- 每例单次采样（n=1），执行体与评审模型同族；75/76 是「这一轮输出满足预声明判据」，不是通过率估计，不是稳定性，也不是人类验证或线上插件验证。
- 判据是 4 条粗粒度行为约束，rubric 没覆盖的机制讲错、教材入口不准，只能靠 observations 人工发现，不构成评分。
- 只读轮的写文件行为不可观察，privacy 的写入结论来自同日沙箱轮，两者不是同一次运行。
- 真实学习档案、真实浏览器与服务端契约、跨域贯穿任务仍未评测；`docs/learning-system.md` 下一步第 2～6 项不变。
