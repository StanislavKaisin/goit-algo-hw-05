import timeit
from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    cache = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


def fibonacci_no_cache(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


fib = caching_fibonacci()
print(fib(10))
print(fib(35))

n = 20
time_caching = timeit.timeit(lambda: fib(n), number=1000)
time_no_cache = timeit.timeit(lambda: fibonacci_no_cache(n), number=1000)

print("time_caching = ", time_caching)  # 0.00012104200141038746
print("time_no_cache = ", time_no_cache)  # 1.5208435840031598
print(
    "time_no_cache / time_caching= ", time_no_cache / time_caching
)  # 3944.182448539036
