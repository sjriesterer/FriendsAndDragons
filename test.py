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

obstacles = ['O']
empty_square = '.'

# Function to parse the input board
def parse_input(input):
    return [list(row) for row in input]

# Function to check if a point is a chokepoint
def is_chokepoint(board, row, col):
    rows, cols = len(board), len(board[0])

    # Ensure the current cell is an empty square
    if board[row][col] != empty_square:
        return False

    # Check for obstacles on both sides (left and right)
    if col > 0 and col < cols - 1 and board[row][col - 1] in obstacles and board[row][col + 1] in obstacles:
        # Check for empty squares above and below
        if (row == 0 or board[row - 1][col] == empty_square) and (row == rows - 1 or board[row + 1][col] == empty_square):
            return True

    # Check for obstacles above and below
    if row > 0 and row < rows - 1 and board[row - 1][col] in obstacles and board[row + 1][col] in obstacles:
        # Check for empty squares left and right
        if (col == 0 or board[row][col - 1] == empty_square) and (col == cols - 1 or board[row][col + 1] == empty_square):
            return True

    # Check if the current cell is an empty square and is located at the edge of the board
    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
        # Check for corners
        if (row == 0 and col == 0) or (row == 0 and col == cols - 1) \
                or (row == rows - 1 and col == 0) or (row == rows - 1 and col == cols - 1):
            return True

        # Check for edges
        if row == 0 and col > 0 and col < cols - 1 and board[row + 1][col] in obstacles:
            return True
        if row == rows - 1 and col > 0 and col < cols - 1 and board[row - 1][col] in obstacles:
            return True
        if col == 0 and row > 0 and row < rows - 1 and board[row][col + 1] in obstacles:
            return True
        if col == cols - 1 and row > 0 and row < rows - 1 and board[row][col - 1] in obstacles:
            return True

    # Check for corners when the cell is not on an edge
    if row > 0 and row < rows - 1 and col > 0 and col < cols - 1:
        if board[row - 1][col - 1] in obstacles and board[row - 1][col + 1] in obstacles \
                and board[row + 1][col - 1] in obstacles and board[row + 1][col + 1] in obstacles:
            return True

    return False

# Function to find all chokepoints on the board
def find_chokepoints(board):
    chokepoints = []
    for row in range(len(board)):
        for col in range(len(board[0])):
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
