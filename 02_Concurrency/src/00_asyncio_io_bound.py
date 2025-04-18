# GOOD CASE
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

url = "https://pkmn.li"

URLS = [url for _ in range(80)]


def fetch_url(url: str) -> str:
    response = httpx.get(url)
    return f"{url} returned with status code {response.status_code}"


# Executed Sequentially
start_time = time.perf_counter()

for url in URLS:
    response = fetch_url(url)
    # print(response)

duration = time.perf_counter() - start_time
print(f"Sequential Execution Took: {duration:.3f}s")


# Immediate collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor() as executor:
    results = executor.map(fetch_url, URLS)

# print(list(results))

duration = time.perf_counter() - start_time
print(f"Immediate Collection Took: {duration:.3f}s")


# asyncio execution
async def main():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in URLS]
        results = await asyncio.gather(*tasks)  # noqa: F841
        # for r in results:
        #     print(r.status_code)


start_time = time.perf_counter()

asyncio.run(main())

duration = time.perf_counter() - start_time
print(f"AsyncIO Collection Took: {duration:.3f}s")

# Sequential Execution Took: 96.931s
# Immediate Collection Took: 20.092s
# AsyncIO Collection Took: 2.314s
