import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

URLS = [
    "http://www.foxnews.com/",
    "http://www.cnn.com/",
    "http://europe.wsj.com/",
    "http://www.bbc.co.uk/",
    "http://google.com/",
    "http://example.com/",
    "https://httpbin.org/get",
]


def fetch_url(url: str) -> str:
    response = httpx.get(url)
    return f"{url} returned with status code {response.status_code}"


# Immediate collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor() as executor:
    results = executor.map(fetch_url, URLS)

print(list(results))

duration = time.perf_counter() - start_time
print(f"Immediate Collection Took: {duration:.3f}s")


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in URLS]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(r.status_code)


start_time = time.perf_counter()

asyncio.run(main())

duration = time.perf_counter() - start_time
print(f"AsyncIO Collection Took: {duration:.3f}s")
