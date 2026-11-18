# 02 异步与并发：谁等待，谁停止，谁限制数量

本章围绕检索 I/O 与 worker 的生命周期。代码为**未执行教学示例**；不表示 CLI 已实现异步 HTTP 或生产调度。[官方证据](../../skills/knowledge-interviewer/references/domains/python-backend/sources.md)

## py.async.eventloop — 协程只有让出控制权，事件循环才能服务其他任务

**结论**：`async def` 不会把函数体自动变成非阻塞；同步阻塞调用仍会卡住该事件循环线程。

**案例**：检索 endpoint 里用 `time.sleep(2)` 模拟下游延迟，同一个 worker 上连健康检查也等两秒。将其替换为 `await asyncio.sleep(2)` 才能让其他任务获得调度机会。

```python
import asyncio

def legacy_read():
    # 教学替身：代表一个阻塞 I/O 调用
    import time
    time.sleep(0.1)
    return "document"

async def retrieve():
    return await asyncio.to_thread(legacy_read)
```

**机制**：事件循环在挂起点调度协程；协程创建后要被 `await` 或调度才执行。`to_thread` 可把阻塞 I/O 移到线程，不会把所有 CPU 工作变快。优先使用与事件循环兼容的异步客户端，并确认其内部不调用长时间阻塞函数。`await` 也不保证每次都挂起：立即可用的结果可能直接继续执行。

**取舍边界**：短小的纯 Python 计算可以直接执行，重 CPU 解析要隔离到有界 executor 或独立 worker。多进程 HTTP worker 能隔离一部分阻塞，但不能弥补每个进程内部的循环阻塞；内存、连接池也随进程复制。

**误解靶子**：“所有函数改成 async 就并发了。”没有可挂起的 I/O 与数量控制，只是换了声明。

**判据**：模拟检索变慢时，同 worker 上无关请求的延迟是否也上涨？代码能否指出每个同步 I/O 的执行位置？

**自测**：一次请求既读阻塞文件又做五秒纯 Python 排序，分别适合放在哪里，为什么都写成 `await to_thread(...)` 未必最好？

## py.async.cancellation — 用 TaskGroup 和 timeout 给子任务一个可退出的家

**结论**：Python >= 3.11 用 `TaskGroup` 管子任务、`timeout` 管期限；取消是协作信号，不是强制撤销外部效果。

**案例**：同时检索两路来源，一路失败，另一路却继续占连接；endpoint 已返回错误，孤儿任务还在写结果。结构化作用域让失败、等待和清理回到调用者。

```python
import asyncio

async def retrieve_pair(fetch):
    try:
        async with asyncio.timeout(2):
            async with asyncio.TaskGroup() as group:
                left = group.create_task(fetch("left"))
                right = group.create_task(fetch("right"))
        return left.result(), right.result()
    except TimeoutError:
        return {"status": "dependency_timeout"}
```

**机制**：`TaskGroup` 等待其子任务结束；通常一个子任务发生非取消异常会取消同组其他任务，并在退出时汇总异常（可能为 `ExceptionGroup`）。`timeout` 对当前任务施加期限，所触发的取消在作用域外转换为 `TimeoutError`。协程应在 `finally` 清理；如果显式捕获 `CancelledError`，通常必须重新抛出，不要吞掉结构化并发的控制信号。

**取舍边界**：期限只约束能响应取消的协作路径；同步阻塞、线程中的函数或已发送的远端请求可能继续运行。`shield` 只改变取消传播，不能让任务耐久、无限延长服务生命周期或替代幂等。HTTP 客户端还要设置连接/读取超时，并在父预算内分配重试时间。

**误解靶子**：“超时就是没执行。”“cancel 成功就回滚了远端写入。”未知结果需查询、幂等或对账。

**判据**：超时后子任务是否被等待、连接是否释放？代码有没有取消后仍能不受保护地提交任务终态的路径？

**自测**：一路检索失败、另一路正在远端写审计事件时，TaskGroup 能保证什么，不能保证什么？

## py.async.backpressure — 限并发之外，还要限制等待队列与入口

**结论**：并发上限限制正在做的工作；背压还要限制排队数、等待时间与单项大小。

**案例**：对十万个 chunk 各自 `create_task`，每个内部使用 `Semaphore(8)`。正在执行的只有八个，但等待的任务对象与输入仍占满内存。

```python
import asyncio

async def consume(queue, process):
    while True:
        item = await queue.get()
        try:
            if item is None:
                return
            await process(item)
        finally:
            queue.task_done()

# 设计片段：queue = asyncio.Queue(maxsize=32)
# 固定数量 consumer，由 TaskGroup 拥有；生产者逐项 await queue.put(item)
# 每个 consumer 一个结束标记；失败时由父作用域取消生产者和其他 consumer。
```

**机制**：有界队列满时 `put` 挂起，将压力传回生产者；固定 worker 数限制任务对象数量。`queue.join()` 只等待 `task_done()` 计数归零，不会代替错误传播与子任务收尾。HTTP 入口需设置请求体上限、租户配额、入队等待期限，容量不足时按契约返回拒绝/稍后重试，而不是无限接收。

**取舍边界**：内存队列仅适合同进程短生命周期流水线；跨 worker 与重启恢复依赖持久任务存储或 broker。大条目可能让有界条数仍消耗大量字节，须限制内容大小。扩大队列会增加排队延迟，不能增加下游服务能力。

**误解靶子**：“信号量就是完整背压。”“队列越大越抗压。”它们可能把过载伪装成超长等待。

**判据**：能否列出活跃数、排队数、单项字节数和等待期限四个上限？过载是否有明确外部响应与监控信号？

**自测**：八个 worker 平均每项一秒，突然来一万项；只加大队列会改变吞吐还是等待时间，你会在哪一层拒绝新任务？

## py.async.execution — 按目标构建与工作类型选择协程、线程或进程

**结论**：执行模型由 I/O、CPU、隔离要求决定；GIL 是目标 CPython 构建的边界，不是所有 Python 的普遍定律。

**案例**：纯 Python chunk 分词被放进十六线程，延迟没有按线程数下降；另一个 native 扩展释放 GIL 的任务却可能在线程上获益。二者不能用同一个口号解释。

**机制**：在启用 GIL 的 CPython 中，同一进程通常不能让多个线程同时执行 Python 字节码；I/O 与部分扩展可释放 GIL。另有自由线程构建及其他 Python 实现，必须核实目标环境；即使无 GIL，也需保护共享不变量。进程可并行执行 CPU 任务，但引入序列化、IPC、启动与内存成本，传参应是可序列化数据，而不是 session、连接或活动事件循环。

**取舍边界**：协程适合大量等待且依赖支持异步的路径；线程适合阻塞 I/O 或经测量适配的扩展；进程/独立 worker 适合 CPU 与故障隔离。executor 必须有容量预算。取消等待 `to_thread` 的协程不会强制终止底层线程；进程中的外部效果同样需要幂等。

**误解靶子**：“Python 永远不能并行。”“有 GIL 所以共享字典更新天然安全。”即使单个操作表现为原子，多步检查再写也不是业务原子操作。

**判据**：部署构建、热点工作类别、并发上限、跨进程序列化对象与取消后遗留执行是否都有记录？性能结论是否来自目标环境测量，而非本文示例？

**自测**：服务要做阻塞 SDK 下载、纯 Python 大段解析和异步数据库查询，如何分配执行位置，并控制取消后仍继续下载的成本？
