# 来源、版本与证据边界

核对日期：2026-11-17。采用平台官方入口、Python官方文档与算法参考项目原始资料作依据；教程正文、微型题面与代码为本项目原创整理。题单说明只是站点定位，不采纳其营销覆盖率作为实测结论。

| 来源 | 本卷用途 | 核对范围 |
|---|---|---|
| [力扣热题100](https://leetcode.cn/studyplan/top-100-liked/) | 常见面试题型导航 | 公开入口与题单说明；不声称完整复刻100题 |
| [牛客模板速刷TOP101](https://www.nowcoder.com/exam/oj/ta?tpId=295) | 链表、二分、树、哈希、DP、双指针、贪心等分类导航 | 公开题单与核心代码模式说明；不假设所有题是ACM |
| [Python3.11 collections](https://docs.python.org/3.11/library/collections.html) | deque/Counter与队列接口 | 不把deque等同于list头删 |
| [Python3.11 heapq](https://docs.python.org/3.11/library/heapq.html) | 最小堆接口、优先队列 | 以3.11兼容写法为基础，不依赖新版本最大堆API |
| [Python3.11 bisect](https://docs.python.org/3.11/library/bisect.html) | 插入点与二分边界 | 区分查找代价和list插入代价 |

直接核验的代表题：[两数之和](https://leetcode.cn/problems/two-sum/)、[无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)、[课程表](https://leetcode.cn/problems/course-schedule/)、[网络延迟时间](https://leetcode.cn/problems/network-delay-time/)。这些题的完整限制与判定以原页为准，本卷构造输入不冒充原题。

部分独立题页请求超时（前缀和计数、分割等和子集）；没有将超时当作题面核验成功。练习索引其余题名是检索线索，不是逐页验题记录，更不是付费题收录或平台AC成绩。

本地确定性测试只能证明其断言覆盖的实现性质；没有牛客/力扣真实提交成绩，也没有把新领域陪练行为用例标为已执行。学习者状态不在公共目录；不读取真实档案做测试。

更新策略：算法不变量通常稳定；平台题面/语言版本/题目归属、Python新API、运行上限属于易变事实，使用前核对官方页面。算法示例默认Python3.11+，提高递归上限不能保证安全运行。自定义图的点号、边权、区间语义均由正文契约限定，不外推平台所有变体。

## 二次核验：2026-11-17

| 疑点 | 核验依据与处理 |
|---|---|
| sorted稳定性、sort返回值 | [Python排序说明](https://docs.python.org/3.11/howto/sorting.html)：同键保持顺序，sort原地且返回None；正文保持 |
| heapify、固定大小堆 | [heapq官方文档](https://docs.python.org/3.11/library/heapq.html)：线性建堆、heappushpop与heapreplace不同；不依赖新最大堆API |
| LIS严格递增和tails | [CP-Algorithms LIS](https://cp-algorithms.com/dynamic_programming/longest_increasing_subsequence.html)、[bisect](https://docs.python.org/3.11/library/bisect.html)：最小结尾数组不必是实际子序列；重复值用左插入点；正文与枚举对拍一致 |
| 惰性Dijkstra堆项 | [CP-Algorithms稀疏图Dijkstra](https://cp-algorithms.com/graph/dijkstra_sparse.html)：跳过旧状态，堆可保留多条同节点候选；本地保留log(E+2)口径，不无条件声称堆O(V) |
| 并查集复杂度 | [CP-Algorithms DSU](https://cp-algorithms.com/data_structures/disjoint_set_union.html)：路径压缩与按大小合并是均摊近常数，不是每次最坏O(1) |
| 0/1背包容量顺序 | [CP-Algorithms背包](https://cp-algorithms.com/dynamic_programming/knapsack.html)：倒序使来源状态仍属于上一件物品；与可无限重复选取的完全背包区分 |
| 负数位数 | [Python int.bit_count](https://docs.python.org/3.11/library/stdtypes.html#int.bit_count)：按绝对值计数，有限位宽先掩码；新增可执行反例断言 |
| 接口含义不一致 | 明确本地topological_order边(u,v)表示u→v，课程表[a,b]需转(b,a)；网格实现用整数0/1，题面若给字符须适配 |
| 最大子数组空集边界 | 补充“要求非空、全负时返回最大单元素”，不能因丢弃负前缀误返回0 |

复杂度默认以基本整数操作为单位成本；任意精度大整数成本另外计算。算法参考项目不是平台语言规范，不能用C++容器复杂度直接代替Python容器成本。二次核验的测试、范围与未完成评测见[校验记录](../../../../../docs/reports/2026-11-17-algorithms-teaching-review.md)。
