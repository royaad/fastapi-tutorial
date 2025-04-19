import asyncio
import math
import threading
import time
from concurrent.futures import Executor, ProcessPoolExecutor
from contextvars import copy_context
from functools import partial
from typing import Callable, Optional, ParamSpec, TypeVar


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


# inspired by the langchain code
# https://api.python.langchain.com/en/latest/_modules/langchain_core/runnables/config.html#run_in_executor

P = ParamSpec("P")
T = TypeVar("T")


def _executor_wrapper(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    try:
        return func(*args, **kwargs)
    except StopIteration as exc:
        raise RuntimeError from exc


async def run_in_executor(
    executor: Optional[Executor],
    func: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    if executor is None:
        return await asyncio.get_running_loop().run_in_executor(
            None,
            partial(copy_context().run, _executor_wrapper, func, *args, **kwargs),
        )
    return await asyncio.get_running_loop().run_in_executor(
        executor,
        partial(_executor_wrapper, func, *args, **kwargs),
    )


async def main():
    # Approach 1
    start_time = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        batch = await asyncio.gather(
            task_1(),
            run_in_executor(executor, factorial, 10_000_000),
            run_in_executor(executor, is_prime, 999_999_999_999_989),
            return_exceptions=True,
        )
    result_1, result_2, result_3 = batch
    duration = time.perf_counter() - start_time
    print(
        result_1, result_2, result_3, f"Total Tasks Duration: {duration:.3f}s", sep="\n"
    )


if __name__ == "__main__":
    asyncio.run(main())
# Starting Task 1 in MainThread
# Starting Task 2 in asyncio_0
# Task 2 Ending after 2.000s
# Task 1 Ending after 3.019s
# Task 1 Ready
# Task 2 Ready
# Total Tasks Duration: 3.020s
