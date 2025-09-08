import threading

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

def lru_cache_thread_safe(maxsize):
    cache = {}
    head = Node(None, None)
    tail = Node(None, None)
    head.next = tail
    tail.prev = head
    lock = threading.Lock()

    def _remove(node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(node):
        node.next = head.next
        node.prev = head
        head.next.prev = node
        head.next = node

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            with lock:
                if key in cache:
                    node = cache[key]
                    _remove(node)
                    _add_to_head(node)
                    return node.value

            value = func(*args, **kwargs)
            with lock:
                if key in cache:
                    node = cache[key]
                    node.value = value
                    _remove(node)
                    _add_to_head(node)
                else:
                    new_node = Node(key, value)
                    cache[key] = new_node
                    _add_to_head(new_node)
                    
                if len(cache) > maxsize:
                    lru_node = tail.prev
                    _remove(lru_node)
                    del cache[lru_node.key]
            
            return value
        return wrapper

@lru_cache_thread_safe(maxsize=3)
def heavy_computation(a, b):
    time.sleep(0.1)
    return a * b

def worker(a, b):
    print(f"Result for ({a}, {b}): {heavy_computation(a, b)}")

if __name__ == '__main__':
    threads = [threading.Thread(target=worker, args=(i, i+1)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()