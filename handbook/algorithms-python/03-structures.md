# 3. 线性结构与索引

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.linked — 链表操作与身份

**入门简介。** 链表把节点靠next引用串起来；节点的值与节点本身的身份是两回事。

**生活比喻与边界。** 像每张卡片写着下一张卡片的位置；两张卡内容一样也不是同一张卡。

**结论与机制。** 反转需要先保存后继，再改next，否则会丢失余链。虚拟头统一删除首节点与普通节点；合并有序链表维持已接好前缀。Floyd相遇后把一个指针放回头部同速走可找环入口，证明依赖步长与环长关系。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 按节点身份而不是val判断相遇/相交。反转例子只接受无环链表，原地O(n)时间O(1)空间；递归版还用O(n)调用栈。 |
| 构造反例 | 两个值都为1的节点不一定是同一节点。 |
| 掌握判据 | 能在纸上追踪prev/current/following，不断链，覆盖空链和单节点。 |

**Python实现。** `reverse_list`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def reverse_list(head):
    """无环链表；改变原节点的next。"""
    previous = None
    while head is not None:
        following = head.next
        head.next = previous
        previous, head = head, following
    return previous

def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False
```

**手推与自测。** 只指出反转next前必须保存哪个引用。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.stack — 栈、括号与单调栈

**入门简介。** 栈是后放入的先取出；单调栈额外让待处理元素按某种大小关系排列。

**生活比喻与边界。** 像叠盘子只能先拿顶层；大小关系是算法额外维护的，不是所有栈天然拥有。

**结论与机制。** 括号匹配维护尚未匹配的开括号；遇到闭括号必须匹配最近一个。单调栈保存尚未找到下一个更大值的下标；严格更大时相等值不能弹出。元素各进出一次，嵌套while总时间仍O(n)。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 栈存下标才能计算距离；最大矩形等题的相等边界需单独定义，不能机械复用比较符。Python用list尾部append/pop而不是pop(0)。 |
| 构造反例 | 温度[70,70,71]答案[2,1,0]，相等不是更暖。 |
| 掌握判据 | 讲清何时能确定被弹元素的答案，辅助栈最坏O(n)。 |

**Python实现。** `daily_temperatures`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def daily_temperatures(values):
    result, stack = [0] * len(values), []
    for i, value in enumerate(values):
        while stack and values[stack[-1]] < value:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result

def valid_brackets(text):
    pairs, stack = {")": "(", "]": "[", "}": "{"}, []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char not in pairs or not stack or stack.pop() != pairs[char]:
            return False
    return not stack
```

**手推与自测。** 只写出[70,70,71]每日等待更暖天数。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.heap — 堆、Top K 与优先队列

**入门简介。** 堆是一种方便反复取最小值或最大值的结构；它不保证其余元素整体排好序。

**生活比喻与边界。** 像候诊系统先叫当前优先级最高的人；不能据此说候诊名单的每个位置都已排序。

**结论与机制。** 最小堆只保证堆顶最小，不保证整个数组有序。保留最大的k项时维护大小k的最小堆，堆顶就是当前第k大。重复元素按出现次数计算；多路合并把每路当前头放堆，每弹出一个再补该路后继。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | heapify线性建堆；本实现O(n log(k+1))时间、O(k)空间，k必须在1..n。Python3.11用负数模拟数值最大堆；同优先级的不可比较对象应加唯一序号，不能直接比较对象。 |
| 构造反例 | 第2大不是第2个不同的大值，[5,5,3]应返回5。 |
| 掌握判据 | 能说清堆内集合与阈值含义，不把heappushpop和heapreplace的空堆/顺序语义混淆。 |

**Python实现。** `kth_largest`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def kth_largest(nums, k):
    if not 1 <= k <= len(nums):
        raise ValueError("1 <= k <= n")
    heap = list(nums[:k])
    heapify(heap)
    for i in range(k, len(nums)):
        heappushpop(heap, nums[i])
    return heap[0]
```

**手推与自测。** 只解释为何找第k大要维护最小堆。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.trie — 字典树与前缀查询

**入门简介。** 字典树让多个词共享开头相同的字符路径，并用单独标记表示一个词已经结束。

**生活比喻与边界。** 像地址从省到市逐级分叉；路径经过某地不代表完整地址就在这里结束。

**结论与机制。** 把字符作为边逐层共享前缀，单词结束必须单独标记。查单词要求结束标记，查前缀只要求路径存在；删除还需引用/计数，不能简单删共享路径。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 插入/查询期望O(L)，空间与不同前缀总数相关；大量稀疏Unicode字典有对象开销。结束标记用独立对象，避免与普通字符冲突。空前缀始终存在，空词只有插入后才存在。 |
| 构造反例 | 插入apple后查前缀app成立，但查完整词app不成立。 |
| 掌握判据 | 区分路径存在与词终止，能处理空词、重复词和含特殊字符的词。 |

**Python实现。** `Trie`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
class Trie:
    END = object()
    def __init__(self):
        self.root = {}
    def insert(self, word):
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node[self.END] = True
    def _node(self, word):
        node = self.root
        for char in word:
            if char not in node:
                return None
            node = node[char]
        return node
    def contains(self, word):
        node = self._node(word)
        return node is not None and self.END in node
    def starts_with(self, prefix):
        return self._node(prefix) is not None
```

**手推与自测。** 只判断插入apple后contains('app')的结果。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
