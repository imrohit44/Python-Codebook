def solve_sudoku(board: list[list[int]]) -> bool:
    """
    Solves a Sudoku puzzle using backtracking. Modifies the board in-place.
    Args:
        board (list[list[int]]): The 9x9 Sudoku board, with 0s for empty cells.
    Returns:
        bool: True if a solution is found, False otherwise.
    """
    
    empty_cell = find_empty(board)
    if not empty_cell:
        return True # No empty cells left, puzzle solved!
    else:
        row, col = empty_cell

    for num in range(1, 10): # Try numbers 1 through 9
        if is_valid(board, num, (row, col)):
            board[row][col] = num # Place the number

            if solve_sudoku(board): # Recursively try to solve the rest
                return True
            
            board[row][col] = 0 # Backtrack: if the current placement leads to no solution, reset the cell

    return False # No number worked for this cell

def find_empty(board: list[list[int]]) -> tuple[int, int] | None:
    """Finds the next empty cell (represented by 0)."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid(board: list[list[int]], num: int, pos: tuple[int, int]) -> bool:
    """
    Checks if placing 'num' at 'pos' (row, col) is valid according to Sudoku rules.
    """
    row, col = pos

    # Check row
    for c in range(9):
        if board[row][c] == num and col != c:
            return False

    # Check column
    for r in range(9):
        if board[r][col] == num and row != r:
            return False

    # Check 3x3 box
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3

    for r in range(box_start_row, box_start_row + 3):
        for c in range(box_start_col, box_start_col + 3):
            if board[r][c] == num and (r, c) != pos:
                return False

    return True

def print_board(board: list[list[int]]):
    """Prints the Sudoku board in a readable format."""
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("- - - - - - - - - - - - ")

        for c in range(9):
            if c % 3 == 0 and c != 0:
                print(" | ", end="")

            if c == 8:
                print(board[r][c])
            else:
                print(str(board[r][c]) + " ", end="")

# Example Usage:
if __name__ == "__main__":
    puzzle1 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("--- Original Puzzle 1 ---")
    print_board(puzzle1)
    print("\nSolving...\n")

    if solve_sudoku(puzzle1):
        print("--- Solved Puzzle 1 ---")
        print_board(puzzle1)
    else:
        print("No solution found for Puzzle 1.")

    puzzle2 = [ # A puzzle with no solution
        [1, 2, 3, 4, 5, 6, 7, 8, 0],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 1, 4, 3, 6, 5, 8, 9, 7],
        [3, 6, 5, 8, 9, 7, 2, 1, 4],
        [8, 9, 7, 2, 1, 4, 3, 6, 5],
        [5, 3, 1, 6, 4, 2, 9, 7, 8],
        [6, 4, 2, 9, 7, 8, 5, 3, 1],
        [9, 7, 8, 5, 3, 1, 6, 4, 2] # Last cell will cause conflict
    ]
    print("\n--- Original Puzzle 2 (No Solution Expected) ---")
    print_board(puzzle2)
    print("\nSolving...\n")
    if solve_sudoku(puzzle2):
        print("--- Solved Puzzle 2 ---")
        print_board(puzzle2)
    else:
        print("No solution found for Puzzle 2 (as expected).")