from collections import defaultdict

def topological_sort(graph):
    visited = set()
    recursion_stack = set()
    result = []

    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if not dfs(neighbor):
                    return False
            elif neighbor in recursion_stack:
                return False
        
        recursion_stack.remove(node)
        result.append(node)
        return True

    for node in graph:
        if node not in visited:
            if not dfs(node):
                return None
    
    return result[::-1]

if __name__ == "__main__":
    graph1 = {
        'A': ['C', 'D'],
        'B': ['D'],
        'C': ['E'],
        'D': ['F', 'G'],
        'E': [],
        'F': [],
        'G': []
    }
    print(topological_sort(graph1))

    graph2 = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }
    print(topological_sort(graph2))