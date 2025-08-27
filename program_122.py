from collections import deque

def bfs(graph, s, t, parent):
    visited = [False] * len(graph)
    queue = deque()
    queue.append(s)
    visited[s] = True
    parent[s] = -1

    while queue:
        u = queue.popleft()
        for v in range(len(graph)):
            if not visited[v] and graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False

def ford_fulkerson(graph, s, t):
    parent = [0] * len(graph)
    max_flow = 0
    
    while bfs(graph, s, t, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = parent[v]

        max_flow += path_flow
        v = t
        while v != s:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    
    return max_flow

def max_bipartite_matching(bipartite_graph):
    u_count = len(bipartite_graph[0])
    v_count = len(bipartite_graph[1])
    source = u_count + v_count
    sink = u_count + v_count + 1
    
    flow_network = [[0] * (sink + 1) for _ in range(sink + 1)]
    
    for i in range(u_count):
        flow_network[source][i] = 1
        for j in range(v_count):
            if bipartite_graph[0][i][j] == 1:
                flow_network[i][u_count + j] = 1
    
    for i in range(v_count):
        flow_network[u_count + i][sink] = 1
        
    return ford_fulkerson(flow_network, source, sink)

if __name__ == '__main__':
    bipartite_graph = [
        [
            [0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0]
        ],
        [
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1]
        ]
    ]
    print(f"Maximum matching is {max_bipartite_matching(bipartite_graph)}")