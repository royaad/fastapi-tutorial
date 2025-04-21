# BAD CASE
import asyncio
import time

url = "https://pkmn.li"

URLS = [url for _ in range(80)]


async def factorial(n):
    return sum(i * i for i in range(1, n))


numbers = [10000000 + i for i in range(8)]


# A coroutine cannot be ran directly


# asyncio execution
async def main():
    tasks = [factorial(number) for number in numbers]
    results = await asyncio.gather(*tasks)  # noqa: F841
    print(results)


start_time = time.perf_counter()

asyncio.run(main())

duration = time.perf_counter() - start_time
print(f"AsyncIO Collection Took: {duration:.3f}s")

# AsyncIO Collection Took: 16.107s
# sys:1: RuntimeWarning: coroutine 'factorial' was never awaited
