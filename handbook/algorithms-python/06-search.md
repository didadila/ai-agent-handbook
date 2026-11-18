# 6. 回溯搜索

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.backtracking — 回溯、剪枝与去重

**入门简介。** 回溯逐层尝试选择，记录路径，返回上一层时撤销选择，继续探索其他分支。

**生活比喻与边界。** 像走迷宫到岔路尝试一条再退回；能否重复走某格和何时停止仍由题目决定。

**结论与机制。** 先定义决策树的一层选择什么，再维护路径与可选集合。递归前选择、返回后撤销；保存答案必须复制当前路径。同层去重防重复答案，同一路径内是否可重用元素由题意决定。排列、组合、子集的start/used语义不同。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 例子返回多重集合的唯一子集，先排序副本并跳过同层相等项。最坏时间/输出空间O(n*2^n)，辅助路径和递归O(n)。剪枝必须证明不漏解；含负数时不能随意以当前和超标剪枝。 |
| 构造反例 | 把path直接append进答案后继续pop，会让多个答案共享可变列表。 |
| 掌握判据 | 能区分同层与同路径去重、选择/撤销配对以及输出规模成本。 |

**Python实现。** `unique_subsets`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def unique_subsets(nums):
    values, answer, path = sorted(nums), [], []
    def visit(start):
        answer.append(path.copy())
        for i in range(start, len(values)):
            if i > start and values[i] == values[i - 1]:
                continue
            path.append(values[i])
            visit(i + 1)
            path.pop()
    visit(0)
    return answer
```

**手推与自测。** 只指出记录回溯答案应保存path还是path.copy()。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
