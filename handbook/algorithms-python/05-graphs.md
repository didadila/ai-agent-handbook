# 5. 图与依赖

Python 3.11+。例子为原创教学实现，函数及测试见[algorithms.py](examples/algorithms.py)和[test_algorithms.py](examples/test_algorithms.py)。它们不是平台提交记录；本章的构造输入不是用户错题。使用deque、heapq、bisect等标准库的导入在实现模块顶部统一列出；节点类型也在那里定义。

## alg.graph — 图的 BFS/DFS 与最短步数

**入门简介。** 图用点和边表示关系；BFS（广度优先搜索）先处理距离起点一步的点，再处理更远层。

**生活比喻与边界。** 像消息沿朋友圈一轮轮转发；只有每条边代价相同，轮数才能表示最短代价。

**结论与机制。** 先区分有向/无向、带权/无权、是否连通，再选邻接表。BFS按层首次到达给出无权最短边数；DFS适合可达性、连通块与回溯，不保证首先找到最短路。无向图两端都登记；不连通图全遍历需每个未访问顶点启动。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 入队时标记，避免多个前驱重复入队。邻接表时间O(V+E)，空间O(V)加存图；稠密矩阵遍历另计O(V²)。这里只接受邻接顶点为合法下标的列表。 |
| 构造反例 | 两条不同权重边不能仅按经过边数判断更短。 |
| 掌握判据 | 讲清层次单调、不把visited的图搜索规则套到允许不同路径重访的回溯。 |

**Python实现。** `bfs_distances`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
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
```

**手推与自测。** 只判断BFS首次到达为何能代表无权最短边数。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.topo — 拓扑排序与依赖环

**入门简介。** 拓扑排序给有先后依赖的任务排合法顺序；有循环依赖时排不出全部任务。

**生活比喻与边界。** 像先洗菜再炒菜；这是依赖先后，不包含炉灶数量和最短完工时间。

**结论与机制。** Kahn算法把入度为0的顶点加入队列，删除其出边后释放新就绪节点。输出数量小于顶点数说明有向图存在环；拓扑序不一定唯一。本地函数edges中的(u,v)直接表示u→v，即先u后v；力扣课程表的prerequisites条目[a,b]则表示b→a，需要先转换为(b,a)，不能原样混用。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 只有DAG有拓扑序；无向环检测不能直接用这套入度规则。O(V+E)时间空间（含图），返回None与空图合法的[]区分。课程完成顺序不等于资源受限下的最短总工期。 |
| 构造反例 | a依赖b且b依赖a时没有任何合法课程开始顺序。 |
| 掌握判据 | 说明就绪集合含义与完成计数，不把任意DFS访问顺序当拓扑序。 |

**Python实现。** `topological_order`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
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
```

**手推与自测。** 只判断0→1→0是否存在拓扑序。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.union — 并查集与连通性

**入门简介。** 并查集维护哪些元素属于同一个集合，支持查代表和合并集合。

**生活比喻与边界。** 像把班级小组名单合并；能知道同组不等于保存了成员间的具体路线。

**结论与机制。** 用代表元描述等价类，路径压缩让后续查找更短，按大小/秩合并控制树高。判断无向边是否把同一连通块再连起来可检测冗余边。代表元的编号不是业务语义，不能依赖它是最小节点。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 压缩与按大小合并共同给出均摊近常数O(α(n))，不是每次最坏O(1)。普通并查集不支持高效删边，也不解决有向可达与最短路。 |
| 构造反例 | 单向有边a→b并不代表b可达a，不能当无向等价关系。 |
| 掌握判据 | 能区分连通关系与路径本身，重复union不减少连通块数。 |

**Python实现。** `DSU`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
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
```

**手推与自测。** 只说明普通并查集为何不直接解决有向可达。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。

## alg.shortest — 最短路与非负权条件

**入门简介。** 最短路比较多条路径的总代价；Dijkstra每次优先处理当前距离最小的候选状态。

**生活比喻与边界。** 像比较不同路线的累计车费；本例要求每段费用非负，不能把返款负费用直接套进证明。

**结论与机制。** Dijkstra把当前最小距离的有效状态弹出，才可利用非负边权证明该距离已确定。松弛只在发现更短路径时入堆；堆内旧距离必须跳过。BFS用于等权，0-1 BFS用于0/1权，含负边要考虑Bellman-Ford等其他方法。

| 判断维度 | 要点 |
|---|---|
| 适用与代价 | 例子采用惰性堆，最多O(E)堆项，时间O((V+E) log(E+2))、辅助空间O(V+E)（不含输入图）。不能说这个实现堆空间始终O(V)。不可达用inf；输入为非负整数权。 |
| 构造反例 | 0→1权10，0→2权1，2→1权1，首次发现1的距离10不是最终最短路。 |
| 掌握判据 | 区分发现与确定、旧堆项与当前最优，说明负权破坏证明。 |

**Python实现。** `dijkstra`的完整函数如下；输入契约在上述机制中限定，不把这个模板套到未满足前提的题上。

```python
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
```

**手推与自测。** 只写出该图从0到1的最短距离。 先手推变量/状态，再用不同边界输入验证；能得到输出还不够，需要解释为何排除候选不漏解。陪练首题与追问见[对应题库](../../skills/knowledge-interviewer/references/domains/algorithms-python/questions.md)。本点的最小验证与A档判据由陪练分开使用，不一次性展示答案。
