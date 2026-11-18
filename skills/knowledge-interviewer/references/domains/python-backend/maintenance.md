# Python 后端领域 — 维护与定位契约

## 维护职责与写入边界

- `map.md` 是唯一稳定 ID 清单，共 36 点：主链 30 点，分组固定为语言 6、并发 4、服务 4、存储 6、任务分发 4、Agent 3、运维 3；工程底座 6 点（`py.eng.*`）单独成组、按需查阅，不占五天必做，也不改变主链 DAG。每行五个内容列：ID、层级、名称、该考什么、常见误解。前置写在“该考什么”单元格中，不另增依赖列，保持下方格式。
- `questions.md` 每个 ID 恰好一个三级标题，标题只含反引号包裹的完整 ID，含首题、2–3 个逐轮追问、A 档要点、错误答法和一个最小验证。答案供判档，不随首题展示；每个提问仅一个独立作答动作。
- `sources.md` 记录来源、实际支持切面、版本边界、核验日期与失败/待核验状态；本文件维护更新规则。完整案例/实验归 `handbook/python-backend/`，图解归 `materials/python-backend/`，不在题库复制教材。
- 领域参考由本文件维护：`map.md`/`questions.md`/`sources.md` 与本文件的 ID 范围、题链、证据和校验规则。稳定 ID 集合或总数变化必须同步 `catalog.json` 的 `points`、阅读地图与入口、checker 断言和对应检查输出；只改一处会让数量契约自相矛盾。教材正文、demo、materials、评测夹具和 docs 由对应维护者负责，发现接口不匹配只报告证据，不代改其文件、不新增校验脚本或隐藏安装步骤。个人状态永远不在同步范围内。
- 稳定 ID 不改名、不复用；修正机制、来源或教材不会自动更新学习者 A/B/C/D、错题、复习日期或历史。真实记录保持本机私有，不自动云同步；工具默认只读，不因维护/评测自动安装、调用付费云资源或部署。

图谱行与题库标题的固定格式：

```text
| `ID` | L1/L2/L3 | 名称 | 该考什么 | 常见误解 |
### `ID`
```

## 更新流程

1. 先读取 map 的目标 ID 与最近缺口，确认此次改的是稳定机制、组件版本契约还是应用设计。依赖改变要确认存在、无环且能按前置渐进出题。
2. 用 WebFetch 实际读取目标官方页/节；GitHub 使用 gh。记录返回正文明确支持的结论；只有目录、重定向、摘要或访问失败，不算核验。来源中的 `latest`/`stable` 路由不是“最新版本”结论。
3. 只为实际支持的切面更新 verified_at，未重读的条目保留旧日期，未打开或失败继续待核验；可替换失效 URL，但保留失败与成功范围。当前版本题超过 14 天或有不确定就即时重验，不能给整表统一刷新日期。
4. 更新 map 范围和误解靶子、questions 的单动作题链、sources 的证据边界。教材需要变更时交接相同 ID，不复制整章到参考包；未安装/尚未完成教材时明确回退。
5. 运行现有标准库检查；审阅无法静态判定的机制与题面。只记录真实运行结果、环境和未完成项，不把计划命令或静态覆盖称作行为评测。

## 已有项目的标准库校验命令

从仓库根目录执行以下命令；这里列的是已有脚本，不虚构 `check_python_backend_domain.py`。`PYTHONDONTWRITEBYTECODE=1` 避免生成项目内 pycache；测试只使用临时 SQLite 数据和模拟工具，不安装 FastAPI/PG/Redis/Celery/S3/pgvector。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_system.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/knowledge-interviewer/scripts -p 'test_learning_content.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s handbook/python-backend/examples -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 skills/knowledge-interviewer/scripts/learning_content.py --domain python-backend --point py.jobs.leases
python3 skills/knowledge-interviewer/scripts/check_learning_privacy.py
git diff --check
```

准备提交时另运行 `python3 skills/knowledge-interviewer/scripts/check_learning_privacy.py --staged`；这是发布面检查，不是自动提交授权。本轮不 stage/commit，不改 Git 配置。

| 检查 | 可证明 | 不能证明 |
|---|---|---|
| scripts/check_system.py | catalog 的数量契约、map/questions ID 对齐与重复、正文/阅读地图覆盖、公共文件/链接、评测 ID 引用 | 依赖无环、单动作质量、答案正确、模型陪练行为；不要只凭它通过判断全包完善 |
| test_learning_content.py | 每个点能找到真实主节、起止行有效、跨域拒绝与历史别名兼容 | 教材已充分解释机制、未运行的实验正确或 Python API 事实已核验 |
| examples 的 unittest discover | 当前标准库 demo 在临时文件/模拟工具下的断言；具体数量取实际输出 | 真实 LLM、鉴权、多节点队列、PG 隔离、Celery broker、S3/pgvector、生产容量或灾难恢复 |
| learning_content.py 单点定位 | 一个 ID 的真实正文路径/heading/display_title/行号 | 其他 ID 全覆盖；读取器返回入口不等于已读正文 |
| check_learning_privacy.py | 部分公共路径/个人目录引用/私有标记技术边界 | 全量隐私审查、外部工具没有泄漏或已经完成云授权 |
| git diff --check | Git 已跟踪差异的空白问题 | 新未跟踪文件的全部格式、内容正确性；新文件还需直接审阅 |

集成检查可能因其他维护者尚未提交的教材/materials/evals 不完整而失败。明确报出缺失路径或定位失败，交给对应维护者，不补写他们的文件，也不修改 checker/catalog 让失败消失。示例目录不存在或依赖缺失时停止对应检查并报“未运行”，不自动安装。

## 结构与内容人工验收

- 固定 IDs（36）：主链语言 py.lang.objects/collections/functions/types/resources/environment；并发 py.async.eventloop/cancellation/backpressure/execution；服务 py.svc.contract/lifecycle/idempotency/streaming；存储 py.data.model/transactions/indexes/cache/objects/retrieval；任务 py.jobs.delivery/outbox/leases/scheduling；Agent py.agent.tools/runtime/evaluation；运维 py.ops.observability/deployment/recovery。工程底座 py.eng.dependencies/testing/errors/time/security/profiling。前缀后的缩写在此仅为阅读，实际 map/questions 使用完整 ID。
- 每个 map ID 仅一行，层级只有 L1/L2/L3；不要把依赖补充表也写成 ID 开头的图谱行，避免现有正则重复计数。每点前置明确，主链依赖无环；svc.idempotency 必须先确认 data.transactions，data.objects 又依赖幂等。
- 工程底座横切主链但独立成表：它们不进入五天必做，不因“基础”被提前批量考完；`py.eng.*` 的前置可指向主链点，主链点不反向依赖它们，保持原 DAG 成立。
- 首题和每个追问均可单独评分；“只用一个问号”不够，不能要求列举后再解释、判断后再修复、同时设计并测试。最小验证仅一个动作，不提前泄漏答案；A 栏可列多维判据，因为它不是同轮问题。
- 首诊逐轮先语言，再并发，再任务；未确认前置不跳级。计划四个定位点不是一次问四题，不因学习者习惯 Python 就自动标语言掌握。
- 同轮复述、教材原句和已讲过的输出不能直接记 A；按未见变体验证，再在后续独立迁移确认。题面有缺陷先作废，用户要求结束不追加追问。

## 必须保留的机制边界

| 机制 | 维护时不得改成 |
|---|---|
| async/await 允许等待阶段并发；CPU 并行取决于执行模型/GIL/扩展/构建 | async 就多核；所有 Python GIL 一样；free-threaded 是 3.11 默认 |
| 取消等待与副作用完成是不同事实；运行中线程/远端不因取消 Task 自动终止或回滚 | timeout 代表没有退款；finally 撤回 HTTP；取消能硬杀任意远端 |
| 会话有事务状态，Session per thread、AsyncSession per task | 有池就可共享全局 Session；lifespan 是整个集群只执行一次 |
| 幂等键标识意图，指纹绑定载荷，唯一约束与状态原子保存 | key 相同就跨载荷/跨租户复用；查后插没有窗口；换新键安全重试 |
| Outbox 持久保存事件意图，发布/标记仍有重复窗口 | Outbox/Celery ack 自动 exactly-once；发布成功就是业务完成 |
| 租约过期不杀旧 worker；受保护写入端检查身份/generation | 单靠 TTL 安全；随机解锁 token 是单调 fencing；数据库拒绝旧结果能撤销邮件 |
| SSE 是事件传输，checkpoint/日志/审批属应用持久状态 | token 文本恢复 Python 栈；断线自动恢复所有执行；socket flush 就数据库提交 |
| 检索候选在授权租户/ACL 范围内产生，返回前仍防权限过期 | 全库 top-k 后过滤能替代检索前授权；相似度证明事实；安装 pgvector 才算学习 |
| 默认只读与最小权限；真实写/外传/安装/部署另授权 | 工具参数合法就是审批；只读标签允许个人记录自动云同步 |

本地 demo 若使用随机 lease token 与数据库条件更新，它可以验证“迟到 worker 不能覆盖该数据库结果”；不要冒称已实现供任意外部资源使用的单调 fencing 服务。SQLite 只验证其自身事务/约束；PG 和真实云系统另验。FakeAgent 是确定性模拟，不代表真实模型工具质量或 RAG 召回。

## 教材定位与协作

用 learning_content.py 查询目标 ID，实际读取返回节再解释；以返回的 heading/display_title/path/start_line/end_line 生成入口，不编造文件名、章标题或行号。没有 sections 时明确“教材尚未可定位”；独立安装缺小册则回退 map/questions/sources，不要求先装扩展。

新正文主节应与现有定位器约定兼容：编号章节文件 `handbook/python-backend/[0-9][0-9]-*.md`，`## ` 主节标题带完整稳定 ID。这只是交接契约，本文件不创建/修改这些章节。定位器会在下一个 `## ` 处终止该节；正文是否充分、代码是否可跑由教材/demo 维护者验证。

## 来源复核优先级

1. 已核验来源若用于当前版本题，先重读目标切面，尤其 free-threaded、FastAPI、SQLAlchemy 会话、PG 索引、Celery ack 与 S3 权限。
2. `sources.md` U01 的 Pydantic 正文访问 403，继续标待核验；不要以成功读取 Python typing 替它盖章。校验库具体转换/strict 规则作为版本前提，未核验时改成显式给定规则的机制题。
3. U02/U03 的 hash/dict/set/闭包/生成器精确切面与 U04 运行中 Future.cancel 优先补；原整页局部读取不等于这些子节已验。
4. U05–U08 与 U10–U16 的数据库约束、缓存模式、pgvector、安全、调度/broker、Outbox、观测/部署/备份、锁工具、覆盖率/flaky、重试库、采样 profiler 与压测仍待核验；U09 的 ASVS 对象级授权也未读正文。它们作为本包设计的参考候选，不把未打开的官方链接写为 verified。
5. 不为了来源更新改用户成绩、个人状态、权限配置或其他 agent 的工作；无法完成的集成/演练留明确未验证边界。

## 本次实际验证记录（2026-11-16，36 点状态）

- 实际解释器 Python 3.14.5；标准库本地验证不等于另已在 3.11 上执行，教学 API 仍以 3.11 可用边界为准。
- `scripts/check_system.py` 实际输出：python-backend 36 点 / 36 条题链，全仓 171 个稳定点，0 errors。静态检查不证明模型陪练行为。
- Skill 脚本全部 unittest 实际 65/65 通过；行为评测归档信封一致性检查通过，其中 python-backend 归档仍是 2026-11-16 的 5/6 cases、21/22 criteria，本轮未重跑模型评审，不能据此宣称行为已通过。
- 示例 unittest discover 实际 54/54 通过；本次只跑标准库与临时 SQLite，未运行真实 LLM/PG/Redis/Celery/S3/pgvector 或生产演练。
- `learning_content.py --domain python-backend --point py.eng.dependencies` 返回真实章节 `handbook/python-backend/08-engineering-foundations.md` 第 18–33 行；36 点逐点定位由 test_learning_content.py 覆盖。
- `check_learning_privacy.py` 与 `git diff --check` 实际通过。上一轮 30 点状态的记录已被本轮取代；并行工作区历史失败不在本轮复现，也不代表其文件已被清理。
