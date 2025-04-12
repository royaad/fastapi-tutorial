import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    print(
        f"fetching: {url} on thread with id: {threading.get_ident()} and name: {threading.current_thread().name}"
    )
    response = httpx.get(url)
    print(f"done: {url}")
    return f"{url} returned with status code {response.status_code}"


# Executed Sequentially

start_time = time.perf_counter()

for url in URLS:
    print(fetch_url(url))

duration = time.perf_counter() - start_time
print(f"Sequential Execution Took: {duration:.3f}s")

# Lazy collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=5) as executor:
    # executor.map(task, range(5))
    futures = [executor.submit(fetch_url, url) for url in URLS]
    for future in as_completed(futures):
        print(f"Result: {future.result()}")

duration = time.perf_counter() - start_time
print(f"Lazy Async Calls Took: {duration:.3f}s")

# Immediate collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_url, URLS)

print(list(results))

duration = time.perf_counter() - start_time
print(f"Immediate Collection Took: {duration:.3f}s")
