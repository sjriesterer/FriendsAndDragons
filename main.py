# Author: Samuel Riesterer
# Date: 6/1/24
# Titles: Friends & Dragons Planning

# ================================================================================
# IMPORTS
# ================================================================================
import sys
from modules import *

sys.path.append('/modules')

# ================================================================================
# INPUTS
# ================================================================================

terrain = [
    "..o...",
    "ooo...",
    ".....l",
    "oo..ll",
    ".....i",
    ".....i",
    "www...",
    "......"
]

positions = [
    "...aaa",
    "....a.",
    ".a...b",
    "...bbb",
    "aa....",
    "......",
    "......",
    "123456"
]

heros = [
    "monk", "knight", "mage", "rogue", "hunter", "pirate"
]
# ================================================================================
# GLOBALS
# ================================================================================

# GLOBALS

# board terrain legend
lava = 'L'
water = 'W'
rubble = 'R'
ice = 'I'
obstacle = 'O'
empty_square = '.'
monster = 'M'

# Monsters
monster1 = 'A'
monster2 = 'B'
monster3 = 'C'
monster4 = 'D'

obstacles = [lava, water, rubble, obstacle]
monsters = [monster1, monster2, monster3, monster4]

# class legend
monk = ''
barbarian = ''
assassin = ''
rouge = ''
pirate = ''
knight = ''
warrior = ''
guardian = ''
ranger = ''
archer = ''
hunter = ''
jav = ''
mage = ''
elemental = ''
warlock = ''
wizard = ''
healer = ''
paladin = ''
druid = ''
bard = ''
princess = ''


# ================================================================================
# METHODS
# ================================================================================
# Function to check if a point is within the bounds of the board
def within_bounds(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

def is_valid_position(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

# ================================================================================
def is_valid_point(board, point):
    return 0 <= point[0] < len(board) and 0 <= point[1] < len(board[0])

# ================================================================================
def is_valid_move(board, visited, row, col, designated_point):
    rows = len(board)
    cols = len(board[0])
    return (0 <= row < rows and 0 <= col < cols and
            board[row][col] != 'O' and not visited[row][col] and
            (row, col) != designated_point)

# ================================================================================
# Checks if the chokepoint is a deadend by finding all paths from one end of the chokepoint to the other
# if the only path is through the chockpoint, then it is a deadend
def is_deadend(board, chokepoint):
    row, col = chokepoint
    up = (row, col-1)
    down = (row, col+1)
    right = (row+1, col)
    left = (row-1, col)
    check_up_down = False
    check_left_right = False

    # if next to the left or right edges of the map
    if is_valid_point(board, left) is False or is_valid_point(board, right) is False:
        check_up_down = True

    # if next to the top or bottom edges of the map
    elif is_valid_point(board, up) is False or is_valid_point(board, down) is False:
        check_left_right = True

    elif board[row][col-1] == empty_square:
        check_left_right = True

    elif board[row-1][col] == empty_square:
        check_up_down = True

    else:
        return False
           
    if check_up_down is True:
        start = (row, col-1)
        end = (row, col+1)
    else:
        start = (row-1, col)
        end = (row+1, col)

    return not does_path_exist(board, start, end, chokepoint)

# ================================================================================
def is_dead_end_corner(board, row, col, deadends, chokepoints):
    if (0, 0) in chokepoints and (0, 1) in deadends:
        deadends.append((0,0))
    if (0, len(board[0]) - 1) in chokepoints and (0, len(board[0] - 2)) in deadends:
        deadends.append((0, len(board[0]) - 1))
    if (len(board) -1, 0) in chokepoints and (len(board) - 2, 0) in deadends:
        deadends.append((len(board) -1, 0))
    if (len(board) -1, len(board[0]) - 1) in chokepoints and (len(board) - 2, len(board[0]) - 2) in deadends:
        deadends.append((len(board) -1, len(board[0]) - 1))
    return deadends
# ================================================================================
# true if a path exists on the board from start to end not passing through the designated_point
def does_path_exist(board, start, end, designated_point):
    rows = len(board)
    cols = len(board[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    def backtrack(row, col):
        if (row, col) == end:
            return True
        visited[row][col] = True
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(board, visited, new_row, new_col, designated_point):
                if backtrack(new_row, new_col):
                    return True
                
        visited[row][col] = False
        return False
    
    start_row, start_col = start
    return backtrack(start_row, start_col)

# ================================================================================
# gets all paths from start to end on the board not passing through the designated_point
def get_paths(board, start, end, designated_point):
    rows = len(board)
    cols = len(board[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    paths = []
    
    def backtrack(row, col, path):
        if (row, col) == end:
            paths.append(path)
            return
        visited[row][col] = True
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(board, visited, new_row, new_col, designated_point):
                backtrack(new_row, new_col, path + [(new_row, new_col)])
                
        visited[row][col] = False
    
    start_row, start_col = start
    backtrack(start_row, start_col, [start])
    return paths

# region square checks
# ================================================================================
def empty_square_left(board, row, col):
    return board[row][col-1] == empty_square
def empty_square_right(board, row, col):
    return board[row][col+1] == empty_square
def empty_square_above(board, row, col):
    return board[row-1][col] == empty_square
def empty_square_below(board, row, col):
    return board[row+1][col] == empty_square
def empty_square_left_right(board, row, col):
    return empty_square_left(board, row, col) and empty_square_right(board, row, col)
def empty_square_above_below(board, row, col):
    return empty_square_above(board, row, col) and empty_square_below(board, row, col)
# ================================================================================
def obstacle_left(board, row, col):
    return board[row][col-1] == obstacle
def obstacle_right(board, row, col):
    return board[row][col+1] == obstacle
def obstacle_above(board, row, col):
    return board[row-1][col] == obstacle
def obstacle_below(board, row, col):
    return board[row+1][col] == obstacle
def obstacle_left_right(board, row, col):
    return obstacle_left(board, row, col) and obstacle_right(board, row, col)
def obstacle_above_below(board, row, col):
    return obstacle_above(board, row, col) and obstacle_below(board, row, col)
# ================================================================================
def edge_left(board, row, col):
    return col == 0
def edge_right(board, row, col):
    return col == len(board[0]) - 1
def edge_above(board, row, col):
    return row == 0
def edge_below(board, row, col):
    return row == len(board) - 1
# ================================================================================
def is_top_left_corner(board, row, col):
    return (row == 0 and col == 0)
def is_top_right_corner(board, row, col):
    return (row == 0 and col == len(board[0]) -1)
def is_bottom_left_corner(board, row, col):
    return (row == len(board) - 1 and col == 0)
def is_bottom_right_corner(board, row, col):
    return (row == len(board) - 1 and col == len(board[0]) - 1)
# ================================================================================
def is_in_middle(board, row, col):
    return 0 < row < len(board) - 1 and 0 < col < len(board[0]) - 1
# endregion

# ================================================================================
# Checks if the point is a chokepoint
def is_chokepoint(board, row, col):
    # Ensure the current cell is an empty square
    if board[row][col] != empty_square:
        return False

    # Define the conditions for different types of chokepoints
    return (
        (is_top_left_corner(board, row, col) and 
            ((obstacle_below(board, row, col) and empty_square_right(board, row, col)) or (obstacle_right(board, row, col) and empty_square_below(board, row, col)))) or # Top left corner
        (is_top_right_corner(board, row, col) and 
            ((obstacle_below(board, row, col) and empty_square_left(board, row, col)) or (obstacle_left(board, row, col) and empty_square_below(board, row, col)))) or # To right corner
        (is_bottom_left_corner(board, row, col) and 
            ((obstacle_above(board, row, col) and empty_square_right(board, row, col)) or (obstacle_right(board, row, col) and empty_square_above(board, row, col)))) or # Bottom left corner
        (is_bottom_right_corner(board, row, col) and 
            ((obstacle_above(board, row, col) and empty_square_left(board, row, col)) or (obstacle_left(board, row, col) and empty_square_above(board, row, col)))) or # Bottom right corner
        (edge_above(board, row, col) and 
            ((obstacle_left_right(board, row, col) and empty_square_below(board, row, col)) or (obstacle_below(board,row,col) and (empty_square_left(board, row,col) or empty_square_right(board, row, col))))) or  # Above Edge
        (edge_below(board, row, col) and 
            ((obstacle_left_right(board, row, col) and empty_square_above(board, row, col)) or (obstacle_above(board,row,col) and (empty_square_left(board, row,col) or empty_square_right(board, row, col))))) or  # Below Edge
        (edge_left(board, row, col) and 
            ((obstacle_above_below(board,row,col) and empty_square_right(board, row,col)) or (obstacle_right(board, row, col) and (empty_square_above(board, row, col) or empty_square_below(board, row, col))))) or  # Left Edge
        (edge_right(board, row, col) and 
            ((obstacle_above_below(board,row,col) and empty_square_left(board, row,col)) or (obstacle_left(board, row, col) and (empty_square_above(board, row, col) or empty_square_below(board, row, col))))) or  # Right Edge
        (is_in_middle(board, row, col) and (
            (obstacle_above_below(board, row, col) and (empty_square_left(board, row, col) or empty_square_right(board, row, col))) or
            (obstacle_left_right(board, row, col) and (empty_square_above(board, row, col) or empty_square_below(board, row, col))) # Middle
        ))
    )

# ================================================================================
def find_chokepoints(board):
    chokepoints = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_chokepoint(board, row, col):
                chokepoints.append((row, col))
    return chokepoints

# ================================================================================
def find_deadends(board, chokepoints):
    barriers = []
    for chokepoint in chokepoints:
        if is_deadend(board, chokepoint):
            barriers.append(chokepoint)
    return barriers

# ================================================================================
def print_board(board):
    # Print column numbers
    print('    ', end='')
    for col in range(len(board[0])):
        print(f'{col:2}', end='')
    print()
    print(" ----------------")

    # Print board rows with row numbers
    for i, row in enumerate(board):
        print(f'{i:2} | ', end='')
        print(' '.join(row))

# ================================================================================
    # Use a list comprehension to convert each string into a list of characters
def parse_input(input):
    board = [list(row) for row in input]
    return board

# ================================================================================
# Remove spaces and convert to uppercase
def format_input(input):
    new_input = []
    for item in input:
        new_input.append(item.upper().replace(' ', ''))
    return new_input

# ================================================================================
#
def validate_inputs():
    #TODO
    return True

# ================================================================================
def get_obstacle_board(board_terrain, board_pos):
    # Determine the size of the boards
    rows = len(board_terrain)
    cols = len(board_terrain[0])
    
    # Create an empty board for the final output
    final_board = [[empty_square for _ in range(cols)] for _ in range(rows)]
    
    # Iterate through each position in the boards
    for i in range(rows):
        for j in range(cols):
            # Check if the terrain board has an obstacle
            if board_terrain[i][j] in obstacles:
                final_board[i][j] = obstacle
            # Check if the position board has a monster character
            elif board_pos[i][j] in monsters:
                final_board[i][j] = obstacle
            # Otherwise, keep the square empty
            else:
                final_board[i][j] = empty_square
    
    return final_board
# ================================================================================
# SCRIPT
# ================================================================================

if validate_inputs is False:
    pass
else:

    board_terrain = parse_input(format_input(terrain))
    board_pos = parse_input(format_input(positions))
    board_obstacles = get_obstacle_board(board_terrain, board_pos)

    print("\nTerrain:")
    print_board(board_terrain)
    print("\nPositions:")
    print_board(board_pos)
    print("\nObstacles:")
    print_board(board_obstacles)

    chokepoints = find_chokepoints(board_obstacles)
    deadends = find_deadends(board_obstacles, chokepoints)
    print("\nchokepoints: ", chokepoints)
    print("deadends: ", deadends)
    # print("Board:")
    # print_board(board, chokepoints, deadends)

    # monk: MyHero = MyHero(name="monk")
    # print(monk)

