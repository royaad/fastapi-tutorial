# Concurrency

In the previous parts, we mentioned that FastAPI can handle synchronous and asynchronous functions. however, there is a best practice to when to use synchronous and asynchronous. In this part, we try to our best to explain when to use synchronous vs when not to. in order to better understand when, we will briefly not deal with FastAPI, but instead explain what is concurency and parallelism and how to use them in python and how they affect the latency of a software before we imbark again on our FastAPI journey

## What is Asynchronous Function?

When a function is called synchronously each step in that function must complete before the next step is executed. However, in an asynchronous function tasks are executed "concurrently". so to understand asynchronous functions we must first understand concurency. so what is concurency?

### Concurrency vs. Parallelism

A lot of times concurrency is confused with parrallelism.
- Parallelism is achieved when multiple task are executed at the exact same time by levaraging multiple CPU cores. Parellilism in about independability. Tasks run independently of each other, at the exact same time.
- Concurrency on the other hand is about managing multiple tasks by interleaving their execution giving the illusion that they are happening simultaneously. Basically concurency is about interrubtibility. Tasks interupt and resume, making them appear to progress.

Parallelism is suitable for CPU-intensive tasks such as mathematical computations
Concurrency is best for I/O bound tasks such as file read/write and network based tasks.

### Concurrency and Parallelism in Python

In python concurrency is achieved by using the `Threading` Module while parallelism can be achieved by using the `multiprocessing` module


https://youtu.be/Ii7x4mpIhIs?si=JZtNMF0tORjjtU1W
https://youtu.be/K56nNuBEd0c?si=rhvR-5LQE2DKEclg
https://youtu.be/SAueUTQNup8?si=sF1kXLsJgMKcT2i6
https://youtu.be/MfCbM6NKPeY?si=0F4fPh6f0J6a8jae