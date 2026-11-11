# 四域目录与内容一致性校验

## 调整结果

统一为ai-agent、go-backend、java-backend、frontend。教材、阅读图谱、陪练参考、辅助材料与评测按领域贯通。posts和sketches分别是历史问答卡片与图解，已迁入materials各域的legacy；四域均新增当前知识总览和复习卡片。

|领域|图谱ID|正文覆盖|题链|新增行为用例|
|---|---:|---:|---:|---:|
|Agent|33|33|33|5|
|Go|19|19|19|5|
|Java|64|64|64|5|
|前端|19|19|19|5|

Java补入七章完整教材、阅读图谱、来源与维护流程。原64个ID保持兼容，CMS与偏向锁按历史边界处理，避免固定分代比例、并发容器聚合统计和Spring事务条件的过度概括。Go补8条、Agent补12条题链；Go补来源索引和维护流程，并收窄索引、幂等效果和透明流式故障转移的保证范围。

## 实际运行

- `python3 scripts/check_system.py`：四域135点、135题链和公共Markdown链接校验。
- `python3 -m unittest discover -s skills/knowledge-interviewer/scripts -p 'test_*.py'`：16项通过，包含已有serve档案兼容、空环境命名及隐私防护。
- `node --test handbook/frontend/examples/*.test.mjs`：26项通过。
- `check_ai_agent_domain.py`、`check_frontend_domain.py`：通过。
- `check_frontend_eval_results.py`：历史证据与评分结构通过；原baseline10/12、retest12/12结论保留，未重跑模型。
- `check_learning_privacy.py`与`git diff --check`：通过。

## 评测限制

四域统一新增20个合成行为用例及预定rubric，状态为not_run，未执行新的冷启动模型评测，不能据静态校验声称陪练行为全部通过。Java教材本轮按来源和稳定ID校验，没有新增Java运行时实验。四域内容广度不同，目录契约一致不表示覆盖了全部面试知识。

本轮不修改、不移动真实个人学习档案，不重写历史Git记录。serve输入别名和既有本地状态目录保留兼容，公共目录已使用go-backend规范名。
