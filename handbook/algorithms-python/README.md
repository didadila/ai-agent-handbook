# Python算法与数据结构

26个知识点、8章，面向牛客与力扣的常见算法题型。默认Python 3.11+；不要求先学Python后端，未使用第三方依赖。目标是从题目约束辨认可用机制、解释不变量、写出代码并检验反例，不承诺刷完必过面试。

| 章 | 内容 | 知识点数 |
|---|---|---:|
| 1 | [基础与 Python](01-foundations.md) | 3 |
| 2 | [数组与字符串](02-arrays.md) | 6 |
| 3 | [线性结构与索引](03-structures.md) | 4 |
| 4 | [树与搜索树](04-trees.md) | 2 |
| 5 | [图与依赖](05-graphs.md) | 4 |
| 6 | [回溯搜索](06-search.md) | 1 |
| 7 | [动态规划](07-dp.md) | 3 |
| 8 | [贪心与数学边界](08-strategies.md) | 3 |

## 学习顺序

先读[图谱](knowledge-map.md)，按前置推进：Python与复杂度 → 数组题型 → 数据结构 → 树图 → 回溯/DP/贪心。算法域入口是`algorithms-python`；“Python后端”仍走另一卷。讲解优先短表格/流程，陪练一次一题。

| 每道题的处理 | 可检查产物 |
|---|---|
| 明确契约 | 输入规模、是否有序/带负数、是否原地、输出类型、OJ模式 |
| 从暴力找重复工作 | 不变量、状态、单调性或交换证明；不凭标签套模板 |
| 写Python实现 | 小而完整的函数；没有调试打印或依赖平台未提供的类型 |
| 边界与对拍 | 空输入、重复、单元素、负数、不可达、极端形状；与小规模枚举比较 |
| 解释成本 | 最坏/期望/均摊，辅助/输出空间，递归深度与Python容器隐含复制 |

题型练习索引见[practice.md](practice.md)。正式题面、语言环境、时空限制以各平台当前页面为准；题号、题单热度不等于客观面试频率。本文不复制付费题面或整套题解。

## 可运行实现

复杂度默认按基本整数操作为单位成本；大整数的运算和哈希成本还随位数增长。空输入与零容量等边界按代码契约处理，常用复杂度简写不代表这些场景零开销。

除非另有说明，数组/区间输入为可重复遍历的list或tuple，图的邻接点号合法，网格为矩形0/1数据。节点字段为val/next或val/left/right；平台已提供节点类型时保留其定义，不能直接以本地dataclass替换。契约内的边界测试不等于对任意恶意输入的生产校验。

[examples/algorithms.py](examples/algorithms.py)含所有正文函数及节点结构，[examples/acm_pairs.py](examples/acm_pairs.py)演示独立ACM入口。函数式平台通常需要包装为`class Solution`的方法；牛客同样有核心代码模式，不能把所有牛客题都当ACM。提交前确认方法名、节点字段、返回值或打印约定。

```bash
python3 -m unittest discover -s handbook/algorithms-python/examples -p 'test_*.py' -v
python3 skills/knowledge-interviewer/scripts/learning_content.py --domain algorithms-python --point alg.window
```

所有实现为原创教学代码，不声称已经在牛客/力扣提交AC。验证结果以实际执行的测试和[来源/维护记录](../../skills/knowledge-interviewer/references/domains/algorithms-python/sources.md)为准。代码可运行不等于覆盖本主题所有变体。

2026-11-17二次核验补充了全卷入门简介、带边界的生活比喻与自包含题面，修正了课程表边方向的接口歧义和非空最大子数组的全负边界。范围与证据见[校验记录](../../docs/reports/2026-11-17-algorithms-teaching-review.md)。

## 本卷边界与扩展

基础面试核心不等于算法竞赛全集。Fenwick/线段树、KMP、复杂字符串、最小生成树、强连通、网络流、数论与计算几何作为后续专题；不假装一个模板覆盖全部。树点可继续扩展前中后序、LCA与直径；序列DP点可继续展开编辑距离、回文区间、打家劫舍与股票状态机。

与Agent项目的可选联系：堆用于优先级任务，拓扑排序识别依赖环，图搜索表示状态可达；实际分布式调度还需幂等、容量与故障语义，不能只凭会刷题宣称工程掌握。学习记录仍仅在被忽略的本地目录，未读取或修改你的个人档案。
