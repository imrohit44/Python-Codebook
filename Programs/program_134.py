def bellman_ford(graph, start_node):
    num_vertices = len(graph)
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    
    for _ in range(num_vertices - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
    
    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                return None, "Negative cycle detected."
                
    return distances, "No negative cycle."

if __d__ == '__main__':
    graph1 = {
        'A': {'B': 10, 'C': 5},
        'B': {'C': 2, 'D': 1},
        'C': {'B': 3, 'D': 9, 'E': 2},
        'D': {'E': 4},
        'E': {'A': 7, 'B': -1}
    }
    dist, msg = bellman_ford(graph1, 'A')
    print(f"Distances: {dist}, Message: {msg}")
    
    graph2 = {
        'A': {'B': 1},
        'B': {'C': -1},
        'C': {'A': -1}
    }
    dist, msg = bellman_ford(graph2, 'A')
    print(f"Distances: {dist}, Message: {msg}")