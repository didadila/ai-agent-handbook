# 01 Python 基础：任务状态先别写错

本章六点是后续并发、数据库与工具调用的语言地基。目标 Python >= 3.11；代码均为**未执行的教学示例**，不是配套 demo 的源码，也不代表实测结果。案例是构造故障，不是线上统计。[官方证据与版本边界](../../skills/knowledge-interviewer/references/domains/python-backend/sources.md)由独立来源文件维护。

## py.lang.objects — 赋值与浅拷贝不能隔离任务的嵌套状态

**结论**：Python 变量绑定对象；给另一个名字赋值不会复制任务。隔离边界必须落在可变对象上，而不只是顶层容器。

**案例**：提交检索任务时复制默认配置，随后增加一个租户的过滤条件，其他租户也受影响。

```python
base = {"filters": [], "limit": 5}
a = base.copy()
b = base.copy()
a["filters"].append("tenant-a")
assert b["filters"] == ["tenant-a"]  # 浅拷贝仍共享内层列表
```

**机制**：`dict.copy()` 新建字典，但值仍引用原列表；`is` 判断身份，`==` 判断值。对边界明确的小结构，可每次构造新列表或用不可变元组；`deepcopy` 会递归复制，却不适合复制数据库连接、锁和其他资源句柄。`dataclass(frozen=True)` 禁止字段重新赋值，不会冻结字段里的列表。

**取舍边界**：共享只读配置减少复制成本；请求、任务与租户可变状态不能借此共享。即使单线程，顺序请求也能污染共享对象，不必等到并发才出错。

**误解靶子**：“加了类型注解或 frozen 就线程安全。”它们并未消除内部可变对象，更没定义写入所有权。

**判据**：修改任务 A 的嵌套过滤器后，任务 B 与默认配置是否保持不变？测试必须覆盖嵌套层，而不是只比较两个字典的 `id`。

**自测**：若要让默认过滤条件只读、每个任务还能追加自己的条件，你会采用什么数据结构与构造边界，为什么不直接对整个任务 `deepcopy`？

## py.lang.collections — 用集合表达不变量，用迭代器控制检索内存

**结论**：容器选择同时决定顺序、去重和内存上界；“能装进去”不是检索任务的数据设计。

**案例**：worker 对大文档的所有 chunk 先 `list()`，再一次性提交任务；内存随文档长度增长。与此同时，用 `set` 去重引用打乱了原本按相关性排序的结果。

```python
def unique_in_order(ids):
    seen = set()
    for doc_id in ids:
        if doc_id not in seen:
            seen.add(doc_id)
            yield doc_id
```

**机制**：生成器按需推进，`seen` 仍随不同 ID 数量增长；流式产出不等于恒定内存。字典保留插入顺序，集合不提供业务排序契约；列表适合有序结果，`deque` 适合两端队列。迭代器通常只能消费一次，日志先遍历生成器可能让实际 worker 读到空数据。

**取舍边界**：对小结果集先 materialize 可以简化重复访问；对大文档需分批、限制批大小及去重窗口。生成器如果持有文件或连接，必须把关闭责任交给明确的作用域，不能靠“惰性”逃避资源管理。

**误解靶子**：“换成 generator 就不会爆内存。”下游 `list()`、无限 `seen` 或无限任务创建会重新引入无界增长。

**判据**：输入 chunk 数翻倍时，内存增长来自哪里？排序是否在去重后仍被保留？代码有没有重复消费同一迭代器？

**自测**：检索返回按分数排序的 100 条引用，其中有重复文档；如何保留首个位置去重，并说明哪部分内存仍不是常数？

## py.lang.functions — 默认参数与闭包会把跨请求状态偷偷留下

**结论**：默认参数在函数定义时求值，闭包读取捕获的绑定；任务工厂应显式传入依赖与状态。

**案例**：`def submit(query, tags=[])` 每次追加租户标签，后续请求继承旧标签；循环中构造三个回调，都查询最后一个任务 ID。

```python
def build_task(query: str, tags=None):
    return {"query": query, "tags": list(tags) if tags is not None else []}

def make_reader(task_id, read):
    def fetch():
        return read(task_id)
    return fetch
```

**机制**：默认列表只有一份；函数调用不会自动重新求值默认表达式。循环闭包若引用同一个循环变量，执行时读到的是它当前的值；工厂函数给每次调用创建独立绑定。把 clock、检索器、授权查询传入函数，能用确定性 stub 构造超时、租约过期与权限撤销场景，而不是在测试里修改全局对象。

**取舍边界**：纯函数便于测试，但 I/O 必须有明确的适配器边界；不要把真实副作用藏进装饰器。依赖注入不要求引入容器框架，普通参数通常够用。

**误解靶子**：“默认参数只在调用时才创建。”“lambda 很短，所以不会保留状态。”二者都忽略绑定的生命周期。

**判据**：两次 `build_task` 的列表是否相互独立？测试能否在不联网、不改全局设置的情况下替换检索器与时间？

**自测**：为五个任务构造延迟执行的查询回调时，怎样避免它们全读最后一个 ID，并让测试控制查询失败？

## py.lang.types — 注解帮助静态推理，边界校验才挡住非法请求

**结论**：`str` 注解不会在运行时拒绝整数；入口校验、业务不变量与当前授权是三道不同的门。

**案例**：Python 函数标注 `limit: int`，直接被调用时仍收到 `"很多"`；另一个请求提供合法 `tenant` 字符串，却试图读取别人的任务。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Query:
    text: str
    limit: int

    def __post_init__(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("query must be non-empty")
        if type(self.limit) is not int or not 1 <= self.limit <= 20:
            raise ValueError("limit out of range")
```

**机制**：类型检查器分析代码，但不会替代运行时校验。上例显式排除 `bool`（它是 `int` 的子类）。生产可用 Pydantic 定义 schema；根据接口契约选择严格模式、长度与额外字段策略，避免不知情的类型转换。校验后仍需从认证主体推导租户，检查任务所有权；客户端传来的 tenant 不能成为授权来源。

**取舍边界**：内部已验证对象不必层层重复解析；不可信 HTTP、队列消息、checkpoint 恢复、模型 tool 参数都要校验。SQLAlchemy 模型解决持久化映射，不等于 HTTP schema，更不等于权限策略。

**误解靶子**：“Pydantic 通过就是安全。”合法 URL 仍可能指向内网，合法 task ID 仍可能越权。

**判据**：空查询、超大 limit、未知字段与跨租户读取是否有各自可断言的拒绝路径？是否记录拒绝原因但不泄露敏感输入？

**自测**：一个类型合法的 tool 参数包含别人的 task ID；schema、业务校验与授权分别应该检查什么？

## py.lang.resources — 资源释放需要作用域，事务退出不等于连接关闭

**结论**：文件、数据库连接与网络客户端要有明确所有者；垃圾回收时机不能承担服务释放承诺。

**案例**：CLI 连续执行多个任务，开发者以为 `with sqlite3.connect(...)` 退出会关闭连接，实际只处理提交或回滚，文件句柄生命周期并未因此结束。

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect("tasks.db")) as conn:
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS audit (message TEXT)")
        conn.execute("INSERT INTO audit VALUES (?)", ("submitted",))
```

**机制**：外层 `closing` 调用 `close()`；内层连接上下文管理事务，异常触发回滚，正常退出按连接事务设置提交。事务具体开始时机还受驱动与配置影响，不要把 `with conn` 理解成所有 SQL 自动开启同一种事务。异步资源使用 `async with`，清理放 `finally`，取消时依然要等待资源退出。Python >= 3.11 的 `TaskGroup` 负责子任务作用域，不会替你关闭所有客户端。

**取舍边界**：连接池可以在应用生命周期内复用，session/事务通常按请求或任务独立；关闭 session 与销毁整个连接池是不同操作。SQLite demo 使用显式短事务，只是本地教学，不模拟 PostgreSQL 多写能力。

**误解靶子**：“CPython 引用计数很快，所以靠析构就行。”引用环、异常路径和其他 Python 实现都会改变释放时机。

**判据**：成功、异常、取消三条退出路径里，谁回滚、谁关闭、谁等待子任务结束？能否画出资源的唯一所有者？

**自测**：worker 在写审计记录时抛错，如何保证回滚与连接关闭都发生，为什么只有 `with conn` 还不够？

## py.lang.environment — 可复现解释器与测试入口比“本机能跑”更可靠

**结论**：记录 Python 版本、解释器路径和依赖边界；先运行标准库验证，再按需求安装生产组件。

**案例**：编辑器使用虚拟环境，终端 `pip` 却装进另一解释器；部署机器低于 3.11，启动时找不到 `asyncio.TaskGroup`。

```bash
# 示例命令，未在正文中执行；从仓库根目录运行
python3 --version
python3 -c 'import sys; print(sys.executable)'
python3 -m unittest discover -s handbook/python-backend/examples -p 'test_*.py'
```

**机制**：`python -m ...` 把模块操作绑定到该解释器。独立虚拟环境隔离项目依赖，但不隔离操作系统、系统库和数据库版本。生产建议 FastAPI + Pydantic + SQLAlchemy + PostgreSQL；这是分工组合，不是本册要求的安装清单。依赖用项目锁定机制与 CI 核验兼容，不硬编码“最新版本”。标准库 SQLite CLI 不需要 Redis、Celery、S3 或真实模型凭证。

**取舍边界**：学习阶段只要求 Python >= 3.11；目标 CPython 是否启用 GIL、扩展是否释放 GIL、进程启动方式都要按实际构建检查。不要把某台机器的线程吞吐结论推广到所有 Python。测试发现 0 项不是通过验收：先确认示例测试文件已交付、路径正确，再查看实际数量和退出码。

**误解靶子**：“升级到最新依赖能解决所有问题。”“unittest 命令退出 0 就证明功能完整。”环境漂移与空测试集都能制造假安全感。

**判据**：干净环境能否按同一入口运行非零测试集？失败是否能区分导入错误、行为断言失败与外部服务缺失？

**自测**：CI 显示 `Ran 0 tests` 且成功，你应先查哪三件事，为什么不能把它记作任务服务已验证？
