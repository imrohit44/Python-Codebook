import ctypes
import threading
import time

class Node(ctypes.Structure):
    _fields_ = [("value", ctypes.py_object), ("next", ctypes.py_object)]

class LockFreeQueue:
    def __init__(self):
        self.head = ctypes.py_object(None)
        self.tail = ctypes.py_object(None)
        self.lock = threading.Lock()

    def push(self, value):
        new_node = Node(value=value)
        with self.lock:
            if not self.tail:
                self.head = ctypes.py_object(new_node)
                self.tail = ctypes.py_object(new_node)
            else:
                self.tail.value.next = ctypes.py_object(new_node)
                self.tail = ctypes.py_object(new_node)

    def pop(self):
        with self.lock:
            if not self.head:
                return None
            old_head = self.head
            self.head = old_head.value.next
            if not self.head:
                self.tail = ctypes.py_object(None)
            return old_head.value.value
            
def worker(queue, num_items):
    for i in range(num_items):
        queue.push(f"item-{threading.get_ident()}-{i}")
        time.sleep(random.uniform(0.01, 0.05))

if __name__ == '__main__':
    lock_free_queue = LockFreeQueue()
    threads = [threading.Thread(target=worker, args=(lock_free_queue, 10)) for _ in range(5)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    count = 0
    while True:
        item = lock_free_queue.pop()
        if item is None:
            break
        count += 1
    print(f"Total items popped: {count}")