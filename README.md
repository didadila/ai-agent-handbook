# 技术知识学习系统

以知识图谱组织学习范围，由AI陪练逐题诊断、结合教材讲解，并安排本地错题复习。项目目前通过Markdown教材、HTML图解、Skill和校验脚本提供学习能力；使用者可以一直从Skill进入，无需自己在多个目录间切换。

公共知识供不同学习者复用；个人错题、成绩、偏好与会话记录只保存在本机。当前四域共135个稳定知识点，每点均有教材入口和题库入口。

## 能学什么

|领域|主要内容|知识点|学习入口|
|---|---|---:|---|
|Agent工程|模型边界、上下文、工具、检索、循环、评估、成本与安全|33|[教材](handbook/ai-agent/README.md) · [图谱](skills/knowledge-interviewer/references/domains/ai-agent/map.md) · [题库](skills/knowledge-interviewer/references/domains/ai-agent/questions.md)|
|Go后端|值与错误、并发、服务边界、事务、一致性、可观测、Agent后端|19|[教材](handbook/go-backend/README.md) · [图谱](skills/knowledge-interviewer/references/domains/go-backend/map.md) · [题库](skills/knowledge-interviewer/references/domains/go-backend/questions.md)|
|Java后端|JVM、并发、MySQL、Redis、Spring、消息与分布式设计|64|[教材](handbook/java-backend/README.md) · [图谱](skills/knowledge-interviewer/references/domains/java-backend/map.md) · [题库](skills/knowledge-interviewer/references/domains/java-backend/questions.md)|
|前端工程|HTML/CSS、JS/TS、状态、HTTP/SSE、审批、安全、性能与交付|19|[教材](handbook/frontend/README.md) · [图谱](skills/knowledge-interviewer/references/domains/frontend/map.md) · [题库](skills/knowledge-interviewer/references/domains/frontend/questions.md)|

135点是当前核心课程范围。各卷章节深度、实验覆盖和评测成熟度不同，目录齐全不等于已覆盖所有基础或完成逐句事实认证。Go与Java按各自依赖学习；前端和Agent通过状态、授权与恢复等主题衔接，无需先读完全部其他卷。

## 怎么开始

|想做什么|操作|
|---|---|
|直接阅读|从上表教材README进入，按knowledge-map中的依赖顺序读|
|开始陪练|在支持Skill的AI编码工具中打开本仓库，让它读取[knowledge-interviewer](skills/knowledge-interviewer/SKILL.md)，再提出学习目标|
|复习错题|说“复习我的前端错题，一次一题”；Skill读取当前克隆中的本地档案|
|查看图解|打开[materials](materials/README.md)对应域的maps/overview.html；复习卡片在cards中|
|了解项目设计|查看[docs导航](docs/README.md)，无需把历史审计报告当教材阅读|

陪练请求示例：

```text
从前端基础开始，按知识图谱考我，一次只问一题。
我不会这个点，先用短表格或流程图讲解。
这点已经懂了，换下一个知识点。
展开讲这个机制，并给对应教材入口。
```

首次定位也逐轮进行；不会一次抛出整组问题。你可以要求换点、改变讲解方式或结束，不需要把计划题数全部问完。

使用全局安装的Skill时，先确认它指向本仓库，还是另一份复制版本；仓库更新不会自动更新独立副本。软链应核对最终目标路径，避免以为在用新规则，实际读取旧工作副本。本仓库不自动改写其他工具的全局安装配置。

全局入口建议指向选定的仓库工作副本，避免复制后长期分叉；可运行 `python3 skills/knowledge-interviewer/scripts/check_skill_entry.py`核验Qoder入口、主Skill及配套脚本是否确实来自当前仓库。该检查验证文件入口，不证明宿主已打开会话的缓存已刷新；切换后在新会话使用。

## Skill、教材、题库怎样协作

```mermaid
flowchart LR
    A[学习目标与本地记录] --> B[图谱选点]
    B --> C[题库诊断：一次一题]
    C --> D[依据回答定位缺口]
    D --> E[读取教材对应节与来源]
    E --> F[表格或流程讲解]
    F --> G[一个新场景验证]
    G --> H[仅本地记录与后续复习]
```

|组成|负责什么|Skill何时使用|
|---|---|---|
|Skill|流程、交互、判档、停止条件和隐私执行|每场学习|
|领域map|稳定ID、范围、依赖和常见误解|选择当前知识点|
|领域questions|诊断场景、追问、答案判据|出题与评价，逐轮取用|
|领域sources|官方证据、版本、边界和核验日期|解释当前API、处理争议与更新知识|
|handbook|案例、机制、取舍与自测|补课或主动要求讲解时按ID读取|
|materials|依赖总览、图解和短复习卡片|视觉说明有帮助时|
|本地档案|这位学习者的答法、错因、复习与偏好|会话前后，不混入公共知识|

教材按“结论 → 案例 → 机制 → 误解靶子 → 判据 → 自测题”组织。Skill是你使用的入口，handbook是讲解内容来源；无需自己切换去读，仍可要求打开原文深入学习。仅复制安装Skill而未携带教材时，使用包内图谱/题库/来源回退，并说明完整教材未安装。

正文可按稳定ID定位，输出公共文件及起止行：

```sh
python3 skills/knowledge-interviewer/scripts/learning_content.py --domain frontend --point fe.ts.contract
```

## 目录结构

```text
.
├── README.md                         项目说明与使用入口
├── catalog.json                      四域规范名、别名、ID前缀和目录契约
├── PRIVACY.md                        公共存储与发布规则
├── handbook/
│   ├── ai-agent/                     Agent教材
│   ├── go-backend/                   Go教材
│   ├── java-backend/                 Java教材
│   └── frontend/                     前端教材
├── materials/<domain>/
│   ├── maps/                         当前知识总览；legacy存历史图解
│   └── cards/                        复习卡片；legacy存历史问答图卡
├── skills/knowledge-interviewer/
│   ├── SKILL.md                      陪练主入口
│   ├── references/                   通用教学规则与四域知识参考
│   ├── templates/                    空白进度/错题结构
│   ├── scripts/                      定位、本地档案与校验工具
│   └── evals/<domain>/               合成用例、评分标准与历史证据
├── scripts/                          全项目一致性检查
├── docs/                             设计说明与维护报告
└── .local/learning/                   个人档案，被Git忽略
```

旧handbook/agent是迁移前路径，公共教材现统一在handbook/ai-agent；agent仍可作领域输入别名，知识点agent.*保持不变。旧serve同理对应go-backend。本机遗留的旧目录若只有私人进度/错题，不属于第二套教材；本轮已在确认本地副本完整且内容一致后清除重复文件。

旧posts是问答图卡、sketches是知识图解，现归入materials的领域目录。历史素材保留原语境，不覆盖当前教材。

## 个人数据与展示偏好

首次使用可初始化空白档案；需要Python3和Git：

```sh
python3 skills/knowledge-interviewer/scripts/learning_state.py init
python3 skills/knowledge-interviewer/scripts/learning_state.py paths
```

初始化不覆盖已有记录；paths只显示本地索引位置。旧.local/learning/serve存在时继续使用，避免丢失Go学习记录。

仓库模式的--root必须是Git工作区根目录，.local必须被忽略且未跟踪。独立安装无仓库时，显式运行同脚本的 `init --standalone`，默认写本机私有状态目录；`--standalone --root <私有目录>`把该目录本身作为状态根，且拒绝Git工作区内路径。初始化失败会给可读提示且停止保存，不能手写模板绕过检查。

|内容|位置|是否随Git发布|
|---|---|---|
|教材、图谱、题库、图解与空白模板|公共目录|是|
|明确为合成数据的评测|evals|是|
|个人进度与错题|.local/learning/领域|否|
|输出偏好、教学反馈|.local/learning/preferences|否|
|会话总结与历史备份|.local/learning中的sessions/archive等|否|

Skill会读取存在的output-style.md和interviewer-feedback.md；前者控制这位学习者的展示偏好，后者记录历史教学反馈。当前用户明确要求优先。要求表格时用短表格，步骤与因果链用流程，图表替代重复段落；唯一问题仍单独放末尾。个人偏好不改变事实或掌握判据。

默认补课采用固定“结论／机制／验证”三段，保存收尾采用“状态／记录／入口”三段；教材入口嵌入表格，不加开场旁白或额外段落。普通出题仍只问一个动作，不外露内部知识点ID和图谱层级。check_response_format.py可检查结构，事实准确性与语义动作数仍需评审。

不自动同步个人记录到Git、QMind、Pages或其他外部服务。.gitignore是防误提交措施，不能清除旧提交历史或阻止任意程序读取本机文件。完整边界见[PRIVACY](PRIVACY.md)。

## 知识新鲜度与准确度

|内容类型|维护方式|
|---|---|
|稳定机制|明确目标版本与前提；不因版本旧就直接删掉|
|当前API、默认值、兼容性、协议状态|查官方版本入口，记录实际核验范围与日期|
|历史实现|保留适用条件和迁移关系，避免当当前默认能力判档|
|论文或厂商实验数字|保留样本、版本和指标；不能直接当普适结论|
|无法确认的断言|标待核验/部分支持，不批量刷新日期冒充已核验|

每个领域的sources与maintenance记录证据和更新方式；过去报告描述当时状态，当前事实以最近的明确核验条目为准。2026-11-10再核验修正了OTel核心依赖版本、无法固定版本的错误推论和OWASP失效链接，详见[本轮报告](docs/reports/2026-11-10-freshness-and-presentation.md)。

## 校验与评测

在仓库根目录运行；Python检查使用标准库，前端代码测试另需Node.js：

```sh
python3 scripts/check_system.py
python3 -m unittest discover -s skills/knowledge-interviewer/scripts -p 'test_*.py'
python3 skills/knowledge-interviewer/scripts/check_learning_privacy.py
python3 skills/knowledge-interviewer/scripts/check_behavior_eval_runs.py
python3 skills/knowledge-interviewer/scripts/check_frontend_eval_results.py
node --test handbook/frontend/examples/*.test.mjs
```

提交前检查暂存区：

```sh
python3 skills/knowledge-interviewer/scripts/check_learning_privacy.py --staged
```

|验证类型|能说明什么|当前限制|
|---|---|---|
|目录/ID/题链/链接校验|135点的公共材料能对应起来|不证明所有事实正确|
|正文定位与隐私测试|脚本定位、兼容与部分发布边界有效|不证明模型每轮都遵循流程|
|前端Node测试|示例协议核心与语言案例的确定性性质|不替代浏览器和后端验收|
|合成行为用例与rubric|24例已冷启动运行两轮并逐项评审：首轮23例通过、`ai-agent-format`因补课单轮超出简短边界未通过；修复提交b8ec628后同一批原话与同一份rubric复跑24例通过。两轮输出与失败均归档在`evals/<域>/runs/2026-11-10/`与`runs/2026-11-10-v2/`|每例单次采样、执行与评审同族，不构成通过率或稳定性证明；SKILL新增的整轮三块上限不属该rubric，单独记录|
|历史前端行为证据|保留当时12例模拟输出与评分|不当作当前全系统结果|

四域24例行为用例的运行协议、唯一判据失败样本、判据外观察与一个`learning_state.py init`缺陷见[行为评测运行报告](docs/reports/2026-11-10-behavior-eval-run.md)。privacy用例另跑可写沙箱轮直接观察写文件；归档前必须脱敏个人主目录路径，否则公共评测文件会触发隐私检查失败。

上述结果按原判据保留。针对缺陷的脚本修复、新版整轮长度/准确性判据及独立回归见[修复报告](docs/reports/2026-11-10-behavior-fixes.md)；新版结果单独归档，不回写原23/24成绩。可运行 `python3 skills/knowledge-interviewer/scripts/check_fix_regressions.py`检查新信封与原始证据哈希。

原24例的全量复跑及其留下的格式、权限、数字和全局入口问题见[修复后全量复评](docs/reports/2026-11-10-recheck-after-fixes.md)。这些问题已在后续v3定向优化中处理：16个新判据用例满足要求，授权切换全局入口后另跑2例冒烟；详情见[v3优化报告](docs/reports/2026-11-10-v3-optimization.md)。旧24/24仍按旧rubric保存，不改分、不与新标准混算；全局入口文件已指向当前仓库，已打开宿主会话的缓存不在文件校验范围内。

维护知识时同步检查教材、图谱、题库、来源和有关图解；稳定ID不改名、不重用，不为适配新教材篡改个人成绩。详细职责、已知缺口和补全优先级见[学习系统说明](docs/learning-system.md)。
