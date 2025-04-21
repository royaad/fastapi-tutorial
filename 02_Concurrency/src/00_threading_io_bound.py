# GOOD CASE
# import threading
import time
from concurrent.futures import ThreadPoolExecutor  # , as_completed

import httpx

# import aiohttp # offers an equivalent alternative to httpx

url = "https://pkmn.li"

URLS = [url for _ in range(80)]


def fetch_url(url: str) -> str:
    # print(
    #     f"fetching: {url} on thread with id: {threading.get_ident()} and name: {threading.current_thread().name}"
    # )
    response = httpx.get(url)
    # print(f"done: {url}")
    return f"{url} returned with status code {response.status_code}"


# Executed Sequentially
start_time = time.perf_counter()

for url in URLS:
    print(fetch_url(url))

duration = time.perf_counter() - start_time
print(f"Sequential Execution Took: {duration:.3f}s")

# Lazy collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=None) as executor:
    futures = [executor.submit(fetch_url, url) for url in URLS]
    # for future in as_completed(futures):
    #     print(f"Result: {future.result()}")

duration = time.perf_counter() - start_time
print(f"Lazy Async Calls Took: {duration:.3f}s")

# Immediate collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=None) as executor:
    results = executor.map(fetch_url, URLS)

# print(list(results))

duration = time.perf_counter() - start_time
print(f"Immediate Collection Took: {duration:.3f}s")

# Sequential Execution Took: 98.609s
# Lazy Async Calls Took:     28.581s
# Immediate Collection Took: 17.968s
