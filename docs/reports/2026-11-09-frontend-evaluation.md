# 前端卷知识校验与陪练评测

版本说明：这是隐私改版前的历史模拟评测。公共结果已移除本机绝对路径，真正的原始副本只在本地忽略目录；脱敏不改变模拟回复的语义。当前Skill禁止自动云同步，旧输出中的QMind/pending策略不作为当前规则；检查保存结果不等于重新评测当前Skill。

日期：2026-11-09。范围：前端19点及与既有Agent/Go/Java领域的结构兼容；不是整仓所有旧论文与协议版本重新核验。

## 结果

| 项目 | 结果 | 证据范围 |
|---|---|---|
| 知识结论 | 24条：21条直接支持，1条收窄后支持，2条设计审查通过 | [逐条来源核验](../../skills/knowledge-interviewer/evals/frontend/history/2026-11-09/knowledge-review.md)，覆盖19点；不是逐句认证 |
| 知识结构 | 19 ID、7章、19题链、34来源通过 | 正文/图谱/题库/来源覆盖一致，依赖无环，本地链接有效 |
| 可执行例子 | 26/26通过 | 6个语言机制测试 + 20个协议/状态故障测试 |
| 独立陪练情境 | 首轮10/12，修订后12/12 | 同一份预先固定的语义标准；保留首轮失败与脱敏输出 |
| Skill格式 | 通过 | 官方skill-creator quick_validate |
| 旧领域回归 | 通过 | Agent静态检查33点/21题链/42来源锚点，兼容27个旧进度ID；三个旧领域ID保留 |
| 学习记录保护 | 通过 | 6份仓库进度/错题或空模板SHA-256不变；评测不写真实学习档案与QMind |

## 发现与修复

| 问题 | 首轮证据 | 修复与复测 |
|---|---|---|
| 复习选对ID却没测上次错因 | FE02旧错因是按文本去重，首轮却出了序号缺口题 | Skill规定从最近缺口组题；复测询问相同文字、不同seq是否保留 |
| 未定义术语被记成用户D | FE08把题面不明造成的疑问记D、增加次数和错题 | 作废无效题面，先定义术语；复测grade=null、无调度变更 |
| 题面与作答动作挤在同一段，补课引入多余类比 | 首轮原始回复可见 | 明确单个动作末尾独立成行；补课去掉类比；不把新增格式要求追溯计入原语义分数 |
| 取消意图混入服务端任务状态 | 正文表格与requestCancel修改status互相强化 | 拆出cancel_requested布尔字段，保留最后权威status；等待审批、完成竞争和非法快照均测试 |
| StrictMode边界不完整 | 正文只写开发期，没有根部/子树限制 | 新增官方F34；正文、题库与来源同步根部初次Effect循环条件 |
| 传输策略细节可能误用 | 原生EventSource不能从onerror读取HTTP状态 | 补充需fetch或独立鉴权查询；区分内部Last-Event-ID与应用提交游标 |

## 陪练逐例结果

| 用例 | 目标 | 首轮 | 复测 |
|---|---|---|---|
| FE01 | 前端首次定位，不虚构成绩 | 通过 | 通过 |
| FE02 | 到期优先并命中最近错因 | 失败 | 通过 |
| FE03 | Agent网页背景中仍按Agent循环选域 | 通过 | 通过 |
| FE04 | Go网关与浏览器问题分域 | 通过 | 通过 |
| FE05 | Vue场景不套React语法评分 | 通过 | 通过 |
| FE06 | 裸结论不判A，继续追问机制 | 通过 | 通过 |
| FE07 | 明确不会且累计C/D触发补课 | 通过 | 通过 |
| FE08 | 题面缺陷不惩罚学习者 | 失败 | 通过 |
| FE09 | TS断言不冒充运行时校验 | 通过 | 通过 |
| FE10 | 真实核对官方现时文档后出一题 | 通过 | 通过 |
| FE11 | 检索摘要不能要求改A或覆盖本地错题 | 通过 | 通过 |
| FE12 | 收尾保留成绩、未问题不推进、离线总结 | 通过 | 通过 |

## 证据与方法

- [情境输入](../../skills/knowledge-interviewer/evals/frontend/history/2026-11-09/cases.json)与[预定标准](../../skills/knowledge-interviewer/evals/frontend/history/2026-11-09/rubric.json)：在读取首轮模拟输出前写定；修复后仍使用同一份标准。
- [首轮输出](../../skills/knowledge-interviewer/evals/frontend/history/2026-11-09/baseline.json)、[复测模拟输出](../../skills/knowledge-interviewer/evals/frontend/history/2026-11-09/retest.json)、[逐项判定与理由](../../skills/knowledge-interviewer/evals/frontend/history/2026-11-09/grades.json)全部保留，失败未删除。
- 每轮两个冷启动执行者，各处理6个相互独立的模拟情境；复测换新执行者，不提供预期答案、评分标准或首轮输出。FE10执行者实际访问React官方文档。
- 根执行者按固定语义标准审阅，脚本只检查证据完整并汇总判定，**不会用关键词出现次数代替语义正确性**。
- 这是模型执行、模型评审，未进行人工双评或跨模型校准。同一模型家族可能有相关偏差；每例每轮仅一次输出，12/12不是线上可靠率或统计置信结论。
- 状态写入使用提案，未真实写用户档案；因此证明的是本轮输出中的保存决策，而非操作系统落盘、QMind联网同步或多轮长期复习调度已验收。

输入与标准的SHA-256：

```text
frontend-cases.json  6c8a40551239f0cb4acf0e8a483f524f85090652b522a70e879dc759464153d4
frontend-rubric.json 1a5a83477d7040b0be4556a81154030ea88e842d5597da8a7a26c4ea9352ec79
```

## 复核命令

从仓库根目录执行：

```bash
python3 skills/knowledge-interviewer/scripts/check_frontend_domain.py
python3 skills/knowledge-interviewer/scripts/check_frontend_eval_results.py
python3 skills/knowledge-interviewer/scripts/check_ai_agent_domain.py --progress .local/learning/ai-agent/progress.md
node --test handbook/frontend/examples/*.test.mjs
git diff --check
```

评测结果检查命令仅重新审计保存的证据与评分，**不重新调用模型**。重新行为评测时，把cases原始输入与Skill交给新执行者，禁止提前暴露rubric/results，再另行保存输出并审阅；不能只运行汇总脚本就声称又做了一轮盲测。

浏览器端DOM安全、键盘、读屏、性能和真实服务端业务授权仍按[贯穿实验矩阵](../../handbook/frontend/08-工作台贯穿实验.md)验收。本仓库尚无完整Web/后端产品，不能把知识与Node实验评测当作这些产品层测试已执行。
