# BAD CASE
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

import httpx


def fetch_url(url: str) -> str:
    response = httpx.get(url)
    return f"{url} returned with status code {response.status_code}"


def main():

    url = "https://pkmn.li"

    # Executed Sequentially
    start_time = time.perf_counter()

    results = [
        fetch_url(url) for _ in range(80)
    ]  # make it 10 times more than my cpu count

    duration = time.perf_counter() - start_time

    print(f"Sequential Execution Took: {duration:.3f}s")
    print(results)

    # Python 3.10+
    start_time = time.perf_counter()

    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = executor.map(fetch_url, [url for _ in range(80)])

    duration = time.perf_counter() - start_time

    print(f"ProcessPool Execution Took: {duration:.3f}s")
    print(list(results))


# On Windows the subprocesses will import (i.e. execute) the main module at start.
# You need to insert an `if __name__ == '__main__':` guard in the main module to avoid creating subprocesses recursively.
if __name__ == "__main__":
    main()

    # Sequential Execution Took:  93.771s
    # ProcessPool Execution Took: 23.363s
