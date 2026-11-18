"""对比：同步阻塞调用 vs asyncio.to_thread。

一个协程每 0.5 秒打一次时间戳；另一个协程执行 3 秒同步等待。
版本 A 直接调用，版本 B 丢进线程池。观察时间戳是否被卡住。
"""

import asyncio
import time

START = time.monotonic()


def now() -> float:
    return time.monotonic() - START


async def ticker(label: str, count: int = 7) -> None:
    for i in range(count):
        print(f"[{label}] tick {i}  t={now():.2f}s", flush=True)
        await asyncio.sleep(0.5)


def blocking_call() -> str:
    # 模拟一个只有同步版本的库：占住当前线程 3 秒
    time.sleep(3)
    return "done"


async def blocking_direct() -> None:
    print(f"[A] 开始同步调用 t={now():.2f}s", flush=True)
    result = blocking_call()
    print(f"[A] 同步调用结束 {result} t={now():.2f}s", flush=True)


async def blocking_in_thread() -> None:
    print(f"[B] 开始 to_thread t={now():.2f}s", flush=True)
    result = await asyncio.to_thread(blocking_call)
    print(f"[B] to_thread 结束 {result} t={now():.2f}s", flush=True)


async def demo(label: str, worker) -> None:
    global START
    START = time.monotonic()
    await asyncio.gather(ticker(label), worker())
    print(flush=True)


async def main() -> None:
    print("=== 版本 A：直接调用同步函数（堵住事件循环） ===", flush=True)
    await demo("A", blocking_direct)

    print("=== 版本 B：丢进线程池 asyncio.to_thread ===", flush=True)
    await demo("B", blocking_in_thread)


if __name__ == "__main__":
    asyncio.run(main())
