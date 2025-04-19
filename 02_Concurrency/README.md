# Concurrency in Python and FastAPI

In previous sections, we briefly mentioned that FastAPI can handle both synchronous and asynchronous functions. However, choosing between the two is not arbitrary—there are best practices for when to use each.

Before diving back into FastAPI, this section aims to clarify **when to use synchronous vs asynchronous functions** by stepping back and exploring the broader concepts of **concurrency** and **parallelism** in Python. Understanding these concepts will help you build performant applications and better manage latency in your software.

## What Is an Asynchronous Function?

When a function is called **synchronously**, each step in its execution must complete before the next step begins. In contrast, **asynchronous functions** allow certain operations to be executed **concurrently**, enabling more efficient use of system resources, especially during I/O-bound tasks.

To fully understand asynchronous programming, we must first differentiate between **concurrency** and **parallelism**.

## Concurrency vs. Parallelism

These terms are often used interchangeably, but they refer to fundamentally different concepts:

-   **Parallelism** involves executing multiple tasks **at the same time**, typically by leveraging **multiple CPU cores**. It is ideal for **CPU-bound** tasks—those that require intense computation and can run independently.
-   **Concurrency**, on the other hand, involves **interleaving the execution** of multiple tasks to give the appearance that they are happening simultaneously. It is well-suited for **I/O-bound** operations where the CPU would otherwise remain idle.

> **Rule of thumb:**
>
> -   Use **parallelism** (e.g., `multiprocessing`) for CPU-intensive tasks like data processing and numerical computations.
> -   Use **concurrency** (e.g., `asyncio` or `threading`) for I/O-bound tasks such as file handling or network communication.

## Concurrency and Parallelism in Python

Python provides several tools for implementing both concurrency and parallelism:

-   **`asyncio`** – Asynchronous I/O using a single-threaded, event-driven model
-   **`threading`** – OS-level threads for concurrent execution
-   **`multiprocessing`** – True parallelism using separate processes and CPU cores

The following table outlines the key characteristics of each approach:

| Feature        | `asyncio`                                                        | `threading`                                          | `multiprocessing`                               |
| -------------- | ---------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------- |
| Achieves       | Concurrency                                                      | Concurrency                                          | Parallelism                                     |
| Model          | Single-threaded, cooperative multitasking                        | Multi-threaded, preemptive multitasking (OS-managed) | Multi-process, separate memory space            |
| Task Switching | Controlled by event loop (cooperative)                           | Managed by OS (preemptive)                           | Each process runs independently                 |
| CPU Core Usage | Single core                                                      | Single core                                          | Multiple cores                                  |
| Overhead       | Minimal; requires `async/await` syntax                           | Higher memory usage; risk of race conditions         | Higher overhead; independent memory per process |
| Ideal Use Case | High-latency I/O, many simultaneous connections (e.g., web APIs) | Low-latency I/O, moderate concurrency                | CPU-intensive tasks                             |

### Choosing the Right Model

Selecting the appropriate model depends on the nature of the workload:

-   **CPU-bound tasks**  
     For computationally intensive operations (e.g., data analysis, cryptographic processing), use **`multiprocessing`**, which distributes work across multiple CPU cores for optimal performance.
-   **I/O-bound tasks with low latency and limited concurrency**  
     For lightweight I/O operations (e.g., file reads/writes, basic socket communication), **`threading`** provides a simple concurrency model that’s easy to implement.
-   **I/O-bound tasks with high latency and large-scale concurrency**  
     For large numbers of concurrent I/O operations (e.g., serving thousands of HTTP requests), **`asyncio`** is the most scalable and resource-efficient solution.

> [!NOTE] **Guiding Principle**
>
> -   Use **`multiprocessing`** when your workload is CPU-bound and benefits from parallel execution.
> -   Use **`threading`** for straightforward, moderately concurrent I/O-bound tasks.
> -   Use **`asyncio`** when you need to handle many concurrent I/O tasks with minimal resource usage.

### Benchmark Comparison

To further illustrate the performance differences, two functions were created:

-   `fetch_url` — an **I/O-bound** task simulating network latency
-   `factorial` — a **CPU-bound** task involving heavy computation

Each function was executed using different execution models. Source code is available in the `src` directory under files with the `00_` prefix. The table below summarizes the observed execution times (in seconds):

| Function    | Sequential Run (Baseline) | `asyncio`  | `threading` | `multiprocessing` |
| ----------- | :-----------------------: | :--------: | :---------: | :---------------: |
| `fetch_url` |        **96.931**         | **2.314**  | **20.092**  |    **23.363**     |
| `factorial` |        **16.942**         | **16.107** | **16.432**  |     **5.629**     |

These results support our conclusions:

-   `asyncio` drastically reduces latency for **I/O-bound** tasks.
-   `multiprocessing` significantly improves performance for **CPU-bound** workloads.

### Why This Matters for FastAPI

Modern applications increasingly adopt **microservices architectures** and demand highly concurrent systems to deliver responsive user experiences. As a result, **asynchronous programming** and **non-blocking I/O** have become essential for building scalable APIs with low latency.

In the sections that follow, we will focus on **`asyncio`**, which underpins ASGI servers like **Uvicorn**, and is a core feature of **FastAPI**. Understanding how and when to use asynchronous functions will help you fully leverage FastAPI’s performance capabilities.

## Asyncio

### The `asyncio` Event Loop Works

The `asyncio` event loop is the core of Python's asynchronous programming model. It orchestrates the execution of multiple asynchronous tasks within a single thread, enabling efficient handling of I/O-bound operations without resorting to multithreading.

#### High-Level Overview

At its essence, the event loop functions as follow:

1. **Initialization** The event loop is created and started, preparing to manage asynchronous task.
2. **Task Scheduling** Asynchronous tasks (coroutines) are scheduled for execution.
3. **Execution Cycle**:

    - **Run Tasks** The loop runs each task until it encounters an `await` expression, indicating a pause for an I/O operation or a delay.
    - **Handle I/O** While tasks are awaiting, the loop monitors I/O events and timer.
    - **Resume Tasks** Once the awaited operation completes, the loop resumes the corresponding task.

4. **Completion** This cycle continues until all tasks are completed, after which the event loop stop.

![Asyncio Event Loop](https://miro.medium.com/v2/resize:fit:4800/format:webp/0*g7DPAlp9eWv-6QNH.png)

#### Further Reading

-   [Python's asyncio Event Loop Documentation](https://docs.python.org/3/library/asyncio-eventloop.html)
-   [Build Your Own Event Loop from Scratch in Python](https://python.plainenglish.io/build-your-own-event-loop-from-scratch-in-python-da77ef1e3c39)

### The `async` and `await` Syntax

#### Coroutine Definition

Prefixing a function with `async def` defines it as a **coroutine**, not a regular function. When called, it **does not execute immediately**—instead, it returns a **coroutine object**, which must be scheduled and awaited using an event loop.

A coroutine is not intended to be invoked like a normal function:

```python
coro = my_coroutine()  # Returns a coroutine object, doesn't execute
```

To actually execute the coroutine, it must be **awaited**:

```python
await my_coroutine()
```

or run inside the event loop using `asyncio.run()` or `asyncio.create_task()`.

> [!IMPORTANT]
> A coroutine should contain at least one `await` expression. If a coroutine does not `await` anything, it will still return a coroutine object when called, but a `RuntimeWarning` may be raised during execution because the coroutine was never awaited or awaited without suspension—meaning it didn’t yield control to the event loop, defeating the purpose of being asynchronous.

This ensures that the coroutine participates in cooperative multitasking managed by the event loop.

#### Example: Concurrent Execution with `asyncio.gather()`

The following example defines two I/O-bound coroutines and executes them concurrently using `asyncio.gather()` (other examples with `asyncio.create_task()` and `asyncio.get_event_loop()` can be found in [[01_asyncio_dummy_example.py|AsyncIO Dummy Example]] ):

```python
import asyncio
import threading
import time

async def task_1():
    print(f"Starting Task 1 in {threading.current_thread().name}")
    start = time.perf_counter()
    await asyncio.sleep(3)  # Simulates I/O-bound operation
    print(f"Task 1 Ending after {time.perf_counter() - start}s")
    return "Task 1 Ready"

async def task_2():
    print(f"Starting Task 2 in {threading.current_thread().name}")
    start = time.perf_counter()
    await asyncio.sleep(2)  # Simulates I/O-bound operation
    print(f"Task 2 Ending after {time.perf_counter() - start}s")
    return "Task 2 Ready"

async def main():
    start_time = time.perf_counter()
    batch = asyncio.gather(task_1(), task_2())  # Schedule both tasks concurrently
    result_1, result_2 = await batch             # Await completion of all tasks
    duration = time.perf_counter() - start_time
    print(result_1, result_2, f"Total Tasks Duration: {duration}")

asyncio.run(main())
```

#### Sample Output

```plaintext
Starting Task 1 in MainThread
Starting Task 2 in MainThread
Task 2 Ending after 2.002s
Task 1 Ending after 3.005s
Task 1 Ready Task 2 Ready Total Tasks Duration: 3.006s
```

#### Technical Summary

-   `task_1()` and `task_2()` are both asynchronous coroutines.
-   `asyncio.sleep()` is a non-blocking sleep that suspends execution of the coroutine and yields control to the event loop.
-   `asyncio.gather()` schedules multiple coroutines to run concurrently and waits for all of them to complete.
-   The output demonstrates that tasks are executed concurrently: although `task_1` sleeps for 3 seconds and `task_2` for 2 seconds, the total execution time is ~3 seconds—not 5.

This illustrates the power of `async`/`await` in optimizing I/O-bound operations: while one task is paused, the event loop can continue executing other tasks, all within a single-threaded, cooperative concurrency model.

### Turning an Synchronous Function into an Asynchronous Routine

#### Basic

#### With ProcessPool

### async modules... httpx, aiohttp, aiosqlite

### build a server for fun? and compare with uvicorn

-   [Video Title 1](https://youtu.be/Ii7x4mpIhIs?si=JZtNMF0tORjjtU1W)
-   [Video Title 2](https://youtu.be/K56nNuBEd0c?si=rhvR-5LQE2DKEclg)
-   [Video Title 3](https://youtu.be/SAueUTQNup8?si=sF1kXLsJgMKcT2i6)
-   [Video Title 4](https://youtu.be/MfCbM6NKPeY?si=0F4fPh6f0J6a8jae)
