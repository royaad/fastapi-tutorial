# BAD CASE
import time
from concurrent.futures import ThreadPoolExecutor


def factorial(n):
    return sum(i * i for i in range(1, n))


numbers = [10000000 + i for i in range(8)]

# Executed Sequentially
start_time = time.perf_counter()

results = [factorial(n) for n in numbers]

duration = time.perf_counter() - start_time

print(f"Sequential Execution Took: {duration:.3f}s")

# Immediate collection of results
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=None) as executor:
    results = executor.map(factorial, numbers)

duration = time.perf_counter() - start_time
print(f"Immediate Collection Took: {duration:.3f}s")

# Sequential Execution Took: 16.232s
# Immediate Collection Took: 16.432s
