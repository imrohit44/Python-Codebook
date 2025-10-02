import threading
import time

class ThreadSafePriorityQueue:
    def __init__(self):
        self._heap = []
        self._lock = threading.Lock()

    def _sift_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self._heap[index][0] < self._heap[parent_index][0]:
            self._heap[index], self._heap[parent_index] = self._heap[parent_index], self._heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _sift_down(self, index):
        size = len(self._heap)
        smallest = index
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            
            if left < size and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < size and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right
            
            if smallest != index:
                self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
                index = smallest
            else:
                break

    def push(self, item, priority):
        with self._lock:
            self._heap.append((priority, item))
            self._sift_up(len(self._heap) - 1)

    def pop(self):
        with self._lock:
            if not self._heap:
                return None
            if len(self._heap) == 1:
                return self._heap.pop()[1]
            
            root = self._heap[0]
            self._heap[0] = self._heap.pop()
            self._sift_down(0)
            return root[1]

    def is_empty(self):
        with self._lock:
            return not self._heap

def worker(pq, name, priority):
    pq.push(f"Task {name} start", priority)
    time.sleep(random.uniform(0.1, 0.5))
    pq.push(f"Task {name} end", priority)

if __name__ == '__main__':
    pq = ThreadSafePriorityQueue()
    
    threads = [
        threading.Thread(target=worker, args=(pq, "Low", 10)),
        threading.Thread(target=worker, args=(pq, "High", 1)),
        threading.Thread(target=worker, args=(pq, "Medium", 5))
    ]

    for t in threads: t.start()
    for t in threads: t.join()
    
    while not pq.is_empty():
        print(f"Executing: {pq.pop()}")