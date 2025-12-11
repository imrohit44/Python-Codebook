import threading
import time
from collections import OrderedDict
import functools

def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = OrderedDict()
        cache_lock = threading.Lock()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()
            
            with cache_lock:
                if key in cache:
                    result, expiry = cache[key]
                    if current_time < expiry:
                        cache.move_to_end(key)
                        return result
                    else:
                        del cache[key]
                        
                # Compute and store new result
                result = func(*args, **kwargs)
                expiry = current_time + ttl_seconds
                cache[key] = (result, expiry)
                return result

        return wrapper
    return decorator

@ttl_cache(ttl_seconds=2)
def fetch_user_data(user_id, source):
    print(f"Fetching data for {user_id} from {source}...")
    time.sleep(0.1)
    return f"Data for {user_id} @ {time.time():.2f}"

def task(user_id):
    for _ in range(3):
        print(f"Call {user_id}: {fetch_user_data(user_id, 'DB')}")
        time.sleep(0.5)

if __name__ == '__main__':
    threading.Thread(target=task, args=(1,)).start()
    threading.Thread(target=task, args=(2,)).start()
    time.sleep(3) # Wait for cache to expire