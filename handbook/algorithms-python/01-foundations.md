# 1. 基础与 Python

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.python — Python 刷题与 OJ 输入输出

**入门简介。** OJ（在线判题）接收你的函数返回值或标准输出，先认清交付方式才能让正确计算被判题器识别。

**生活比喻与边界。** 像交作业要按老师要求交表格或答题纸；这是接口约定，不决定算法好坏。

**结论与机制。** 先明确函数式核心代码还是标准输入输出，再按约束选容器。Python 3.11+、零基下标；list切片会复制，字符串不可变；dict/set键须可哈希。计数用Counter，队列用deque，反复拼接字符串用列表加join；多组输入按题面读，不能把首行计数当数据。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 矩阵用列表推导逐行创建，不能用 [[0]*m]*n；不要用eval解析输入，也不要混用bytes与str。Python整数不定宽，但大整数运算不是无限规模下的常数时间。 |
| 构造反例 | a=[[0]*2]*2; a[0][0]=1 会同时改变两行。 |
| 掌握判据 | 两行共享同一内层对象；独立构造每一行，能区分函数返回与ACM打印。 |

**Python实现。** `read_pairs`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def read_pairs(data):
    """ACM示例：每个非空行恰好两个整数，不含组数头。"""
    result = []
    for line in data.splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 2:
            raise ValueError("each line needs two integers")
        result.append(tuple(map(int, fields)))
    return result
```

**手推与自测。** 只写出 [[0]*2]*2 的第二行在第一行首项改为1后的内容。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.complexity — 复杂度、规模与不变量

**入门简介。** 复杂度描述输入变大时工作量怎样增长；不变量是执行过程中持续成立、用来检查步骤的约束。

**生活比喻与边界。** 像估算洗n个碗要多少动作，并检查每洗完一个就多一个干净碗；不能据此预测具体秒数。

**结论与机制。** 先写输入规模n、状态含义及循环不变量，再谈复杂度。最坏、均摊、期望是不同口径；哈希查找平均/期望O(1)不是最坏O(1)。一次扫描不一定线性：循环内切片、查列表或pop(0)都可能线性。输出规模本身也是下界。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 双指针虽嵌套while，只要两个指针各单向移动至多n次仍是O(n)。连续拼接列表会重复复制。空间要区分辅助空间、递归栈与输出。 |
| 构造反例 | 遍历n个元素，每次执行 nums[:i] 再sum，会累计二次工作。 |
| 掌握判据 | 说明每一步的工作与求和，不能按for层数猜；能给反例检验不变量。 |

**Python实现。** `prefix_sums`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def prefix_sums(nums):
    """p[i]是前i个数之和；查询[l,r)用p[r]-p[l]。"""
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    return p
```

**手推与自测。** 只判断对所有i执行sum(nums[:i])的总时间量级。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.sort — 排序、稳定性与分治

**入门简介。** 排序把元素按规则排列；稳定性只讨论规则判断为相等的元素能否保持原先顺序。

**生活比喻与边界。** 像按成绩排队时同分者仍按原队列先后；这里的顺序不是按名字再排序。

**结论与机制。** sorted返回新列表，list.sort原地修改且返回None；相等key保持原顺序称稳定。先选key再排序，不要靠减法比较任意对象。归并排序将已排序子问题线性合并；快速排序平均O(n log n)、最坏O(n²)，随机化也不提供确定性的最坏保证。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | CPython常规比较排序最坏O(n log n)；比较函数成本还要另算。归并需辅助存储；区间题排序不是原始问题自动解决的证明。 |
| 构造反例 | x = nums.sort() 得到None，不是已排序列表。 |
| 掌握判据 | 解释相等key稳定性、原地/返回值与比较成本，区分排序前提及后续算法。 |

**Python实现。** `stable_rank`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def stable_rank(records):
    """按分数升序；同分保持输入顺序。"""
    return sorted(records, key=lambda record: record[1])
```

**手推与自测。** 只写出 records=[('b',1),('a',1)] 按第二项排序后的顺序。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
