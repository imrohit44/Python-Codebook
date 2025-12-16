def has_cycle_directed(graph):
    visited = set()
    recursion_stack = set()
    
    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True
        
        recursion_stack.remove(node)
        return False
        
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    
    return False

if __name__ == '__main__':
    graph1 = { # Cycle: A -> B -> C -> A
        'A': ['B'],
        'B': ['C'],
        'C': ['A'],
        'D': ['E'],
        'E': []
    }
    print(f"Graph 1 has cycle: {has_cycle_directed(graph1)}")

    graph2 = { # No Cycle
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    print(f"Graph 2 has cycle: {has_cycle_directed(graph2)}")