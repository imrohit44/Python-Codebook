'''
# Caching Decorator

A decorator is a function that modifies another function. This program creates a decorator named @cache that stores the results of expensive function calls. When the same function is called with the same arguments again, it returns the cached result instantly instead of re-computing it.

**Concepts:**  

Decorators, higher-order functions, metaprogramming, caching

**How to Run**

**1. Save the code and execute it:**

```
python Program_3.py
```
'''


import time
import functools

def cache(func):
    """A simple decorator to cache function results."""
    cache_dict = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from the function's arguments
        key = (args, frozenset(kwargs.items()))
        if key not in cache_dict:
            print(f"Calculating {func.__name__}{args}...")
            cache_dict[key] = func(*args, **kwargs)
        else:
            print(f"Returning cached result for {func.__name__}{args}...")
        return cache_dict[key]
    return wrapper

@cache
def slow_fibonacci(n):
    """Calculates the nth Fibonacci number recursively (and slowly)."""
    if n < 2:
        return n
    return slow_fibonacci(n-1) + slow_fibonacci(n-2)

if __name__ == "__main__":
    # The first time this runs, it will be slow and calculate all intermediate values.
    print("--- First Run ---")
    start_time = time.time()
    result = slow_fibonacci(20)
    end_time = time.time()
    print(f"Fibonacci(20) = {result}")
    print(f"Time taken: {end_time - start_time:.4f} seconds\n")

    # The second run will be instantaneous because all results are cached.
    print("--- Second Run ---")
    start_time = time.time()
    result = slow_fibonacci(20)
    end_time = time.time()
    print(f"Fibonacci(20) = {result}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")