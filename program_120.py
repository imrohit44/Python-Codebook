import ctypes
import threading
import time
import random

class Node(ctypes.Structure):
    _fields_ = [("value", ctypes.py_object), ("next", ctypes.py_object)]

class LockFreeStack:
    def __init__(self):
        self.head = ctypes.py_object(None)
        self.lock = threading.Lock()

    def push(self, value):
        new_node = Node(value=value)
        with self.lock:
            new_node.next = self.head
            self.head = ctypes.py_object(new_node)

    def pop(self):
        with self.lock:
            if not self.head:
                return None
            old_head = self.head
            self.head = old_head.value.next
            return old_head.value.value

def worker(stack, num_items):
    for i in range(num_items):
        stack.push(f"item-{threading.get_ident()}-{i}")
        time.sleep(random.uniform(0.01, 0.05))

if __name__ == '__main__':
    lock_free_stack = LockFreeStack()
    threads = [threading.Thread(target=worker, args=(lock_free_stack, 10)) for _ in range(5)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    count = 0
    while True:
        item = lock_free_stack.pop()
        if item is None:
            break
        count += 1
    print(f"Total items popped: {count}")