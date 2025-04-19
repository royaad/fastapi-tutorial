import asyncio
import threading
import time


async def task_1():
    print(f"Starting Task 1 in {threading.current_thread().name}")
    start = time.perf_counter()
    await asyncio.sleep(3)  # Simulates I/O-bound operation
    print(f"Task 1 Ending after {time.perf_counter() - start:.3f}s")
    return "Task 1 Ready"


def task_2():
    print(f"Starting Task 2 in {threading.current_thread().name}")
    start = time.perf_counter()
    time.sleep(2)  # Simulates I/O-bound file read/write or computation
    print(f"Task 2 Ending after {time.perf_counter() - start:.3f}s")
    return "Task 2 Ready"


async def main():
    # Approach 1
    start_time = time.perf_counter()
    batch = asyncio.gather(task_1(), asyncio.to_thread(task_2), return_exceptions=True)
    result_1, result_2 = await batch
    duration = time.perf_counter() - start_time
    print(result_1, result_2, f"Total Tasks Duration: {duration:.3f}s", sep="\n")


asyncio.run(main())
# Starting Task 1 in MainThread
# Starting Task 2 in asyncio_0
# Task 2 Ending after 2.000s
# Task 1 Ending after 3.005s
# Task 1 Ready
# Task 2 Ready
# Total Tasks Duration: 3.006s
