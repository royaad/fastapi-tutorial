import asyncio
import time


async def task_1():
    print("Start Task 1")
    await asyncio.sleep(3)
    print("End Task 1")
    return "Task 1 Ready"


async def task_2():
    print("Start Task 2")
    await asyncio.sleep(2)
    print("End Task 2")
    return "Task 2 Ready"


async def main():
    # Approach 1
    start_time = time.perf_counter()
    batch = asyncio.gather(task_1(), task_2())
    result_1, result_2 = await batch
    duration = time.perf_counter() - start_time
    print(result_1, result_2, duration)
    # Approach 2
    start_time = time.perf_counter()
    async_task_1 = asyncio.create_task(task_1())
    async_task_2 = asyncio.create_task(task_2())
    result_1 = await async_task_1
    result_2 = await async_task_2
    duration = time.perf_counter() - start_time
    print(result_1, result_2, duration)


asyncio.run(main())
# 3.01 s
# 3.00 s
