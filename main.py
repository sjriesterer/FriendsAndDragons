import sys

sys.path.append('/modules')


# GLOBALS

# board terrain legend
lava = 'L'
water = 'W'
rubble = 'R'
ice = 'I'
obstacle = 'O'
empty = '.'

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

# monster legend

monster = 'M'

def is_valid_position(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def is_valid_point(board, point):
    return 0 <= point[0] < len(board) and 0 <= point[1] < len(board[0])

def is_valid_move(board, visited, row, col, designated_point):
    rows = len(board)
    cols = len(board[0])
    return (0 <= row < rows and 0 <= col < cols and
            board[row][col] != 'O' and not visited[row][col] and
            (row, col) != designated_point)

# true if the chokepoint is a dead_end
# A dead_end only allows one hero through to the other side
def is_barrier(board, chokepoint):
    row, col = chokepoint
    left = (row, col-1)
    right = (row, col+1)
    down = (row+1, col)
    up = (row-1, col)
    check_up_down = False
    check_left_right = False

    # print("cp: ", chokepoint, "; row=", row, ", col=", col)

    if is_valid_point(board, left) is False or is_valid_point(board, right) is False:
        # print("edgeLR: check_row true")
        check_up_down = True

    elif is_valid_point(board, up) is False or is_valid_point(board, down) is False:
        # print("edgeUD: check_col true")
        check_left_right = True

    elif board[row][col-1] == ' ':
        # print("check_row true")
        check_left_right = True

    elif board[row-1][col] == ' ':
        # print("check_col true")
        check_up_down = True

    else:
        return False
           
    if check_up_down is True:
        start = (row-1, col)
        end = (row+1, col)
    else:
        start = (row, col-1)
        end = (row, col+1)

    # print("start: ", start, ", end: ", end)

    return not does_path_exist(board, start, end, chokepoint)

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

# true if the point is a chokepoint
# a chokepoint has only one square between obstacles (or edges)
def is_chokepoint(board, row, col):
    if board[row][col] != ' ':
        return False
    
    # Check for obstacle on both sides
    if (col > 0 and board[row][col - 1] == 'O') and (col < len(board[0]) - 1 and board[row][col + 1] == 'O'):
        # Check for empty squares above and below
        if row > 0 and row < len(board) - 1 and board[row - 1][col] == ' ' and board[row + 1][col] == ' ':
            return True
    # Check for obstacle above and below
    if (row > 0 and board[row - 1][col] == 'O') and (row < len(board) - 1 and board[row + 1][col] == 'O'):
        # Check for empty squares left and right
        if col > 0 and col < len(board[0]) - 1 and board[row][col - 1] == ' ' and board[row][col + 1] == ' ':
            return True
    # Check for edge case
    if (row == 0 or row == len(board) - 1 or col == 0 or col == len(board[0]) - 1) and board[row][col] == ' ':
        if (col == 0 or col == len(board[0]) - 1) and row > 0 and row < len(board) - 1:
            if (col == 0 and board[row][col + 1] == 'O' and board[row - 1][col] == ' ' and board[row + 1][col] == ' ') \
                    or (col == len(board[0]) - 1 and board[row][col - 1] == 'O' and board[row - 1][col] == ' ' and board[row + 1][col] == ' '):
                return True
        elif (row == 0 or row == len(board) - 1) and col > 0 and col < len(board[0]) - 1:
            if (row == 0 and board[row + 1][col] == 'O' and board[row][col - 1] == ' ' and board[row][col + 1] == ' ') \
                    or (row == len(board) - 1 and board[row - 1][col] == 'O' and board[row][col - 1] == ' ' and board[row][col + 1] == ' '):
                return True
    return False

def find_chokepoints(board):
    chokepoints = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_chokepoint(board, row, col):
                chokepoints.append((row, col))
    return chokepoints

def find_deadends(board, chokepoints):
    barriers = []
    for chokepoint in chokepoints:
        if is_barrier(board, chokepoint):
            barriers.append(chokepoint)
    return barriers

def print_board(board, chokepoints, barriers):
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == 'O':
                print('O', end='')
            elif (row_idx, col_idx) in barriers:
                print('b', end='')
            else:
                print('.', end='')
        print()

# Example usage
board = [
    [' ', ' ', ' ', 'O', ' ', ' ', 'O', ' '],
    ['O', ' ', 'O', ' ', ' ', ' ', ' ', 'O'],
    [' ', ' ', ' ', ' ', 'O', ' ', ' ', ' '],
    [' ', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    [' ', ' ', ' ', ' ', 'O', ' ', ' ', ' '],
    ['O', ' ', 'O', ' ', ' ', ' ', 'O', ' ']
]

terrain = [
    "..b...",
    "bbb...",
    ".....l",
    "....ll",
    ".....i",
    ".....i",
    "www..."
]

chokepoints = find_chokepoints(board)
deadends = find_deadends(board, chokepoints)
print("chokepoints: ", chokepoints)
print("deadends: ", deadends)
print("Board:")
print_board(board, chokepoints, deadends)
