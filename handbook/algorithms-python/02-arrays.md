# 2. 数组与字符串

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.hash — 哈希查找与计数

**入门简介。** 哈希表按键保存和查找信息，适合把已见过的数、次数或位置记下来。

**生活比喻与边界。** 像用姓名查通讯录；名字相同的两个人仍需额外身份信息，不能把键和真实身份混为一谈。

**结论与机制。** 两数配对可把已扫过的值映射到下标，用目标减当前值查历史。必须先查询再登记当前项，否则可能重复使用自己。计数问题用频数而非集合；字符串异位词可用计数或排序签名，字母表固定与Unicode一般输入的代价不同。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 同值的不同下标允许配对；重复值会覆盖历史下标，但对存在性/任意一对的契约可接受。不能把集合去重当作计数。 |
| 构造反例 | [3,3] target=6 需要两个不同下标，先写入会错误匹配自身。 |
| 掌握判据 | 说明扫描前字典只含历史下标，平均O(n)时间、O(n)辅助空间及哈希最坏边界。 |

**Python实现。** `two_sum`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None
```

**手推与自测。** 只指出两数配对时先查表还是先登记当前值。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.two-pointers — 双指针与快慢指针

**入门简介。** 双指针用两个位置协作扫描；每次移动都要有理由，保证被跳过的候选不会是答案。

**生活比喻与边界。** 像在已按价格排好的货架两端选搭配；货架没排序时，移动方向就未必正确。

**结论与机制。** 有序两数和中，两端和太小可排除整个左端候选，太大可排除右端，这依赖排序单调性。三数和固定一个元素后做双指针并去重。原地去重用读指针遍历、写指针维护有效前缀。快慢指针用于链表中点与环，不是按值去重。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 排序会丢失原下标语义；需要下标时保留索引或用哈希。while left<right保证不用同一位置。 |
| 构造反例 | 无序[5,1,4]上直接双指针并没有正确的排除依据。 |
| 掌握判据 | 能证明被排除集合不含答案；O(n)扫描不含排序，排序另计。 |

**Python实现。** `sorted_pair`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def sorted_pair(nums, target):
    """输入非递减，返回不同位置的任意一对下标。"""
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None
```

**手推与自测。** 只解释有序两数和过小时为什么可以排除当前左端。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.window — 滑动窗口与可维护条件

**入门简介。** 滑动窗口维护一段连续范围，边移动边更新范围内的信息，减少重复计算。

**生活比喻与边界。** 像移动相框观察连续街景；这只说明连续范围，不证明任意条件都能只向前移动。

**结论与机制。** 窗口用于连续子串/子数组。无重复子串可维护每个字符最后出现位置，左端只前进；遇到窗口外的历史重复不能让左端倒退。最小覆盖用计数与满足条件的字符种类维护，固定窗口和变长窗口不是同一个模板。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 正数和达到阈值时可收缩，不代表含负数也适用；负数会破坏和的单调性，需前缀和等方法。Unicode这里按Python字符计数，不按用户感知字形簇。 |
| 构造反例 | abba若直接left=last[c]+1，最后一个a会让left倒退。 |
| 掌握判据 | 说明窗口不变量、max保单调、O(n)指针移动和O(字符集)空间。 |

**Python实现。** `longest_unique`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def longest_unique(text):
    last, left, best = {}, 0, 0
    for right, char in enumerate(text):
        left = max(left, last.get(char, -1) + 1)
        last[char] = right
        best = max(best, right - left + 1)
    return best
```

**手推与自测。** 只写出处理abba最后一个a时左边界是否应后退。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.prefix — 前缀和、差分与子数组计数

**入门简介。** 前缀和记录从开头累计到各位置的总和，用两个累计值相减表示中间一段。

**生活比喻与边界。** 像用两次水表读数算用水量；相同读数出现多次时仍对应不同时间点，不能丢掉次数。

**结论与机制。** 前缀p[0]=0对应空前缀，区间[l,r)之和为p[r]-p[l]。连续子数组和为k，等价于寻找此前前缀等于当前前缀减k，用频数累计而不是只存存在性。差分把区间增加变成两次边界修改，最后前缀恢复；二维前缀用容斥。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 先查询再加入当前前缀，避免k=0时把空子数组算入。含负数仍可用前缀频数；大量静态区间和与动态单点更新应分别考虑前缀和/Fenwick等扩展。 |
| 构造反例 | [0,0] target=0有3个非空连续子数组，不是集合中的1个。 |
| 掌握判据 | 区分历史空前缀和空子数组；期望O(n)时间、O(n)空间。 |

**Python实现。** `subarray_count`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def subarray_count(nums, target):
    counts, total, answer = {0: 1}, 0, 0
    for x in nums:
        total += x
        answer += counts.get(total - target, 0)
        counts[total] = counts.get(total, 0) + 1
    return answer
```

**手推与自测。** 只解释为何频数表需要以{0:1}初始化。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.binary — 二分边界与答案二分

**入门简介。** 二分查找在有序或判定结果单调的候选范围中，每次排除一部分不可能的答案。

**生活比喻与边界。** 像按页码查书逐步缩小范围；如果页码乱序，中间值不能指导排除哪半边。

**结论与机制。** 先定义要找的第一个满足条件的位置。lower_bound在有序数组中找第一个>=target，使用半开区间[lo,hi)，返回n是合法插入点。答案二分还需要可证明单调的可行性判定，如速度增加使完成时间不增；不是所有优化问题都能二分。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 空数组、全部小于、全部大于、重复元素都要手推；每次更新必须缩小区间。bisect查找O(log n)，在list中插入仍O(n)。 |
| 构造反例 | 在[1,2,2,4]查2应返回1，不是任意一个2的位置。 |
| 掌握判据 | 解释左右排除区与终止时位置的含义，不混用闭区间更新。 |

**Python实现。** `lower_bound`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

**手推与自测。** 只写出lower_bound在[1,2,2,4]查2的结果。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.matrix — 矩阵、网格与边界

**入门简介。** 网格可看成每格是一个点、相邻格之间有边的图；连通块是一组能沿允许方向互达的格子。

**生活比喻与边界。** 像给地图中的相连陆地分岛屿；是否允许对角走必须由题目定义。

本例的0/1是整数；平台若给的是字符网格'0'/'1'（例如常见的岛屿题接口），应改成字符比较或显式转换，不能不核对类型就提交。本卷函数不是平台Solution的原样替身。

**结论与机制。** 网格可视为每格最多四条边的图。先确定矩形/空矩阵、邻接方向、是否允许修改原图，再选DFS/BFS。岛屿用已访问集合或原地标记，入队时标记可避免重复入队；二维查找还要区分全局行序与仅行列分别有序。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 下面按0/1矩形且四邻接计岛屿，保留输入，O(rows*cols)时间和空间；八邻接会得到不同答案，不能默认斜对角相连。 |
| 构造反例 | [[1,0],[0,1]]四邻接有2个岛，八邻接有1个。 |
| 掌握判据 | 能定义邻接与访问时机，检查单行、单列、全0、全1及输入是否被改。 |

**Python实现。** `islands`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
def islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    if any(len(row) != cols for row in grid):
        raise ValueError("rectangular grid required")
    visited, answer = set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or (r, c) in visited:
                continue
            answer += 1
            visited.add((r, c))
            queue = deque([(r, c)])
            while queue:
                x, y = queue.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
    return answer
```

**手推与自测。** 只写出该对角网格按四邻接的岛屿数。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
