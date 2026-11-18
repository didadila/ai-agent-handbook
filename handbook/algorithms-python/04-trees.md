# 4. 树与搜索树

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.tree — 二叉树遍历与递归分解

**入门简介。** 二叉树的每个节点最多有左右两个孩子；遍历规定以什么顺序访问所有节点。

**生活比喻与边界。** 像组织结构逐层点名；这里不允许一个孩子由多个父节点共享，否则不再是本例的树。

**结论与机制。** 前序先处理根，中序在左右之间，后序在子问题返回后合并。层序BFS用队列，每层固定本轮队列长度。递归要先定义返回值：高度、是否找到目标或子树答案不能混用；最近公共祖先与直径通常需要后序汇总。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 层序时间O(n)、队列O(最大宽度)。退化树递归深度O(n)，Python可能RecursionError；提高递归上限不是无限栈保证。重建树常用遍历序列+索引表，但重复值会破坏简单唯一定位。 |
| 构造反例 | 树高大不等于层宽大；链状树的层宽为1。 |
| 掌握判据 | 解释队列本轮/下一轮边界，能用显式栈替换深递归。 |

**Python实现。** `level_order`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def level_order(root):
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)
    return result
```

**手推与自测。** 只指出层序遍历每一层开始时为何固定队列长度。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.bst — 搜索树的全局约束

**入门简介。** 二叉搜索树给整棵左右子树施加大小规则，帮助排除不可能的查找方向。

**生活比喻与边界。** 像按编号分区管理档案；检查某区首个文件合规不代表整个区间都合规。

**结论与机制。** 严格BST要求左子树所有值小于根、右子树所有值大于根。检查父子关系不够，需传递上下界，或用中序严格递增。第k小可在中序计数，修改树后维护子树大小才支持更快秩查询。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 这里重复值视为非法；若题目允许重复必须重新定义落点。验证最坏O(n)时间O(h)辅助栈；平衡BST查找O(log n)，任意BST最坏O(n)。 |
| 构造反例 | 根10，左孩子5，5的右孩子12满足局部父子但不是BST。 |
| 掌握判据 | 能携带祖先边界、处理空树与极端整数，不使用固定32位哨兵误判。 |

**Python实现。** `valid_bst`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def valid_bst(root):
    stack = [(root, None, None)]
    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue
        if (low is not None and node.val <= low) or (high is not None and node.val >= high):
            return False
        stack.append((node.left, low, node.val))
        stack.append((node.right, node.val, high))
    return True
```

**手推与自测。** 只判断这个10/5/12的树是否合法。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
