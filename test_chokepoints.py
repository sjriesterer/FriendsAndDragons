# Define the input board and obstacles
board = [
    "..OOOO",
    "OOO.O.",
    ".O...O",
    "OO.OOO",
    "OO....",
    "......",
    "OOO...",
    "......"
]

obstacle = 'O'
empty_square = '.'

# Function to parse the input board
def parse_input(input):
    return [list(row) for row in input]

# Function to check if a point is within the bounds of the board
def within_bounds(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

# Function to check if a point is a chokepoint
def is_chokepoint(board, row, col):
    rows, cols = len(board), len(board[0])

    # Ensure the current cell is an empty square
    if board[row][col] != empty_square:
        return False

    # Define the conditions for different types of chokepoints
    conditions = [
        # Top left corner
        (row == 0 and col == 0 and within_bounds(row + 1, col, rows, cols) and within_bounds(row, col + 1, rows, cols) and
         board[row][col + 1] == obstacle and board[row + 1][col] == empty_square),
        (row == 0 and col == 0 and within_bounds(row + 1, col, rows, cols) and within_bounds(row, col + 1, rows, cols) and
         board[row][col + 1] == empty_square and board[row + 1][col] == obstacle),
        # Top right corner
        (row == 0 and col == cols - 1 and within_bounds(row + 1, col, rows, cols) and within_bounds(row, col - 1, rows, cols) and
         board[row][col - 1] == obstacle and board[row + 1][col] == empty_square),
        (row == 0 and col == cols - 1 and within_bounds(row + 1, col, rows, cols) and within_bounds(row, col - 1, rows, cols) and
         board[row][col - 1] == empty_square and board[row + 1][col] == obstacle),
        # Bottom left corner
        (row == rows - 1 and col == 0 and within_bounds(row - 1, col, rows, cols) and within_bounds(row, col + 1, rows, cols) and
         board[row][col + 1] == obstacle and board[row - 1][col] == empty_square),
        (row == rows - 1 and col == 0 and within_bounds(row - 1, col, rows, cols) and within_bounds(row, col + 1, rows, cols) and
         board[row][col + 1] == empty_square and board[row - 1][col] == obstacle),
        # Bottom right corner
        (row == rows - 1 and col == cols - 1 and within_bounds(row - 1, col, rows, cols) and within_bounds(row, col - 1, rows, cols) and
         board[row][col - 1] == obstacle and board[row - 1][col] == empty_square),
        (row == rows - 1 and col == cols - 1 and within_bounds(row - 1, col, rows, cols) and within_bounds(row, col - 1, rows, cols) and
         board[row][col - 1] == empty_square and board[row - 1][col] == obstacle),
        # Edges
        (row == 0 and within_bounds(row + 1, col, rows, cols) and board[row + 1][col] == obstacle and
         (col == 0 or col == cols - 1) and board[row][col - 1] == empty_square and board[row][col + 1] == empty_square),
        (row == rows - 1 and within_bounds(row - 1, col, rows, cols) and board[row - 1][col] == obstacle and
         (col == 0 or col == cols - 1) and board[row][col - 1] == empty_square and board[row][col + 1] == empty_square),
        (col == 0 and within_bounds(row, col + 1, rows, cols) and board[row][col + 1] == obstacle and
         (row == 0 or row == rows - 1) and board[row - 1][col] == empty_square and board[row + 1][col] == empty_square),
        (col == cols - 1 and within_bounds(row, col - 1, rows, cols) and board[row][col - 1] == obstacle and
         (row == 0 or row == rows - 1) and board[row - 1][col] == empty_square and board[row + 1][col] == empty_square),
        # Middle
        (within_bounds(row + 1, col, rows, cols) and within_bounds(row - 1, col, rows, cols) and
         within_bounds(row, col + 1, rows, cols) and within_bounds(row, col - 1, rows, cols) and
         (board[row + 1][col] == obstacle or board[row - 1][col] == obstacle) and
         (board[row][col + 1] == obstacle or board[row][col - 1] == obstacle))
    ]

    print("row: ", row, "; col: ", col, " Conditions:")
    print(conditions)

    # Check if any of the conditions are met
    return any(conditions)

# Function to find all chokepoints on the board
def find_chokepoints(board):
    chokepoints = []
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            if is_chokepoint(board, row, col):
                chokepoints.append((row, col))
    return chokepoints

# Parse the board and find chokepoints
board_terrain = parse_input(board)
chokepoints = find_chokepoints(board_terrain)

# Print the chokepoints
print("Chokepoints found at:")
for chokepoint in chokepoints:
    print(chokepoint)
