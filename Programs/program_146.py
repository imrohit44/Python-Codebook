import threading
import time

class ConcurrentQueue:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self._queue = []
        self._lock = threading.Lock()
        self._full_event = threading.Event()
        self._empty_event = threading.Event()
        self._full_event.set()

    def put(self, item, timeout=None):
        backoff = 0.01
        while True:
            with self._lock:
                if len(self._queue) < self.maxsize:
                    self._queue.append(item)
                    self._empty_event.set()
                    return
            
            if timeout is not None and backoff > timeout:
                raise TimeoutError
            
            self._full_event.clear()
            self._full_event.wait(backoff)
            backoff *= 2

    def get(self, timeout=None):
        backoff = 0.01
        while True:
            with self._lock:
                if self._queue:
                    item = self._queue.pop(0)
                    self._full_event.set()
                    return item
            
            if timeout is not None and backoff > timeout:
                raise TimeoutError
                
            self._empty_event.clear()
            self._empty_event.wait(backoff)
            backoff *= 2

def producer(q):
    for i in range(5):
        q.put(i)
        time.sleep(0.1)

def consumer(q):
    for _ in range(5):
        item = q.get()
        print(f"Consumed: {item}")

if __name__ == '__main__':
    q = ConcurrentQueue(maxsize=3)
    p = threading.Thread(target=producer, args=(q,))
    c = threading.Thread(target=consumer, args=(q,))
    
    p.start()
    c.start()
    
    p.join()
    c.join()