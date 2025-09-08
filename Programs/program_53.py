def bellman_ford(graph, num_vertices, start_node):
    distances = {node: float('inf') for node in range(num_vertices)}
    distances[start_node] = 0
    
    for _ in range(num_vertices - 1):
        for u, v, weight in graph:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
    
    for u, v, weight in graph:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            return None, "Negative cycle detected"
            
    return distances, "No negative cycle"

if __name__ == "__main__":
    num_vertices = 5
    edges = [
        (0, 1, -1), (0, 2, 4),
        (1, 2, 3), (1, 3, 2), (1, 4, 2),
        (3, 2, 5), (3, 1, 1),
        (4, 3, -3)
    ]
    
    dist, msg = bellman_ford(edges, num_vertices, 0)
    print(msg)
    if dist:
        print(dist)

    num_vertices_cycle = 4
    edges_cycle = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 3, -1),
        (3, 0, -1)
    ]
    dist_cycle, msg_cycle = bellman_ford(edges_cycle, num_vertices_cycle, 0)
    print(msg_cycle)