import heapq

def a_star_search(grid, start, end):
    """
    Finds the shortest path in a grid using the A* algorithm.

    Args:
        grid (list[list[int]]): 2D list representing the grid (0=walkable, 1=obstacle).
        start (tuple[int, int]): (row, col) coordinates of the start point.
        end (tuple[int, int]): (row, col) coordinates of the end point.

    Returns:
        list[tuple[int, int]] or None: The path as a list of (row, col) tuples,
                                        or None if no path exists.
    """
    rows, cols = len(grid), len(grid[0])

    # Check valid start/end points
    if not (0 <= start[0] < rows and 0 <= start[1] < cols and grid[start[0]][start[1]] == 0):
        print(f"Invalid start point: {start} or it's an obstacle.")
        return None
    if not (0 <= end[0] < rows and 0 <= end[1] < cols and grid[end[0]][end[1]] == 0):
        print(f"Invalid end point: {end} or it's an obstacle.")
        return None
    
    # Priority queue: (f_score, g_score, current_node)
    # The g_score is included for tie-breaking, preferring shorter paths in case of equal f_scores.
    open_set = [(0, 0, start)] # (f_score, g_score, node)

    # g_score[node] is the cost of the cheapest path from start to node currently known
    g_score = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    g_score[start] = 0

    # came_from[node] is the node immediately preceding it on the cheapest path found so far
    came_from = {}

    # Heuristic function (Manhattan distance)
    def heuristic(node_a, node_b):
        return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])

    # Possible movements (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while open_set:
        current_f, current_g, current_node = heapq.heappop(open_set)

        if current_node == end:
            # Reconstruct path
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1] # Reverse to get path from start to end

        for dr, dc in directions:
            neighbor = (current_node[0] + dr, current_node[1] + dc)
            
            # Check if neighbor is within grid bounds and not an obstacle
            if (0 <= neighbor[0] < rows and
                0 <= neighbor[1] < cols and
                grid[neighbor[0]][neighbor[1]] == 0):

                tentative_g_score = g_score[current_node] + 1 # Cost to move to neighbor is 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))
    
    return None # No path found

# Function to print the path on the grid (optional for visualization)
def print_path_on_grid(grid, path):
    if not path:
        print("No path to display.")
        return

    rows, cols = len(grid), len(grid[0])
    display_grid = [row[:] for row in grid] # Make a copy

    for r, c in path:
        if (r, c) == path[0]:
            display_grid[r][c] = 'S' # Start
        elif (r, c) == path[-1]:
            display_grid[r][c] = 'E' # End
        else:
            display_grid[r][c] = '*' # Path

    for r in range(rows):
        for c in range(cols):
            val = display_grid[r][c]
            if val == 0:
                print(".", end=" ")
            elif val == 1:
                print("#", end=" ")
            else:
                print(val, end=" ")
        print() # New line for each row

# Example Usage:
grid1 = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

start1 = (0, 0)
end1 = (4, 4)
print("--- Grid 1 Path ---")
path1 = a_star_search(grid1, start1, end1)
print(f"Path from {start1} to {end1}: {path1}")
print_path_on_grid(grid1, path1)

print("\n--- Grid 2 Path (No Path) ---")
grid2 = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]
start2 = (0, 0)
end2 = (4, 4)
path2 = a_star_search(grid2, start2, end2)
print(f"Path from {start2} to {end2}: {path2}")
print_path_on_grid(grid2, path2)

print("\n--- Grid 3 Path (Short Path) ---")
grid3 = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]
start3 = (0, 0)
end3 = (2, 2)
path3 = a_star_search(grid3, start3, end3)
print(f"Path from {start3} to {end3}: {path3}")
print_path_on_grid(grid3, path3)