from collections import deque

def solve_maze_bfs(maze, start, end):
    """
    Finds a path from start to end in a maze using Breadth-First Search (BFS).
    Returns True if a path exists, False otherwise.
    If a path exists, it also prints one such path.
    """
    rows, cols = len(maze), len(maze[0])
    
    # Check if start or end are walls or out of bounds
    if not (0 <= start[0] < rows and 0 <= start[1] < cols and maze[start[0]][start[1]] == 0):
        return False
    if not (0 <= end[0] < rows and 0 <= end[1] < cols and maze[end[0]][end[1]] == 0):
        return False

    queue = deque([(start, [start])]) # (current_position, path_taken_to_reach_current_position)
    visited = set([start])

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            print(f"Path found: {path}")
            return True

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check boundaries and if it's a valid path (0) and not visited
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)])) # Extend the path

    return False

# Solution (using DFS - simpler to implement for existence, but not necessarily shortest)
def solve_maze_dfs(maze, start, end):
    """
    Finds if a path exists from start to end in a maze using Depth-First Search (DFS).
    Returns True if a path exists, False otherwise.
    """
    rows, cols = len(maze), len(maze[0])
    visited = set()

    # Check if start or end are walls or out of bounds
    if not (0 <= start[0] < rows and 0 <= start[1] < cols and maze[start[0]][start[1]] == 0):
        return False
    if not (0 <= end[0] < rows and 0 <= end[1] < cols and maze[end[0]][end[1]] == 0):
        return False

    def dfs(r, c):
        if (r, c) == end:
            return True
        
        if not (0 <= r < rows and 0 <= c < cols and maze[r][c] == 0 and (r, c) not in visited):
            return False

        visited.add((r, c))

        # Explore neighbors
        if dfs(r + 1, c) or dfs(r - 1, c) or dfs(r, c + 1) or dfs(r, c - 1):
            return True
        
        # If no path found from this node, backtrack
        # (This line is effectively optional as visited set handles it for path existence)
        # visited.remove((r, c)) 
        return False

    return dfs(start[0], start[1])

maze1 = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start1 = (0, 4)
end1 = (4, 4)
print(f"Maze 1 (BFS) - Path from {start1} to {end1}: {solve_maze_bfs(maze1, start1, end1)}") # True

start2 = (0, 0)
end2 = (0, 2) # A wall
print(f"Maze 1 (BFS) - Path from {start2} to {end2}: {solve_maze_bfs(maze1, start2, end2)}") # False

maze2 = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]
start3 = (0, 0)
end3 = (4, 4)
print(f"\nMaze 2 (BFS) - Path from {start3} to {end3}: {solve_maze_bfs(maze2, start3, end3)}") # True

print(f"\nMaze 1 (DFS) - Path from {start1} to {end1}: {solve_maze_dfs(maze1, start1, end1)}") # True
print(f"Maze 1 (DFS) - Path from {start2} to {end2}: {solve_maze_dfs(maze1, start2, end2)}") # False
print(f"Maze 2 (DFS) - Path from {start3} to {end3}: {solve_maze_dfs(maze2, start3, end3)}") # True