import asyncio
import math
import threading
import time


async def task_1():
    print(f"Starting Task 1 in {threading.current_thread().name}")
    start = time.perf_counter()
    await asyncio.sleep(3)  # Simulates I/O-bound operation
    print(f"Task 1 Ending after {time.perf_counter() - start:.3f}s")
    return "Task 1 Ready"


def factorial(n):
    # takes around 2 seconds to calculate factorial of 10_000_000
    print(f"Starting factorial in {threading.current_thread().name}")
    start = time.perf_counter()
    result = sum(i * i for i in range(1, n))
    print(f"factorial ending after {time.perf_counter() - start:.3f}s")
    return result


def is_prime(n):
    # takes around 7 seconds to compute if 999_999_999_999_989 is_prime
    print(f"Starting i_prime in {threading.current_thread().name}")
    start = time.perf_counter()
    if n <= 1:
        print(f"is_prime ending after {time.perf_counter() - start:.3f}s")
        return False
    result = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
    print(f"is_prime ending after {time.perf_counter() - start:.3f}s")
    return result


async def main():
    # Approach 1
    start_time = time.perf_counter()
    batch = asyncio.gather(
        task_1(),
        asyncio.to_thread(factorial, 10_000_000),
        asyncio.to_thread(is_prime, 999_999_999_999_989),
        return_exceptions=True,
    )
    result_1, result_2, result_3 = await batch
    duration = time.perf_counter() - start_time
    print(
        result_1, result_2, result_3, f"Total Tasks Duration: {duration:.3f}s", sep="\n"
    )


asyncio.run(main())
# Starting Task 1 in MainThread
# Starting factorial in asyncio_0
# Starting i_prime in asyncio_1
# Task 1 Ending after 3.027s
# factorial ending after 4.038s
# is_prime ending after 9.255s
# Task 1 Ready
# 333333283333335000000
# True
# Total Tasks Duration: 9.344s
