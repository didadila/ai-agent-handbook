# 四域评测

当前修复验收入口为[regressions/2026-11-10-v3](regressions/2026-11-10-v3/README.md)：固定三段结构由程序检查，所有题型均评审证据保真、机制条件与内部标识外露，保存场景明确拒绝自动chmod。候选16例与切换后的全局入口2例分别归档；旧域内cases/rubric和此前v2定向修复均按原标准保留，不能事后改分。

四域均使用cases.json与rubric.json，覆盖路由、错误机制、版本/边界、隐私和换点。2026-11-10 四域各 6 例已按冷启动协议真实运行并逐项评审；修复提交b8ec628后同一批case原话与同一份rubric又独立复跑一轮。`cases.json`的`status`现为`run_reviewed_2026-11-10_v2`，`run`指向`runs/2026-11-10-v2/`（24/24），`previous_run`保留`runs/2026-11-10/`（23/24，失败例`ai-agent-format`）。只有保存实际模型输出并逐项评分后才能报告行为通过，两轮结果与限制见各域runs目录与[行为评测报告](../../../docs/reports/2026-11-10-behavior-eval-run.md)、[修复后全量复评](../../../docs/reports/2026-11-10-recheck-after-fixes.md)。

SKILL新增但不在原rubric里的规则（如整轮三块上限）单独记在grades.json每例的`v2_length_rule`（块数、上限、verdict、超出位置），不参与原判据通过与否——否则等于用新标准回溯重算旧成绩，也会让"判据通过"和"格式仍超出上限"两件事被混成一句。

历史前端12例和Agent4例保留在各自history/2026-11-09中；它们反映旧目录和旧领域名，不改写成新测试结果。前端历史结果通过check_frontend_eval_results.py核验格式与既有评分。四域运行结果由check_behavior_eval_runs.py核验信封：逐个run目录检查判据文本与顺序不得偏离rubric、case_pass必须等于全部判据通过、汇总计数必须对得上、每例必须有含五个必要字段的证据小节、归档文本不得含个人主目录路径、run README必须有协议/结果/限制三节；`cases.json`的`run`与`previous_run`计数必须分别与对应归档目录的grades.json一致。该脚本不生成语义判断，也不能把结构齐全当成行为通过。脚本本身由 `scripts/test_behavior_eval_runs.py` 用合成域夹具自检：改动判据顺序、删判据、部分通过却标整例通过、塞入个人主目录路径、保留 `not_run` 状态、删除 runs 目录、cases.json汇总与归档不符、新增第二次运行后旧归档失校验，都必须报错。

建议每次Skill规则变化独立冷启动：只向执行模型提供Skill、case与合成夹具，不提供rubric；输出保存到本地临时目录，经隐私检查后将合成结果归档到域内runs，再逐项评审。真实学习档案不得作为公开夹具。同一批case在多轮之间保持原话与判据逐字不变，新增轮次写入新的runs子目录而不是覆盖，否则两轮无法对比。

写入行为用可写沙箱轮验证：把本机档案目录映射到临时目录，允许执行体真实写文件，同时禁止改动仓库；结束后核对 `git status --porcelain` 为空、沙箱内文件与声明一致、无任何外部写入。`learning_state.py`有两条不同的初始化路径，需要分别覆盖：仓库模式（Git工作区内`.local`，须已忽略且未跟踪）与`--standalone --root <目录>`（目录必须在所有Git工作区之外且权限0700）。定向回归走前者，2026-11-10-v2轮走后者，两者结论不可互相代替。其余四类用例保持只读运行，因为它们在未作答时本来就不该落地。

归档时必做脱敏：执行体可能把个人主目录绝对路径写进发给学习者的文本，直接入库会让check_learning_privacy.py报“personal home path in shared file”。替换为 `<HOME>`/`<REPO>` 并在run README里记下做过替换，不保留未脱敏原文。执行体偶尔把评测自称标题（如“# knowledge-interviewer v2 冷启动执行体输出”）写进`=== RESPONSE ===`段：那是提示词产物而非发给学习者的行为，从归档正文剔除并在evidence.md单列`harness_artifact_removed`，不计入判据也不据此判失败。

本轮修复回归单独位于regressions/2026-11-10-fixes：新cases/rubric预先定义整轮块数、准确性、教材定位、复习与保存约束；原四域rubric及23/24输出不变。新回归初轮及定向重试都保留实际输出和失败，不用新标准回溯重算旧成绩。check_fix_regressions.py验证新信封及baseline-sha256记录的旧证据哈希，只检查结构和算术，不生成语义评分。

写入行为用可写沙箱轮验证：把本机档案目录映射到临时目录，允许执行体真实写文件，同时禁止改动仓库；结束后核对 `git status --porcelain` 为空、沙箱内文件与声明一致、无任何外部写入。其余四类用例保持只读运行，因为它们在未作答时本来就不该落地。

归档时必做脱敏：执行体可能把个人主目录绝对路径写进发给学习者的文本，直接入库会让check_learning_privacy.py报“personal home path in shared file”。替换为 `<HOME>`/`<REPO>` 并在run README里记下做过替换，不保留未脱敏原文。

新版检查：`python3 scripts/check_fix_regressions.py --suite evals/regressions/2026-11-10-v3`（相对Skill目录），全局冒烟则把suite指向其global-entry子目录。check_response_format.py只做结构粗检；不得据此替代准确性和单动作语义评审。
