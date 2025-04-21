import asyncio
import threading
import time


async def task_1():
    print(f"Starting Task 1 in {threading.current_thread().name}")
    start = time.perf_counter()
    await asyncio.sleep(3)  # Simulates I/O-bound operation
    print(f"Task 1 Ending after {time.perf_counter() - start:.3f}s")
    return "Task 1 Ready"


async def task_2():
    print(f"Starting Task 2 in {threading.current_thread().name}")
    start = time.perf_counter()
    await asyncio.sleep(2)  # # Simulates I/O-bound operation
    print(f"Task 2 Ending after {time.perf_counter() - start:.3f}s")
    return "Task 2 Ready"


async def main():
    # Approach 1
    start_time = time.perf_counter()
    batch = asyncio.gather(task_1(), task_2())  # Schedule both tasks concurrently
    result_1, result_2 = await batch  # Await completion of all tasks
    duration = time.perf_counter() - start_time
    print(result_1, result_2, f"Total Tasks Duration: {duration:.3f}s", sep="\n")
    # Approach 2
    start_time = time.perf_counter()
    async_task_1 = asyncio.create_task(task_1())
    async_task_2 = asyncio.create_task(task_2())
    result_1 = await async_task_1
    result_2 = await async_task_2
    duration = time.perf_counter() - start_time
    print(result_1, result_2, f"Total Tasks Duration: {duration:.3f}s", sep="\n")
    # Approach 3
    start_time = time.perf_counter()
    async_task_1 = asyncio.create_task(task_1())
    async_task_2 = asyncio.create_task(task_2())
    done, pending = await asyncio.wait([async_task_1, async_task_2])
    duration = time.perf_counter() - start_time
    print(f"Total Tasks Duration: {duration:.3f}s", sep="\n")
    for task in done:
        print(task.result())


asyncio.run(main())
# Starting Task 1 in MainThread
# Starting Task 2 in MainThread
# Task 2 Ending after 2.014s
# Task 1 Ending after 3.010s
# Task 1 Ready
# Task 2 Ready
# Total Tasks Duration: 3.012s
# Starting Task 1 in MainThread
# Starting Task 2 in MainThread
# Task 2 Ending after 2.004s
# Task 1 Ending after 3.002s
# Task 1 Ready
# Task 2 Ready
# Total Tasks Duration: 3.004s


def _main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        start = time.perf_counter()
        results = loop.run_until_complete(asyncio.gather(task_1(), task_2()))
        duration = time.perf_counter() - start
        result_1, result_2 = results
        print(result_1, result_2, f"Total Tasks Duration: {duration:.3f}s", sep="\n")
    finally:
        loop.close()


# Using loop = asyncio.get_event_loop() will cause an error because
# asyncio.run(main()) starts and runs a new event loop globally, and by the time _main() runs,
# that event loop is still active. asyncio.get_event_loop() then fetches the already-running loop,
# and run_until_complete() can't be used on a loop that’s already running — hence the RuntimeError.
# Another quick fix is to comment the asyncio.run() in order to use asyncio. ().
# NOTE
# Using
# ```
# result_1 = loop.run_until_complete(task_1())
# result_2 = loop.run_until_complete(task_2())
# ```
# will run the tasks sequentially
# The asyncio documentation also mentions:
# "using the get_running_loop() function is preferred to get_event_loop() in coroutines and callbacks."

_main()
# Starting Task 1 in MainThread
# Starting Task 2 in MainThread
# Task 2 Ending after 2.005s
# Task 1 Ending after 3.021s
# Task 1 Ready
# Task 2 Ready
# Total Tasks Duration: 3.023s
