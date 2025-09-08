def floyd_warshall(graph):
    n = len(graph)
    distances = [row[:] for row in graph]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
    
    return distances

if __name__ == '__main__':
    inf = float('inf')
    graph = [
        [0, 5, inf, 10],
        [inf, 0, 3, inf],
        [inf, inf, 0, 1],
        [inf, inf, inf, 0]
    ]
    
    shortest_paths = floyd_warshall(graph)
    for row in shortest_paths:
        print(row)