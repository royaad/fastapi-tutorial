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

### Event Loop

### async, await

### async modules... httpx, aiohttp, aiosqlite

### build a server for fun? and compare with uvicorn

-   [Video Title 1](https://youtu.be/Ii7x4mpIhIs?si=JZtNMF0tORjjtU1W)
-   [Video Title 2](https://youtu.be/K56nNuBEd0c?si=rhvR-5LQE2DKEclg)
-   [Video Title 3](https://youtu.be/SAueUTQNup8?si=sF1kXLsJgMKcT2i6)
-   [Video Title 4](https://youtu.be/MfCbM6NKPeY?si=0F4fPh6f0J6a8jae)
