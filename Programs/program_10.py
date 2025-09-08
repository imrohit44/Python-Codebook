import heapq

def dijkstra(graph, start_node):
    """
    Finds the shortest path from a start_node to all other nodes in a weighted graph
    using Dijkstra's algorithm.

    Args:
        graph (dict): Adjacency list representation where graph[node] is a list of (neighbor, weight) tuples.
        start_node: The starting node for path calculation.

    Returns:
        dict: A dictionary mapping each node to its shortest distance from the start_node.
              Returns float('inf') for unreachable nodes.
    """
    # Initialize distances with infinity for all nodes and 0 for the start_node
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0

    # Priority queue to store (distance, node). Stores nodes to visit, ordered by shortest distance found so far.
    priority_queue = [(0, start_node)] # (distance, node)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we've already found a shorter path to this node, skip
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Example Usage:
graph1 = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}
print("Graph 1 Shortest Paths from A:", dijkstra(graph1, 'A'))
# Expected: {'A': 0, 'B': 1, 'C': 3, 'D': 4}

graph2 = {
    'S': [('A', 10), ('C', 1)],
    'A': [('B', 2)],
    'B': [('D', 7)],
    'C': [('A', 4), ('D', 8)],
    'D': [('E', 3)],
    'E': []
}
print("Graph 2 Shortest Paths from S:", dijkstra(graph2, 'S'))
# Expected: {'S': 0, 'A': 5, 'B': 7, 'C': 1, 'D': 9, 'E': 12}

graph3 = {
    'X': [('Y', 7)],
    'Y': [('Z', 2)],
    'Z': []
}
print("Graph 3 Shortest Paths from X:", dijkstra(graph3, 'X'))
# Expected: {'X': 0, 'Y': 7, 'Z': 9}