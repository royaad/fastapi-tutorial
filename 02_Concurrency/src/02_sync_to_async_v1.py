import asyncio
import threading
import time
from concurrent.futures import Executor
from contextvars import copy_context
from functools import partial
from typing import Callable, Optional, ParamSpec, TypeVar, cast


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


# inspired by the langchain code
# https://api.python.langchain.com/en/latest/_modules/langchain_core/runnables/config.html#run_in_executor
P = ParamSpec("P")
T = TypeVar("T")


async def run_in_executor(
    executor: Optional[Executor],
    func: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    """Run a function in an executor.

    Args:
        executor: The executor to run in.
        func (Callable[P, Output]): The function.
        *args (Any): The positional arguments to the function.
        **kwargs (Any): The keyword arguments to the function.

    Returns:
        Output: The output of the function.

    Raises:
        RuntimeError: If the function raises a StopIteration.
    """

    def wrapper() -> T:
        try:
            return func(*args, **kwargs)
        except StopIteration as exc:
            # StopIteration can't be set on an asyncio.Future
            # it raises a TypeError and leaves the Future pending forever
            # so we need to convert it to a RuntimeError
            raise RuntimeError from exc

    if executor is None:
        # Use default executor with context copied from current context
        # this chunk of code is similar to asyncio.to_thread()... Therefore, we can simply replace it with
        # return await asyncio.to_thread(func, /, *args, **kwargs))
        return await asyncio.get_running_loop().run_in_executor(
            None,
            cast("Callable[..., T]", partial(copy_context().run, wrapper)),
        )

    return await asyncio.get_running_loop().run_in_executor(executor, wrapper)


async def main():
    # Approach 1
    start_time = time.perf_counter()
    batch = asyncio.gather(
        task_1(), run_in_executor(None, task_2), return_exceptions=True
    )
    result_1, result_2 = await batch
    duration = time.perf_counter() - start_time
    print(result_1, result_2, f"Total Tasks Duration: {duration:.3f}s", sep="\n")


asyncio.run(main())
# Starting Task 1 in MainThread
# Starting Task 2 in asyncio_0
# Task 2 Ending after 2.000s
# Task 1 Ending after 3.019s
# Task 1 Ready
# Task 2 Ready
# Total Tasks Duration: 3.020s
