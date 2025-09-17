class MinHeap:
    def __init__(self):
        self._heap = []

    def _sift_up(self, index):
        parent_index = (index - 1) // 2
        if parent_index < 0:
            return
        
        if self._heap[index] < self._heap[parent_index]:
            self._heap[index], self._heap[parent_index] = self._heap[parent_index], self._heap[index]
            self._sift_up(parent_index)

    def _sift_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        
        smallest = index
        if left_child_index < len(self._heap) and self._heap[left_child_index] < self._heap[smallest]:
            smallest = left_child_index
        if right_child_index < len(self._heap) and self._heap[right_child_index] < self._heap[smallest]:
            smallest = right_child_index
            
        if smallest != index:
            self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
            self._sift_down(smallest)

    def push(self, value):
        self._heap.append(value)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        if not self._heap:
            return None
        
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        value = self._heap.pop()
        self._sift_down(0)
        
        return value

if __name__ == '__main__':
    heap = MinHeap()
    heap.push(5)
    heap.push(3)
    heap.push(8)
    heap.push(1)
    
    print(heap.pop())
    print(heap.pop())