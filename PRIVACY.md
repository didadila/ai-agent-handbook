# 公共知识与本地学习档案

本项目供不同学习者使用。Git共享教材、知识点ID、题库、空白模板、工具代码和明确标记为模拟输入的评测；每个人的答题情况相互独立。

| 内容 | 保存位置 | 是否随Git发布 |
|---|---|---|
| 教材与领域图谱 | handbook、skills中的公共知识 | 是 |
| 空白进度/错题模板 | skills/knowledge-interviewer/templates | 是，仅结构和规则 |
| 模拟评测fixture与脱敏结果 | skills/knowledge-interviewer/evals | 是，不接入真实档案 |
| 个人错答、成绩、复习计划 | .local/learning/领域 | 否 |
| 个人偏好、学习起点、会话总结 | .local/learning/preferences、sessions等 | 否 |
| 旧私人记录备份 | .local/learning/archive | 否 |

## 本地使用

从仓库根目录初始化空白档案：

```bash
python3 skills/knowledge-interviewer/scripts/learning_state.py init
python3 skills/knowledge-interviewer/scripts/learning_state.py paths
```

第二条命令只输出本机索引路径，不输出个人正文。用编辑器打开该文件即可查看本地进度和错题。初始化不会覆盖已有档案，不会替用户填成绩。每个人在自己的克隆中得到独立的忽略目录。

默认仓库模式在验证Git根目录、忽略和未跟踪条件后才写入；非Git目录不会自动降级。独立安装使用显式 `init --standalone`，默认状态根为本机用户的.local/share/knowledge-interviewer，或用--root指定Git工作区外的私有目录；新目录0700、新文件0600，现有共享目录拒绝写入而不自动改权限。Git不可用或检查失败均停止保存，Skill不得手写模板绕过。

现有状态根、领域目录和sessions须为0700，现有索引/进度/错题文件须为0600；脚本先检查全部选定目标再创建文件。拒绝后不得自动chmod、切换路径或手写落盘，只有所有者明确授权后才单独补救并重新验证。新建sessions由脚本设为0700，新会话文件按0600创建；此规则不授权修改其他已有路径。

旧版handbook中的进度、错题和个人反馈已停止跟踪；个人记录保存在忽略目录中。本机handbook/agent与handbook/serve的重复档案在确认与.local对应副本逐字节一致后清除，公共教材只使用规范域目录。新陪练只读写当前本地档案。旧的外部学习目录可以手工迁移，目标已有内容先比较，不做覆盖。

个人教学反馈interviewer-feedback.md和表达偏好output-style.md统一放在.local/learning/preferences。Skill按存在情况读取，不给其他学习者继承个人规则。本机根目录的两份历史副本在确认与本地preferences逐字节相同后已清除；忽略规则仍保留，防止旧工具重新生成后误提交。PRIVACY.md本身是所有使用者共用的存储与发布契约，因此保留在根目录，而不是塞入个人偏好或只藏在Skill内。

## 发布边界

- 默认不把个人错题或总结发送到QMind、Pages、云端知识库或其他外部服务；旧pending同步文件也不自动补传。
- 不把真实学习档案作为公共评测fixture，不把成绩、个人学习起点或历史答法写回公共教材。
- 提交前检查Git索引，而不只检查工作区：`python3 skills/knowledge-interviewer/scripts/check_learning_privacy.py --staged`。
- 可使用仓库自带pre-commit钩子：`git config --local core.hooksPath .githooks`。已有自定义钩子时应先合并检查，不覆盖原有配置。
- 忽略规则不是访问控制：强制添加文件、改名复制或自行上传仍可能泄露。不得绕过检查提交私人数据。

已发布过的旧记录从**当前版本**移除，`.gitignore`不会抹除历史提交。清理远端历史涉及重写历史和协作者同步，需要单独处理；本次不会自动强推或重写旧提交。
