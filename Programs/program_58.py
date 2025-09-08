from collections import deque

def is_bipartite(graph):
    num_vertices = len(graph)
    colors = [-1] * num_vertices

    for start_node in range(num_vertices):
        if colors[start_node] == -1:
            queue = deque([start_node])
            colors[start_node] = 0

            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if colors[v] == -1:
                        colors[v] = 1 - colors[u]
                        queue.append(v)
                    elif colors[v] == colors[u]:
                        return False

    return True

if __name__ == "__main__":
    graph1 = [
        [1, 3],
        [0, 2],
        [1, 3],
        [0, 2]
    ]
    print(is_bipartite(graph1))
    
    graph2 = [
        [1, 2],
        [0, 2],
        [0, 1]
    ]
    print(is_bipartite(graph2))