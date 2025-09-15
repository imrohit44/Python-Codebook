class PriorityQueue:
    def __init__(self):
        self._queue = []
        
    def push(self, item, priority):
        self._queue.append((priority, item))
        self._queue.sort()

    def pop(self):
        if not self._queue:
            return None
        return self._queue.pop(0)[1]

    def is_empty(self):
        return not self._queue

def dijkstra_with_custom_pq(graph, start_node):
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    pq = PriorityQueue()
    pq.push(start_node, 0)
    
    while not pq.is_empty():
        current_node = pq.pop()
        
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                pq.push(neighbor, distance)
    
    return distances

if __name__ == '__main__':
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'C': 2, 'D': 5},
        'C': {'D': 1},
        'D': {}
    }
    
    shortest_paths = dijkstra_with_custom_pq(graph, 'A')
    print(f"Shortest paths from A: {shortest_paths}")