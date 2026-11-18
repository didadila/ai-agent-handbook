# 8. 贪心与数学边界

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.greedy — 贪心的选择证明

**入门简介。** 贪心每步选择当前看来最有利的方案；只有证明这种选择不损失全局答案时才可靠。

**生活比喻与边界。** 像采购时总先拿最便宜的商品；有套餐、额度等限制时，这种直觉可能失效。

**结论与机制。** 贪心需要交换论证、支配关系或可扩展性证明，而不是凭直觉选当前最大。跳跃可达维护已扫描位置能覆盖的最远点，遇到覆盖不到的下标立即失败。最大子数组可把负贡献前缀丢掉（也能用DP表述），但若要求非空，全负输入仍应返回最大单个元素，不能默认0；零钱最少不能对任意币制贪心。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 例子为非负最大跳距，目标是否能到最后；不返回最少跳数，空输入约定False。O(n)时间O(1)空间。最少跳数要按当前层覆盖区间计步，不能简单统计更新最远点次数。 |
| 构造反例 | 币值[1,3,4]金额6，最大面额先拿需3枚，最优是3+3两枚。 |
| 掌握判据 | 能说明何种局部选择可安全保留；找不到证明就考虑DP或反例。 |

**Python实现。** `can_jump`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def can_jump(nums):
    """非负跳距；空数组没有起点。"""
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
        if farthest >= len(nums) - 1:
            return True
    return False
```

**手推与自测。** 只给出该币制使最大面额贪心失败的一种凑法。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.intervals — 区间合并与调度

**入门简介。** 区间表示两个端点之间的范围；合并区间求它们覆盖的整体范围，不是挑最多个互不重叠区间。

**生活比喻与边界。** 像合并重叠预约时段；现实常用半开时间段，本例却用包含两端的闭区间，端点规则不能照搬。

**结论与机制。** 合并区间先按起点排序，维护已合并前缀最后一段的最远终点；当前段与末段相交时更新终点，否则开新段。选择最多不重叠活动通常按最早结束排序，目标不同不能套同一排序规则。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 这里是闭区间，端点相接也合并；半开区间的重叠定义要重定。O(n log n)时间、O(n)输出/排序空间，排序副本不改原输入。 |
| 构造反例 | [1,2]和[2,3]按闭区间重叠；[1,2)和[2,3)不重叠。 |
| 掌握判据 | 定义端点语义并证明扫描不遗漏，区分并集与最多活动数。 |

**Python实现。** `merge_intervals`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def merge_intervals(intervals):
    if any(start > end for start, end in intervals):
        raise ValueError("start <= end required")
    answer = []
    for start, end in sorted(intervals):
        if answer and start <= answer[-1][1]:
            answer[-1] = (answer[-1][0], max(end, answer[-1][1]))
        else:
            answer.append((start, end))
    return answer
```

**手推与自测。** 只判断两段闭区间[1,2]与[2,3]是否合并。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.bits — 位运算与数学工具边界

**入门简介。** 位运算逐个二进制位处理整数；异或可以把恰好成对出现的相同值抵消。

**生活比喻与边界。** 像成对划掉同编号票据；出现三次或缺失配对时，抵消结论就不再适用。

**结论与机制。** 异或满足交换、结合、x^x=0、x^0=x，所以每个值恰好出现两次、只有一个出现一次时可整体异或。它不是任意频数的去重器。标志位用与/或/异或，移位和掩码先定义位宽。最大公约数用math.gcd，模幂用pow(a,b,m)，避免先构造巨大a**b。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | Python int不限制32位；负数位运算按无限符号扩展的语义，有限宽度问题先掩码。int.bit_count对负数按绝对值计1，不是固定补码宽度。例子扫描O(n)次异或，位操作成本另随整数长度增长。 |
| 构造反例 | -1的8位无符号表示需(-1)&255，不能直接把bit_count当8位补码位数。 |
| 掌握判据 | 陈述出现次数假设、整数位宽与符号边界，不能声称任意整数操作永远O(1)。 |

**Python实现。** `single_number`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def single_number(nums):
    if not nums:
        raise ValueError("nonempty paired input required")
    result = 0
    for x in nums:
        result ^= x
    return result
```

**手推与自测。** 只写出(-1 & 255).bit_count()。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
