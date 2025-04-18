# GOOD CASE
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool, cpu_count


def factorial(n):
    return sum(i * i for i in range(1, n))


def main():
    numbers = [10000000 + i for i in range(8)]
    # Executed Sequentially
    start_time = time.perf_counter()

    results = [factorial(n) for n in numbers]

    duration = time.perf_counter() - start_time

    print(f"Sequential Execution Took: {duration:.3f}s")
    print(results)

    # Legacy Python Code
    start_time = time.perf_counter()

    with Pool(cpu_count()) as executor:
        results = executor.map(factorial, numbers)

    duration = time.perf_counter() - start_time

    print(f"Legacy ProcessPool Execution Took: {duration:.3f}s")
    print(results)

    # Python 3.10+
    start_time = time.perf_counter()

    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        results = executor.map(factorial, numbers)

    duration = time.perf_counter() - start_time

    print(f"ProcessPool Execution Took: {duration:.3f}s")
    print(list(results))


# On Windows the subprocesses will import (i.e. execute) the main module at start.
# You need to insert an `if __name__ == '__main__':` guard in the main module to avoid creating subprocesses recursively.
if __name__ == "__main__":
    main()

    # Sequential Execution Took: 16.942s
    # Legacy ProcessPool Execution Took: 5.570s
    # ProcessPool Execution Took: 5.629s
