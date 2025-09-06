def has_cycle(graph):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False
        
    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    
    return False

if __name__ == '__main__':
    graph1 = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }
    print(has_cycle(graph1))

    graph2 = {
        'A': ['B', 'C'],
        'B': ['A'],
        'C': ['A']
    }
    print(has_cycle(graph2))