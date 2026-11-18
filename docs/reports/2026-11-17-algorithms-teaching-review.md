# Python算法二次核验与陪练上下文修订

日期：2026-11-17。范围为新算法卷26个稳定知识点、对应Python实现与题链，以及全部六域共用的陪练/讲解规则。全仓197点做结构校验；本轮没有对其余五域全部正文重新进行逐条事实审稿。不能把本记录理解为绝对无误的保证。

## 发现与修订

| 问题 | 处理 |
|---|---|
| 首次接触缺简介，题库可能引用未展示的函数与场景 | 算法26点逐点补白话用途、生活比喻和边界；重写各点两条追问及最小验证，明确输入、变量、节点、契约和一个动作 |
| 题库把正确机制反例列为“错误靶子”，可能误用于判错 | 改为“内部边界核对”，不把其中正确结论当成错误答法 |
| 泛用“不变量”追问不适合每个点 | 改为与当前机制对应的具体情境；追问按需取一条，不要求逐条做完 |
| 本地拓扑边与课程表题面方向易混淆 | 本地(u,v)为u→v；题面[a,b]为b→a，需转换 |
| 最大子数组丢负前缀的表述可能误导全负输入 | 明确要求非空时全负结果为最大单元素，而非0 |
| 公共自造题模板夸大双亲委派的去重范围 | 按JVMS §5.3补类名+定义加载器身份；Tomcat默认普通应用类本地优先与例外、delegate=true及实际类定义归属分别说明 |
| Skill有题面有效性原则，但没有落实所需背景的模板 | 主入口及teaching-context.md强制定义对象、用途、场景、术语和影响答案的前提；题面缺陷不记C/D、错题或复习进度 |
| 简短格式挤压解释和图示 | 展示协议v4允许短Mermaid流程图；默认保持三段，用户明确展开则允许比喻+图+代码，仍只一个或零个作答动作 |

概念学习采用“白话是什么/有何用 → 生活比喻和技术映射、失配边界 → 真实机制的表格/流程/状态追踪 → 最小验证”。补足对象定义不等于提前泄漏推导；如果已讲出本题答案，标讲解后验证，不能当独立诊断或直接判A。跨域规则不要求给学习者展示内部知识点编号。

## 核验依据

| 核验项 | 原始依据 |
|---|---|
| 排序稳定性、原地与返回值 | [Python 3.11 Sorting HOWTO](https://docs.python.org/3.11/howto/sorting.html) |
| 堆、二分和整数位操作 | [heapq](https://docs.python.org/3.11/library/heapq.html)、[bisect](https://docs.python.org/3.11/library/bisect.html)、[int.bit_count](https://docs.python.org/3.11/library/stdtypes.html#int.bit_count) |
| 惰性堆旧项、并查集均摊与背包遍历 | [Dijkstra](https://cp-algorithms.com/graph/dijkstra_sparse.html)、[DSU](https://cp-algorithms.com/data_structures/disjoint_set_union.html)、[Knapsack](https://cp-algorithms.com/dynamic_programming/knapsack.html) |
| 严格递增与最小结尾状态 | [LIS](https://cp-algorithms.com/dynamic_programming/longest_increasing_subsequence.html)，另以小规模子序列枚举核对本地实现 |
| 类身份和Tomcat策略 | [JVMS 21 §5.3](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html#jvms-5.3)、[Tomcat 10.1 Class Loader](https://tomcat.apache.org/tomcat-10.1-doc/class-loader-howto.html) |

实现按既定输入契约审读，未发现测试覆盖范围内的结果错误；复杂度区分最坏/均摊/期望、辅助/输出空间和Python切片/哈希成本。Dijkstra保留惰性堆O(E)项的口径；不把大整数操作一概视为常数。

## GitHub借鉴

采用[Mermaid](https://github.com/mermaid-js/mermaid)的文本流程图方法，以及[Python Tutor](https://pythontutor.com/)逐步展示变量、引用和栈帧的思路。Python Tutor的[GitHub文档仓库](https://github.com/pythontutor-dev/pythontutor/blob/master/unsupported-features.md)当前主要为文档，不是可直接部署的完整源码；其中不支持的并发/异步场景不能拿来证明线程或asyncio行为。CP-Algorithms用作证明与复杂度的原始参考。

本轮只补充Skill内的选择规则和回退方法，没有安装服务、接入外部执行器或上传个人答案/业务代码。Mermaid无渲染环境时使用文字箭头；格式脚本验证受限语法与规模，不声称实际渲染成功。

## 实际执行的检查

| 检查 | 结果 |
|---|---|
| check_system.py | 六域197个稳定点，0错误 |
| 算法unittest | 21项通过；默认Python 3.10.16、Python 3.13.2、3.14.5均执行通过 |
| Python 3.11语法 | ast按3.11语法解析通过；本机没有3.11运行时，不声称执行过3.11测试 |
| Skill脚本unittest | 74项通过；包括流程图边界、未定义节点、超规模、额外段落、内部编号外露和原有回归 |
| quick_validate.py | Skill is valid；仅Skill结构检查 |
| check_learning_privacy.py | PASS；测试不读取或写入真实个人档案 |
| check_behavior_eval_runs.py | 定义/既有档案信封一致；不是本轮模型行为复评 |
| check_fix_regressions.py（原v3套件） | 历史16例/79条信封及原证据检查通过；原语义评分不变，不是重跑16例 |

新增独立参照：零钱问题与无权最短路搜索对拍、LCS与子序列集合交集对拍，以及负数滑动窗口、不同下标、课程边方向、背包重复选择、整数掩码等反例断言。正文代码AST与实际测试模块逐段比对。

## 尚不能证明的事项

- 新算法域6例、上下文专项8例均为not_run；后者覆盖六域，rubric在执行前声明。没有模型原始输出与逐项评审就不报告行为通过，不能用74项脚本测试冒充。
- 旧Python后端归档仍是5/6例、21/22条；本轮未修复或重评该历史失败。旧四域与v3成绩仅代表旧运行。
- 未进行牛客/力扣提交，不声称平台AC；平台题单未逐题完整复核。边界测试也不等于覆盖所有变体或任意恶意输入。
- 本轮维护仓库中的Skill，不覆盖Qoder或其他宿主的全局安装副本；宿主必须实际加载本仓库修订版本才会应用新规则。
- 个人记录未被用作夹具；未提交、未推送。既有与本任务无关的工作区修改保留。
