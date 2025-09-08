from collections import OrderedDict

def custom_lru_cache(maxsize):
    cache = OrderedDict()

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                value = cache.pop(key)
                cache[key] = value
                return value
            
            value = func(*args, **kwargs)
            if len(cache) >= maxsize:
                cache.popitem(last=False)
            cache[key] = value
            return value

        return wrapper
        
@custom_lru_cache(maxsize=3)
def expensive_function(a, b):
    print(f"Calling expensive_function with {a}, {b}")
    return a + b

if __name__ == "__main__":
    print(expensive_function(1, 2))
    print(expensive_function(3, 4))
    print(expensive_function(1, 2))
    print(expensive_function(5, 6))
    print(expensive_function(3, 4))
    print(expensive_function(1, 2))