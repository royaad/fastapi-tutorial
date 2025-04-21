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

To actually execute the coroutine, it must run inside the event loop using `asyncio.run()` or by creating an event loop `asyncio.get_event_loop()` and running the tasks in it `loop.run_until_complete()`.

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

#### Example Output

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

### Turning a Synchronous Function into an Asynchronous Routine

#### Basic `to_thread`

In asynchronous applications, it's common to encounter existing synchronous (blocking) functions that you'd like to call without freezing the event loop. Python 3.9+ introduced `asyncio.to_thread()` to make this seamless.

`asyncio.to_thread()` runs a synchronous function in a separate thread without blocking the main event loop, making it ideal for I/O-bound operations or legacy code integration.

The [Python Script](./src/02_sync_to_async_v0.py) offers a minimal example combining an `async def` coroutine with a synchronous function:

```python
# full script in link

async def task_1():
    ...

def task_2():
    ...

async def main():
    result_1, result_2 = await asyncio.gather(
        task_1(),
        asyncio.to_thread(task_2),
        return_exceptions=True
    )
    ...

asyncio.run(main())
```

#### Example Output (I/O-bound to_thread)

```plaintext
Starting Task 1 in MainThread
Starting Task 2 in asyncio_0
Task 2 Ending after 2.000s
Task 1 Ending after 3.005s
Task 1 Ready
Task 2 Ready
Total Tasks Duration: 3.006s
```

#### Key Points

-   `task_1()` is a coroutine that uses `await asyncio.sleep(...)`.
-   `task_2()` is a regular blocking function, made non-blocking via `asyncio.to_thread(...)`.
-   They both run concurrently without blocking each other.
-   This approach is particularly effective for offloading file I/O, slow APIs, or computation that isn't CPU-heavy.

> [!NOTE]
> While `to_thread()` is useful for I/O-bound or short-lived blocking functions, for CPU-intensive work consider using `ProcessPoolExecutor` or libraries like `anyio.to_process`.

### Asyncio and CPU-Bound Work: When `to_thread` Is Not Enough

While `asyncio.to_thread()` is a helpful utility for offloading blocking _I/O-bound_ operations, it doesn't scale well for **CPU-intensive** work.

Let’s take the following [example](./src/02_sync_to_async_v1.py):

```python
# full script in link

async def task_1():
    await asyncio.sleep(3)  # Simulates I/O-bound operation
    return "Task 1 Ready"


def factorial(n):
    ...
    return result


def is_prime(n):
    ...
    return result


async def main():
    start_time = time.perf_counter()
    batch = asyncio.gather(
        task_1(),  # I/O-bound
        asyncio.to_thread(factorial, 10_000_000),  # CPU-bound
        asyncio.to_thread(is_prime, 999_999_999_999_989),  # CPU-bound
        return_exceptions=True,
    )
    result_1, result_2, result_3 = await batch
    duration = time.perf_counter() - start_time
    print(result_1, result_2, result_3, f"Total Tasks Duration: {duration:.3f}s", sep="\n")


asyncio.run(main())
```

#### Example Output (CPU-bound to_thread)

```plaintext
Starting Task 1 in MainThread
Starting factorial in asyncio_0
Starting is_prime in asyncio_1
Task 1 Ending after 3.027s
factorial ending after 4.038s
is_prime ending after 9.255s
Task 1 Ready
333333283333335000000
True
Total Tasks Duration: 9.344s
```

#### What’s the Problem?

In theory:

-   `factorial()` takes about **2 seconds**
-   `is_prime()` takes about **7 seconds**

If they were running **truly in parallel**, the total runtime should be close to **7~8 seconds**, since `factorial` would finish before `is_prime`.

But here, the total runtime is **~9.3 seconds**, which is almost the **sum** of the two CPU tasks. This tells us:

> [!CAUTION]
> The CPU tasks are **not** running in parallel — they're sharing a thread pool and taking turns.

#### Why This Happens

`asyncio.to_thread()` offloads work to a **thread pool**, which is suitable for _I/O-bound_ operations but not for _CPU-bound_ tasks. While it prevents blocking the main event loop, it doesn't bypass Python's **Global Interpreter Lock (GIL)** — meaning only one thread executes Python bytecode at a time.

As a result, CPU-intensive work submitted via `asyncio.to_thread()` still runs **sequentially**, just in background threads instead of the main thread. This limits true parallelism and leads to longer overall runtimes when handling heavy computations.

In short:

-   ✅ Great for blocking I/O (e.g., file reads, network calls)
-   ⚠️ Inefficient for CPU-heavy computation (e.g., math, cryptography)

`asyncio` excels at _I/O concurrency_, but to achieve _parallelism_ for CPU-bound tasks, **multiprocessing** is required — which we’ll cover in the next section.

### True Parallelism with `ProcessPoolExecutor`

In the previous section, we discovered that `asyncio.to_thread()` isn't suitable for CPU-intensive work due to the Global Interpreter Lock (GIL). To fully utilize multiple CPU cores and run heavy computations in parallel, we need **process-based concurrency** — specifically, the `ProcessPoolExecutor`.

#### Mixing `asyncio` with `ProcessPoolExecutor`

To execute synchronous, CPU-bound functions in parallel while still leveraging `asyncio` for I/O-bound concurrency, you can use a helper function like `run_in_executor()`. This utility dispatches blocking work to a **process pool**, enabling true parallelism without blocking the event loop.

The implementation shown in the [Python script](https://chatgpt.com/c/src/02_sync_to_async_v3.py) is inspired by both `asyncio.to_thread()` and LangChain's internal approach to managing executors. It offers flexibility by supporting both `ThreadPoolExecutor` and `ProcessPoolExecutor` as needed, while preserving context and preventing common pitfalls.

This pattern ensures that:

-   **I/O-bound tasks** remain non-blocking thanks to `async/await`
-   **CPU-bound tasks** utilize separate processes for true concurrency
-   **Your event loop stays responsive**, even under heavy compute workloads

#### Example Output (ProcessPoolExecutor)

```plaintext
Starting Task 1 in MainThread
Starting factorial in MainThread
Starting i_prime in MainThread
factorial ending after 2.221s
Task 1 Ending after 3.011s
is_prime ending after 7.447s
Task 1 Ready
333333283333335000000
True
Total Tasks Duration: 7.814s
```

#### Observations

-   Unlike `to_thread()`, both `factorial` and `is_prime` now run **truly in parallel** using separate processes.
-   The total time reflects the runtime of the _longest_ task (`is_prime`), while others overlap efficiently.
-   `task_1()` completes mid-way, showcasing **async + parallel compute** running side by side.

This technique effectively combines the best of both worlds:

-   `asyncio` for non-blocking I/O
-   `ProcessPoolExecutor` for parallel CPU-bound computation

### Simplified Parallelism with `anyio.to_process.run_sync`

While using `ProcessPoolExecutor` gives you control over process-based parallelism, it comes with some boilerplate. If you prefer a **cleaner and more ergonomic API**, `anyio` provides `to_process.run_sync()` — a function that runs synchronous CPU-bound code in a separate **process**, without needing to manage executors yourself. An example can be found in the implementation shown in the [Python script](https://chatgpt.com/c/src/02_sync_to_async_v4.py) .

#### Example Output (anyio.to_process.run_sync)

```plaintext
Starting Task 1 in MainThread
Task 1 Ending after 3.002s
Task 1 Ready
333333283333335000000
True
Total Tasks Duration: 7.560s
```

#### Advantages of `anyio.to_process.run_sync`

-   **Process-based** execution for true CPU-bound parallelism
-   Works seamlessly with `asyncio` (no need to switch to `trio`)
-   No need to manage `ProcessPoolExecutor`
-   Automatically uses context preservation under the hood

> [!NOTE]
>
> -   The `if __name__ == "__main__"` guard is still **mandatory**, even when using `anyio.to_process`, due to multiprocessing behavior on platforms like Windows.
> -   `run_sync` is ideal for **single function calls**. If you need custom executor configuration or batch submission, `ProcessPoolExecutor` might still be a better fit.

### Final Note: Parallelism Here vs. in Production

The parallelism techniques demonstrated so far—using `asyncio.to_thread()`, `ProcessPoolExecutor`, and `anyio.to_process`—are meant to **illustrate how asyncio interacts with synchronous functions**, and how we can combine **I/O-bound and CPU-bound workloads** in the same event loop.

These examples help build an intuitive understanding of:

-   How Python's `asyncio` cooperates with other concurrency primitives
-   The limitations of threads for CPU-heavy operations
-   How process-based execution can bypass the Global Interpreter Lock (GIL)

However, in **real-world production environments** (such as FastAPI apps served with Uvicorn or Gunicorn), we don't typically use thread or process pools manually.

Instead, we scale **horizontally** using **multiple worker processes**, like this:

```bash
gunicorn -k uvicorn.workers.UvicornWorker myapp:app -w 4
```

This launches multiple **independent Uvicorn workers**, each running its own event loop on a separate CPU core. It’s the standard, scalable approach to handling both I/O and CPU-bound traffic in production.

We’ll revisit and expand on this topic later to understand how concurrency and parallelism are handled at scale.

### async modules... httpx, aiohttp, aiosqlite

### build a server for fun? and compare with uvicorn

-   [Video Title 1](https://youtu.be/Ii7x4mpIhIs?si=JZtNMF0tORjjtU1W)
-   [Video Title 2](https://youtu.be/K56nNuBEd0c?si=rhvR-5LQE2DKEclg)
-   [Video Title 3](https://youtu.be/SAueUTQNup8?si=sF1kXLsJgMKcT2i6)
-   [Video Title 4](https://youtu.be/MfCbM6NKPeY?si=0F4fPh6f0J6a8jae)
