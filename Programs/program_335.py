from collections import OrderedDict
import time
import threading

class TTL_LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        # Stores {key: (value, expiration_time)}
        self.cache = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return None
            
            value, expiry = self.cache[key]
            current_time = time.time()
            
            if current_time > expiry:
                del self.cache[key]
                print(f"Key {key} expired.")
                return None
            
            # Move to the end (Most Recently Used)
            self.cache.move_to_end(key)
            return value

    def put(self, key, value, ttl_seconds):
        with self.lock:
            current_time = time.time()
            expiry = current_time + ttl_seconds
            
            if key in self.cache:
                del self.cache[key]
            elif len(self.cache) >= self.capacity:
                # Remove Least Recently Used (first item)
                self.cache.popitem(last=False)
                
            self.cache[key] = (value, expiry)

if __name__ == '__main__':
    cache = TTL_LRUCache(3)
    
    cache.put('A', 1, ttl_seconds=2)
    cache.put('B', 2, ttl_seconds=10)
    
    print(f"Get A (fresh): {cache.get('A')}")
    
    time.sleep(2.5) # A expires
    
    print(f"Get A (expired): {cache.get('A')}")
    print(f"Get B (fresh): {cache.get('B')}")
    
    cache.put('C', 3, ttl_seconds=10)
    cache.put('D', 4, ttl_seconds=10) # B should be evicted as LRU
    
    print(f"Cache size: {len(cache.cache)}")