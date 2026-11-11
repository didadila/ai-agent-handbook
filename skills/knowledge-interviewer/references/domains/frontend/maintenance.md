# 前端领域维护与接入

知识源为 map（唯一ID清单）、questions（逐点追问链）、sources（官方证据）、前端小册（完整机制与实验）。新增知识必须同步四处；保留既有ID，状态文件不因教材更新而迁移档位。

## 维护步骤

1. 从官方文档核验变化；区分语言/浏览器机制与框架/工具版本。社区面经只能决定练习场景。
2. 每点正文保持结论、案例、机制、误解靶子、判据、自测题六段；数字标明是教学输入或真实测量。
3. 题库首题只要求一个动作；追问按轮次使用；最小验证不推进其他知识点。
4. 更新 sources 的日期只覆盖实际重新核验的范围；不能只打开一条来源就把全表日期重置。
5. 运行下列检查；浏览器与服务端用例只有实际跑过才写通过。

```bash
python3 skills/knowledge-interviewer/scripts/check_frontend_domain.py
python3 skills/knowledge-interviewer/scripts/check_ai_agent_domain.py --progress .local/learning/ai-agent/progress.md
node --test handbook/frontend/examples/*.test.mjs
python3 skills/knowledge-interviewer/scripts/check_frontend_eval_results.py
git diff --check
```

## 陪练路由检查清单

| 输入 | 应执行的行为 |
|---|---|
| 考我前端/JS/TS/CSS/React | 选 frontend，先读 frontend 学习状态，再按本领域图谱组题 |
| 我想学 SSE 在 Agent 界面如何恢复 | frontend 的 stream；必要时补 async/state/http 前置 |
| 我想学 Agent 为什么循环 | ai-agent，不因网页项目背景改为 frontend |
| 我想学 Go 服务端 SSE 网关 | go-backend（兼容旧名serve）；前端流恢复可以后续跨卷关联 |
| 继续 | 沿用已选领域，仍先处理到期错题，不因为新卷上线重做首次定位 |
| frontend无进度行 | 逐轮首次定位，未回答不写成绩 |
| sources 超过14天且问当前浏览器支持 | 先核对官方文档，给出版本前提再出机制题 |

公开空白模板位于 `skills/knowledge-interviewer/templates/`；真实状态位于忽略目录 `.local/learning/frontend/`。已有记录不覆盖，个人总结不自动上传QMind或其他云端服务。历史模拟评测中的同步行为仅代表旧版，不是当前隐私策略。

## 2026-11-09 接入验证记录

以下是接入阶段历史记录；后续知识与行为评测见文末及完整报告。

- 内容覆盖检查通过：7章、19个ID、19条题链、33个来源，依赖无环、本地链接有效，原方案13个ID全部保留。
- Node协议实验16/16通过：任意二段字节切分、逐字节、重复、缺口、快照、未知输入、取消竞争、旧scope与有界帧。
- Skill格式校验通过；原Agent静态检查通过，兼容27个历史进度ID。路由表已按规则审阅，未宣称已运行独立模型行为eval。
- Agent/Go原有4份进度与错题文件SHA-256与本轮开始时相同；Java/Agent/Go原有图谱ID保留。
- 浏览器、读屏、性能、服务端授权与完整产品验收未执行，继续使用小册实验矩阵作为这些层的验收要求。

## 2026-11-09 知识与行为评测

此节记录隐私改版前的历史模拟评测，不表示后续每次Skill修改都重新执行了盲测。当前版禁止自动云同步，实际档案改存忽略目录；不要沿用历史输出中的pending补传策略。

- 24条代表性结论覆盖19点，21条直接支持、1条收窄后支持、2条设计审查；来源追加F34共34条。
- 首轮12情境中10例通过；修复到期错因不匹配、题面未定义术语误判D，换新冷启动执行者复测12/12。
- 代码测试26/26（20协议状态、6语言机制）；6份仓库学习/模板文件哈希不变，旧3领域ID保留。
- [报告与原始证据入口](../../../../../docs/reports/2026-11-09-frontend-evaluation.md)。评测分数是模型执行与模型审阅，不是人类双评或真实插件部署验收。
- 汇总脚本只检查保存结果，不调用模型；重新评测须保留新执行者脱敏输出，不得把重跑脚本当成新的行为实验。
