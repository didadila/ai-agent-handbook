"""Python3.11+ original teaching algorithms; no external services."""
from __future__ import annotations
from bisect import bisect_left
from collections import deque
from dataclasses import dataclass
from heapq import heapify, heappushpop, heappush, heappop

@dataclass
class ListNode:
    val: int
    next: ListNode | None = None

@dataclass
class TreeNode:
    val: int
    left: TreeNode | None = None
    right: TreeNode | None = None

# alg.python
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

# alg.complexity
def prefix_sums(nums):
    """p[i]是前i个数之和；查询[l,r)用p[r]-p[l]。"""
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    return p

# alg.sort
def stable_rank(records):
    """按分数升序；同分保持输入顺序。"""
    return sorted(records, key=lambda record: record[1])

# alg.hash
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None

# alg.two-pointers
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

# alg.window
def longest_unique(text):
    last, left, best = {}, 0, 0
    for right, char in enumerate(text):
        left = max(left, last.get(char, -1) + 1)
        last[char] = right
        best = max(best, right - left + 1)
    return best

# alg.prefix
def subarray_count(nums, target):
    counts, total, answer = {0: 1}, 0, 0
    for x in nums:
        total += x
        answer += counts.get(total - target, 0)
        counts[total] = counts.get(total, 0) + 1
    return answer

# alg.binary
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

# alg.matrix
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

# alg.linked
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

# alg.stack
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

# alg.heap
def kth_largest(nums, k):
    if not 1 <= k <= len(nums):
        raise ValueError("1 <= k <= n")
    heap = list(nums[:k])
    heapify(heap)
    for i in range(k, len(nums)):
        heappushpop(heap, nums[i])
    return heap[0]

# alg.trie
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

# alg.tree
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

# alg.bst
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

# alg.graph
def bfs_distances(adj, start):
    if not 0 <= start < len(adj):
        raise ValueError("invalid source")
    distance = [-1] * len(adj)
    distance[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance

# alg.topo
def topological_order(n, edges):
    if n < 0:
        raise ValueError("negative size")
    graph, indegree = [[] for _ in range(n)], [0] * n
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("invalid vertex")
        graph[u].append(v)
        indegree[v] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return order if len(order) == n else None

# alg.union
class DSU:
    def __init__(self, n):
        if n < 0:
            raise ValueError("negative size")
        self.parent, self.size = list(range(n)), [1] * n
        self.components = n
    def find(self, x):
        if not 0 <= x < len(self.parent):
            raise IndexError(x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        return True

# alg.shortest
def dijkstra(adj, start):
    n = len(adj)
    if not 0 <= start < n:
        raise ValueError("invalid source")
    if any(not 0 <= v < n or w < 0 for row in adj for v, w in row):
        raise ValueError("nonnegative valid edges required")
    distance = [float("inf")] * n
    distance[start] = 0
    heap = [(0, start)]
    while heap:
        cost, u = heappop(heap)
        if cost != distance[u]:
            continue
        for v, weight in adj[u]:
            candidate = cost + weight
            if candidate < distance[v]:
                distance[v] = candidate
                heappush(heap, (candidate, v))
    return distance

# alg.backtracking
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

# alg.dp
def min_coins(coins, amount):
    if amount < 0 or any(c <= 0 for c in coins):
        raise ValueError("positive coins and nonnegative amount required")
    dp = [0] + [amount + 1] * amount
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return dp[amount] if dp[amount] <= amount else -1

# alg.knapsack
def knapsack01(weights, values, capacity):
    if len(weights) != len(values) or capacity < 0 or any(w <= 0 for w in weights):
        raise ValueError("matching arrays, positive weights, nonnegative capacity")
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1):
            dp[c] = max(dp[c], dp[c - weight] + value)
    return dp[capacity]

# alg.sequence
def lis_length(nums):
    tails = []
    for x in nums:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

def lcs_length(a, b):
    if len(b) > len(a):
        a, b = b, a
    dp = [0] * (len(b) + 1)
    for x in a:
        diagonal = 0
        for j, y in enumerate(b, 1):
            old = dp[j]
            dp[j] = diagonal + 1 if x == y else max(dp[j], dp[j - 1])
            diagonal = old
    return dp[-1]

# alg.greedy
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

# alg.intervals
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

# alg.bits
def single_number(nums):
    if not nums:
        raise ValueError("nonempty paired input required")
    result = 0
    for x in nums:
        result ^= x
    return result
