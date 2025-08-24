import threading
import time

class SharedList:
    def __init__(self):
        self._list = []
        self._lock = threading.Lock()

    def append(self, item):
        with self._lock:
            self._list.append(item)

    def pop(self):
        with self._lock:
            if self._list:
                return self._list.pop()
            return None

    def get_item(self, index):
        with self._lock:
            if 0 <= index < len(self._list):
                return self._list[index]
            return None

    def __len__(self):
        with self._lock:
            return len(self._list)

def worker(shared_list, worker_id):
    for i in range(5):
        shared_list.append(f"Item {worker_id}-{i}")
        time.sleep(0.1)

if __name__ == '__main__':
    shared_list = SharedList()
    threads = [threading.Thread(target=worker, args=(shared_list, i)) for i in range(3)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"Final list length: {len(shared_list)}")
    print(f"Last item: {shared_list.pop()}")