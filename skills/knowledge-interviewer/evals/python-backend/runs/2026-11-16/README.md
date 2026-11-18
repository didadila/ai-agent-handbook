# Python 后端合成单轮评测 — 2026-11-16

## 协议

先定义6个case和22条rubric，再并行启动新旧Skill各6个独立冷启动执行体。执行体只接收原始prompt、只读合成fixture、指定Skill及输出边界，不读取rubric、其他运行或真实个人档案；每例输出一轮response和五字段execution记录。本目录归档新版；旧版对照与计时保留在[评审工作区](../../../../../knowledge-interviewer-workspace/iteration-1/protocol.json)。

新版使用仓库Python领域和实际教材定位器；旧版使用提交`2e4a02c5a7cfe6ff1d18158defd8e4e4a38676bc`的Skill快照，无新Python包。工作区`without_skill`代表旧版，不是无Skill。主Skill内容SHA256：新版`f45f58fd2124b51f36e4059ee6e2618595eec5f8ff9925ae9195a82828f140fc`，旧版`4173faccab22d21ee8938d0462d51f8efa4e1ea6a7c92c0207e6447a2a15e37d`。

独立评分执行体阅读实际输出及execution，按原rubric逐项给出引用和理由；格式粗检不替代事实与单个作答动作的判断。主代理复核评分、教材定位和汇总。输出不回写为实际用户学习成绩。

## 结果

[原始输出与读取记录](evidence.md)按case归档；[逐项评分与实际计数](grades.json)保留全部判据和失败。`case_pass`仅在该例所有判据满足时为真。原四域历史成绩不重算，不与本域合并宣称全系统通过。

[静态评审页](../../../../../knowledge-interviewer-workspace/iteration-1/review.html)包含12份新旧输出和逐项评分；[benchmark](../../../../../knowledge-interviewer-workspace/iteration-1/benchmark.json)记录跨6种case的聚合指标。

## 限制

每例每版仅一次采样；执行与评分同族，尚无人类评审，也未测多轮长期学习效果。旧版缺Python资源，因此差异是路由、内容和流程的联合变化，不是单独一句提示的因果效果。跨case标准差不是同case重复运行稳定性。

`public_reads`是执行体报告的相对路径和范围，已与公共文件/定位器核对，不是完整独立审计的工具转录。privacy例只有只读保存请求，不能证明成功写档流程；私有路径、权限、空表初始化和保留旧记录由独立脚本测试在合成临时目录验证。

未运行真实LLM服务、生产HTTP、云端存储、broker或部署。宿主通知中的subagent_tokens仅原样作为计时附属统计，未核验为可计费token或输出长度；不据此推导成本。仓库Skill已更新不等于全局安装或宿主缓存已更新。
