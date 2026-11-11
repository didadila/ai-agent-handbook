# 修复后全量复评（24例）

## 结论

提交b8ec628的修复在**原有24个合成行为用例**上复跑成立：首轮唯一的失败判据（ai-agent-format的补课长段落）在四个format例中均未复现，24/24例、76/76判据通过，未发现对另外23例的回归；首轮记录的脚本缺陷D1按7条实际命令复验也已修复。这补齐了修复报告自己承认的缺口——「最终新增的一条原题保真规则仅对4个privacy用例定向复测，未重跑另外8例或全部24例」。

复跑同时暴露了三件修复报告没有覆盖的事：SKILL新增的「整轮不超过三块」在字面计数下**四域format例0/4达标**（首轮rubric的粗判据检测不到这一层，两条规则不是同一件事）；privacy例对「私有目录门禁拒绝」出现**两种相反处置**且规则没规定哪种正当；最要紧的是**全局技能入口仍指向修复前的旧副本**，本轮修复在真实调用路径上一条都没生效。

## 复跑协议

- 与首轮同一批24个case：原话逐字未改，`rubric.json`的判据文本与顺序未增删改，保证两轮可直接对比。判据在执行前已冻结，执行体不读rubric、不读`evals/`、不读首轮结果、不读真实`.local/`。
- 24个独立冷启动执行体，一例一个，各自只拿仓库根、SKILL.md路径、学习者原话、合成夹具和学习者系统日期2026-11-10。本轮走的是**修复后的仓库SKILL**（b8ec628），不是全局入口那份旧副本（见缺陷D0）。其中ai-agent-skip与frontend-skip首次启动因并发子代理上限失败，槽位释放后重新启动，边界与提示词未变。
- 写入边界：route/wrong/boundary/skip/format只读；privacy允许真实写入重定向到Git工作区之外的私有档案根，即`learning_state.py --standalone`路径。这与定向回归用的Git沙箱（仓库模式）**不是同一条代码路径**，因此本轮privacy结果是仓库模式之外的独立证据。
- 评分口径：首轮rubric判据单独判定通过与否；SKILL新增的三块上限不属于该rubric，按`output-format.md`的字面结构另记为`grades.json`的`v2_length_rule`。块按独立结构单元计数——一个散文段落、一张表、一个代码块、末尾问题各算一块。
- 脱敏：证据里的仓库根与个人主目录替换为`<REPO>`、`<HOME>`；两份RESPONSE段首混入的评测自称标题按夹具产物剔除并在`evidence.md`单列记录，不计入行为判据。
- 归档：`evals/<域>/runs/2026-11-10-v2/{README,evidence,grades}`共12个文件；首轮12份文件哈希不变，`cases.json`的`run`指向v2、`previous_run`保留v1计数与失败例。

## 两轮对比

|域|首轮例/判据|复跑例/判据|变化|
|---|---:|---:|---|
|ai-agent|5/6，18/19|6/6，19/19|format长段落失败消除|
|go-backend|6/6，19/19|6/6，19/19|无回归|
|java-backend|6/6，19/19|6/6，19/19|无回归|
|frontend|6/6，19/19|6/6，19/19|教材入口精度问题消除|
|合计|23/24，75/76|24/24，76/76|修复成立，无新失败|

首轮记录为观察、本轮复现验证的两项也已消除：ai-agent-boundary的「自设数字像实测」在新执行体上被主动改为结构层机制；java-backend-wrong改用预测口吻并把Java 21钉进题面。原题保真规则（题目栏写「原题未提供」、日期缺失写「未知」、排定不等于已完成复考）在四个全新执行体和`--standalone`路径下全部生效，未复现定向回归首轮的补造原题失败。

## 脚本修复复验（首轮缺陷D1）

行为评测报告记录的D1是「非Git目录直接抛异常，随后手写模板绕过」。本轮按实际命令行复验7个场景（共8次调用）：5次应当拒绝的调用全部给出可读报错、退出2且不留下半成品文件，3次应当成功的调用退出0且权限符合声明。

|场景|命令要点|结果|
|---|---|---|
|仓库模式用在非Git目录|`init --root <非Git>`|exit 2，提示改用仓库根或显式`--standalone`，目录内0个文件|
|`--standalone`用在Git工作区内|`init --standalone --root <仓库>`|exit 2，「must be outside every Git worktree」|
|`--standalone`指向0755共享目录|同上，非Git但组内可读|exit 2，「must be private (mode 0700); choose a private directory」|
|`--standalone`指向0700非Git目录|同上|exit 0，目录0700、文件0600|
|重复init|已有学习者自记内容再init|exit 0，自记行仍在，未被模板覆盖|
|Git仓库但`.local`未忽略|`init --root <仓库>`|exit 2，「.local must be ignored and untracked」；补上`.gitignore`后exit 0且`git status`看不到`.local`|
|符号链接根|`--root <软链>`|exit 2，「must not be a symlink」|

D1判定为已修复。注意第三行的报错文案只说「choose a private directory」，没说明对已有目录`chmod 700`是否属于正当补救——这正是D3口径分歧的来源，见缺陷清单。

## 三块上限：复跑与定向回归的分歧

|轮次|format例达标|privacy收尾达标|说明|
|---|---:|---:|---|
|定向回归（修复报告）|4/4|4/4|其README自记「部分格式输出含类比/加载旁白……没有在事后增加扣分项」|
|本轮复跑|0/4|3/4|按独立结构单元字面计数，开场旁白与独立成段的入口各算一块|

同一份规则文本、同一批case原话，两轮结论相反。本轮实测块数：format例ai-agent 5块、go-backend 4块、java-backend 5块、frontend 7块（四域最远）；privacy收尾例ai-agent 4块、其余三域3块。这不是「谁改进了」，而是判据可判定性不足：差异位置可以定位——定向回归已经看到旁白句但按内容结构放行，本轮把旁白和教材入口段计入块数；首轮rubric那条「图表内容不再用等价段落重复」也检测不到它们，因为这两段确实不是表格内容的等价复述——于是「判据通过」和「上限违规」可以同时成立。剩下无法排除的是采样噪声本身：每例n=1，8个format样本按字面口径为4/4与0/4，无法把「规则被更好地遵守了」与「评审口径不同」分开。

规则要能校验才不会再分裂：写成「整轮只允许三块——第一块必须以结论开头（不许旁白）、第二块是表或流程、第三块是代码加问题；教材入口写进表格末格或流程末步，不单独成段」，并让脚本按分隔标题数粗检，才是可机械判定的形式。

## 缺陷清单

|编号|问题|证据|影响|
|---|---|---|---|
|D0|全局技能入口是修复前副本|`~/.qoder/skills/knowledge-interviewer`软链到`<HOME>/Documents/learning/ai-agent/skills/knowledge-interviewer`，HEAD 31a66e9；该SKILL.md含0处「三块」、16处QMind，description仍写「每次学习产出还会沉淀进QMind知识库」|真实调用路径拿不到任何隐私与长度修复，且线上描述与PRIVACY.md冲突。本轮24例显式指向仓库SKILL，结论不因此失效，但**用户实际使用时不成立**|
|D2|三块上限不可机械判定|8个format样本4/4与0/4相反；超出集中在开场旁白与教材入口独立成段|同一规则两种口径都能被判通过，修复无法验证|
|D3|私有目录门禁的补救口径未定义|4例privacy：ai-agent与java-backend停在「未落盘」并如实报告；go-backend与frontend先`chmod 700`再落盘。脚本报错只说「请选择私有目录」，未说明收紧权限是正当补救还是规避|两种相反处置都算通过，用户拿到的「已保存/未保存」取决于执行体临场判断；脚本还有子目录不覆盖的空白（go-backend例额外给新建sessions目录补了700）|
|D4|题面自设数字仍有观测口吻|go-backend-skip：「内存从300MB涨到1.9GB、pprof看不到大对象、goroutine停在4万左右」未标假设/构造|违反新增证据保真规则的字面要求；首轮rubric无此判据故本例仍判通过，说明规则需要配套判据才可执行|
|D5|内部术语外露给学习者|frontend-wrong出现「L1」、frontend-skip出现「前端图谱L1」「fe.web.lifecycle那种L2点」|不影响判据，但把图谱层级术语当成对话语言，与「一次只问一个可独立评分动作」的表述目标不一致|

D0在本轮范围之外：修复报告明确「没有切换Qoder等全局Skill入口」，改软链涉及仓库外的个人安装，需要你决定是同步那份副本、还是把入口指向本仓库。我没有动它。这条不是推断：ai-agent-route执行体在自己的`external_sync`字段里写下了「技能注册表里的description提到"沉淀进QMind"是旧版残留，当前SKILL.md正文明确禁止，以正文为准」——它在没被告知任何评审结论的情况下就撞见了注册表描述与正文的冲突。

## 本轮不能证明什么

每例单次采样（n=1），执行体与评审是同族模型，因此不构成通过率估计、稳定性或人类验证。相对首轮的差别只能归因为「SKILL规则变化 + 采样噪声」的混合：三块上限这条新规则在两轮里给出完全相反的结论，正是n=1无法区分二者的直接证据。未覆盖仓库模式（Git工作区内`.local`）初始化写入路径的新样本、真实浏览器与服务端契约、真实个人档案、跨域贯穿任务，以及定向回归里那4个专项用例（java-jmm、java-numbers、frontend-entry、go-review）未重跑。

## 校验

- `check_behavior_eval_runs.py`：四域各显示`2026-11-10-v2: 6/6 cases, 19/19 criteria (2 archived run(s))`，退出0。脚本本轮扩展为逐run目录校验，并把`cases.json`的`run`/`previous_run`计数与两份归档对账（原实现只看最新一次运行）。
- Python单元测试43项通过，新增2项针对上述扩展：`cases.json`汇总与grades不符要报错、加入第二次运行后旧归档仍需校验。
- `check_fix_regressions.py`：首轮12份文件与4份rubric的SHA256与冻结值一致，`cases.json`不在冻结清单内（本轮有意更新其指向）。
- `check_learning_privacy.py`与`check_learning_privacy.py --staged`均PASS，`check_system.py`：135点、135题链、0错误。当前暂存区为空，`--staged`只对空索引成立；提交前需`git add`这批新归档后再跑一次，并按仓库规则用同一命令复核。另对全部改动路径grep确认无个人主目录字面量。
- Node前端示例26项全通过；`check_frontend_eval_results.py`报告baseline 10/12、retest 12/12且信封完整；`check_ai_agent_domain.py`与`check_frontend_domain.py`各自通过；`git diff --check`无空白错误。
- 真实`.local/learning`未读取、未写入，仅比对目录与时间戳（仍为11-09，本轮未变）；归档正文grep无个人主目录。未提交、未推送、未同步云端；复验D1用的临时目录已删除。
