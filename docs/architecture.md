# 目录设计与一致性约定

原posts是按天发布的问答图卡，sketches是章节机制图解；两者都是辅助阅读材料，不参与学习者判档。frontend没有sketches是覆盖遗漏。Java原来是独立陪练参考包，只有图谱和部分题库；前端评测则来自上一轮专项验证，不能代表其他领域同样经过验证。

## 统一结构

四个领域：ai-agent、go-backend、java-backend、frontend，以[catalog.json](../catalog.json)为命名契约。公共材料按领域贯通，个人记录继续只存本地。

|旧位置|新位置|
|---|---|
|handbook/agent|handbook/ai-agent|
|handbook/serve|handbook/go-backend|
|references/domains/serve|references/domains/go-backend|
|posts|materials/ai-agent/cards/legacy|
|sketches/agent|materials/ai-agent/maps/legacy|
|sketches/serve|materials/go-backend/maps/legacy|
|教材中的历史审计和评测报告|docs/reports|
|evals/frontend-*|evals/frontend/history/2026-11-09|

四域均提供教材、阅读图谱、陪练map/questions/sources/maintenance、辅助图解与卡片、cases与rubric。保持领域覆盖一致，不强行让各域知识点数量相同。历史素材放legacy，历史评测放history，均保留原版本语境。

学习入口与各材料职责见[学习系统说明](learning-system.md)。Skill需要讲解时按稳定ID定位并读取教材，materials仅按需要展示；目录齐全不证明教学链路已被模型执行。个人输出偏好和教学反馈统一位于忽略目录，不再以根目录历史副本作为配置入口。

## 记录与评测

serve作为go-backend输入别名保留。已有.local/learning/serve继续使用，不移动、不复制原学习档案；新环境使用go-backend。稳定知识点ID不变。

静态校验检查目录、点数、题库、来源和链接；行为评测必须保存实际输出并按预先定义的rubric逐项评审，未执行用例明确标记未运行，不用静态检查冒充冷启动通过。
