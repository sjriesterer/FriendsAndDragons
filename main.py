# Author: Samuel Riesterer
# Date: 6/1/24
# Titles: Friends & Dragons Planning

# =================================================================================================
# IMPORTS
# =================================================================================================
import sys
from modules.hero import Hero

from enums import *
from inputs import Inputs
from logger import log

sys.path.append('/modules')

# =================================================================================================
# INPUTS
# =================================================================================================

inputs = Inputs()
terrain = inputs.terrain
positions = inputs.positions
hero_inputs = inputs.heroes

# =================================================================================================
# GLOBALS
# =================================================================================================

obstacle_codes = [Board.lava, Board.obstacle, Board.rubble, Board.water, Board.monster]
obstacle_codes_lava = [Board.obstacle, Board.rubble, Board.water, Board.monster]
obstacle_codes_water = [Board.lava, Board.obstacle, Board.rubble, Board.monster] 
obstacle_codes_flying = [Board.obstacle, Board.monster]
obstacle_codes_rubble = [Board.lava, Board.obstacle, Board.water, Board.monster]
obstacles = [char.value for char in obstacle_codes]
obstacles_lava = [char.value for char in obstacle_codes_lava]
obstacles_water = [char.value for char in obstacle_codes_water]
obstacles_flying = [char.value for char in obstacle_codes_flying]
obstacles_rubble = [char.value for char in obstacle_codes_rubble]

monster_codes = [Monsters.monster1, Monsters.monster2, Monsters.monster3, Monsters.monster4]
monsters = [char.value for char in monster_codes]

lava = 'L'
water = 'W'
rubble = 'R'
ice = 'I'
obstacle = 'O'
empty_square = '.'
monster = 'M'

# =================================================================================================
# CLASSES
# =================================================================================================
class Zone:
    def __init__(self, section, id, is_deadend=False):
        self.section = section
        self.id = id
        self.is_deadend = is_deadend
        self.points = []
        self.connected_zones = []
        self.connected_deadend_zones = []
    def __str__(self):
        return f'{self.id} : Section: {self.section}, Deadend: {self.is_deadend}, Connected: {self.connected_zones}, Deadends: {self.connected_deadend_zones}\n\tPoints: {self.points}'

class Allowable_Points:
    def __init__(self):
        self.section = 0
        self.main_path_id = 0
        self.main_path = []
        self.alt_path_id = None
        self.alt_path = []
        self.zone_id = 0
        self.points = []

# =================================================================================================
# INIT METHODS
# =================================================================================================
# Use a list comprehension to convert each string into a list of characters
def parse_input(input):
    board = [list(row) for row in input]
    return board

# =================================================================================================
# Remove spaces and convert to uppercase
def format_input(input):
    new_input = []
    for item in input:
        new_input.append(item.upper().replace(' ', ''))
    return new_input

# =================================================================================================
# VALIDATION METHODS
# =================================================================================================
# Function to check if a point is within the bounds of the board
def within_bounds(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

def is_valid_position(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

# =================================================================================================
def is_valid_point(board, point):
    return 0 <= point[0] < len(board) and 0 <= point[1] < len(board[0])

# =================================================================================================
def is_valid_move(board, visited, row, col, designated_point):
    rows = len(board)
    cols = len(board[0])
    return (0 <= row < rows and 0 <= col < cols and
            board[row][col] != 'O' and not visited[row][col] and
            (row, col) != designated_point)
# =================================================================================================
#
def validate_inputs():
    #TODO
    return True

# =================================================================================================
# SQUARE CHECK METHODS
# =================================================================================================
# region SQUARE CHECKS
# =================================================================================================
# Specific check
def square_is(board, row, col, type):
    return board[row][col] == type
def square_is_empty(board, row, col):
    return board[row][col] == empty_square
def square_is_obstacle(board, row, col):
    return board[row][col] == obstacle
# =================================================================================================
# Diagnoal obstacles check
def obstacle_above_left(board, row, col):
    return board[row-1][col-1] == obstacle
def obstacle_above_right(board, row, col):
    return board[row-1][col+1] == obstacle
def obstacle_below_left(board, row, col):
    return board[row+1][col-1] == obstacle
def obstacle_below_right(board, row, col):
    return board[row+1][col+1] == obstacle
# =================================================================================================
# Empty squares check
def empty_square_left(board, row, col):
    return board[row][col-1] == empty_square
def empty_square_right(board, row, col):
    return board[row][col+1] == empty_square
def empty_square_above(board, row, col):
    return board[row-1][col] == empty_square
def empty_square_below(board, row, col):
    return board[row+1][col] == empty_square
def empty_square_left_and_right(board, row, col):
    return empty_square_left(board, row, col) and empty_square_right(board, row, col)
def empty_square_above_and_below(board, row, col):
    return empty_square_above(board, row, col) and empty_square_below(board, row, col)
# =================================================================================================
# Obstacles check
def obstacle_left(board, row, col):
    return board[row][col-1] == obstacle
def obstacle_right(board, row, col):
    return board[row][col+1] == obstacle
def obstacle_above(board, row, col):
    return board[row-1][col] == obstacle
def obstacle_below(board, row, col):
    return board[row+1][col] == obstacle
def obstacle_left_and_right(board, row, col):
    return obstacle_left(board, row, col) and obstacle_right(board, row, col)
def obstacle_above_and_below(board, row, col):
    return obstacle_above(board, row, col) and obstacle_below(board, row, col)
# =================================================================================================
# Edges check
def edge_left(board, row, col):
    return col == 0
def edge_right(board, row, col):
    return col == len(board[0]) - 1
def edge_above(board, row, col):
    return row == 0
def edge_below(board, row, col):
    return row == len(board) - 1
# =================================================================================================
# Corners check
def is_top_left_corner(board, row, col):
    return (row == 0 and col == 0)
def is_top_right_corner(board, row, col):
    return (row == 0 and col == len(board[0]) -1)
def is_bottom_left_corner(board, row, col):
    return (row == len(board) - 1 and col == 0)
def is_bottom_right_corner(board, row, col):
    return (row == len(board) - 1 and col == len(board[0]) - 1)
# =================================================================================================
# Middle check
def is_in_middle(board, row, col):
    return 0 < row < len(board) - 1 and 0 < col < len(board[0]) - 1
# endregion

# =================================================================================================
# PATH & BOARD METHODS
# =================================================================================================
# Checks if the chokepoint is a deadend 
def is_deadend(board, chokepoints, chokepoint):
    row, col = chokepoint
    left = (row, col-1)
    right = (row, col+1)
    above = (row-1, col)
    below = (row+1, col)
    start = (0,0)
    end = (0,0)

    log(f"\nchecking deadends for point {chokepoint}")

    if is_in_middle(board, row, col):
        # If chokepoint is in the middle surrounded by empty_squares, need to evaulate paths 
        if empty_square_left_and_right(board, row, col):
            log("middle empty LR")
            start = left
            end = right
        elif empty_square_above_and_below(board, row, col):
            log("middle empty ab")
            start = above
            end = below
        # Chokepoints surrounded by 3 obstacles are deadends only if burried 2 or more squares deep
        elif obstacle_above_and_below(board, row, col):
            if obstacle_left(board, row, col) and obstacle_above_right(board, row, col) and obstacle_below_right(board, row, col):
                log("middle 1")
                return True
            elif obstacle_right(board, row, col) and obstacle_above_left(board, row, col) and obstacle_below_left(board, row, col):
                log("middle 2")
                return True
        elif obstacle_left_and_right(board, row, col) :
            if obstacle_above(board, row, col) and obstacle_below_left(board, row, col) and obstacle_below_right(board, row, col):
                log("middle 3")
                return True
            elif obstacle_below(board, row, col) and obstacle_above_left(board, row, col) and obstacle_above_right(board, row, col):
                log("middle 4")
                return True
    # Corners are only deadends if burried with 2 or more obstacles
    elif is_top_left_corner(board, row, col):
        if (obstacle_below(board, row, col) or obstacle_right(board, row, col)) and obstacle_below_right(board, row, col):
            log("TL corner")
            return True
    elif is_top_right_corner(board, row, col):
        if (obstacle_below(board, row, col) or obstacle_left(board, row, col)) and obstacle_below_left(board, row, col):
            log("TR corner")
            return True
    elif is_bottom_left_corner(board, row, col):
        if (obstacle_above(board, row, col) or obstacle_right(board, row, col)) and obstacle_above_right(board, row, col):
            log("BL corner")
            return True
    elif is_bottom_right_corner(board, row, col):
        if (obstacle_above(board, row, col) or obstacle_left(board, row, col)) and obstacle_above_left(board, row, col):
            log("BR corner")
            return True
    # Edge chokepoints surrounded by empty sqaures need to evaluate paths
    elif (edge_above(board, row, col) or edge_below(board, row, col)) and empty_square_left_and_right(board, row, col):
            log("Edge A or B")
            start = left
            end = right
    elif (edge_left(board, row, col) or edge_right(board, row, col)) and empty_square_above_and_below(board, row, col):
            log("Edge L or R")
            start = above
            end = below
    # Edge chokepoints 
    elif edge_left(board, row, col):
        if obstacle_above_and_below(board, row, col) and obstacle_above_right(board, row, col) and obstacle_below_right(board, row, col):
            log("Edge L 1")
            return True
        elif obstacle_above(board, row, col) and obstacle_right(board, row, col) and obstacle_below_right(board, row, col):
            log("Edge L 2")
            return True
        elif obstacle_below(board, row, col) and obstacle_right(board, row, col) and obstacle_above_right(board, row, col):
            log("Edge L 3")
            return True
    elif edge_right(board, row, col):
        if obstacle_above_and_below(board, row, col) and obstacle_above_left(board, row, col) and obstacle_below_left(board, row, col):
            log("Edge R 1")
            return True
        elif obstacle_above(board, row, col) and obstacle_left(board, row, col) and obstacle_below_left(board, row, col):
            log("Edge R 2")
            return True
        elif obstacle_below(board, row, col) and obstacle_left(board, row, col) and obstacle_above_left(board, row, col):
            log("Edge R 3")
            return True
    elif edge_above(board, row, col):
        if obstacle_left_and_right(board, row, col) and obstacle_below_left(board, row, col) and obstacle_below_right(board, row, col):
            log("Edge A 1")
            return True
        elif obstacle_left(board, row, col) and obstacle_below(board, row, col) and obstacle_below_right(board, row, col):
            log("Edge A 2")
            return True
        elif obstacle_right(board, row, col) and obstacle_below(board, row, col) and obstacle_below_left(board, row, col):
            log("Edge A 3")
            return True
    elif edge_below(board, row, col):
        if obstacle_left_and_right(board, row, col) and obstacle_below_left(board, row, col) and obstacle_above_left(board, row, col):
            log("Edge B 1")
            return True
        elif obstacle_left(board, row, col) and obstacle_above(board, row, col) and obstacle_above_right(board, row, col):
            log("Edge B 2")
            return True
        elif obstacle_right(board, row, col) and obstacle_above(board, row, col) and obstacle_above_left(board, row, col):
            log("Edge B 3")
            return True
    
    log(f"finding path from {start} to {end}")

    return not does_path_exist(board, start, end, chokepoint)

# =================================================================================================
# True if point1 is cardinally adjacent to point2
def is_cardinally_adjacent(point1, point2):
    return (abs(point1[0] - point2[0]) == 1 and point1[1] == point2[1]) or (abs(point1[1] - point2[1]) == 1 and point1[0] == point2[0])

# =================================================================================================
# True if a path exists on the board from start to end and not passing through the chokepoint
def does_path_exist(board, start, end, chokepoint):
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
            if is_valid_move(board, visited, new_row, new_col, chokepoint):
                if backtrack(new_row, new_col):
                    return True
                
        visited[row][col] = False
        return False
    
    start_row, start_col = start
    return backtrack(start_row, start_col)

# =================================================================================================
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
            ((obstacle_left_and_right(board, row, col) and empty_square_below(board, row, col)) or (obstacle_below(board,row,col) and (empty_square_left(board, row,col) or empty_square_right(board, row, col))))) or  # Above Edge
        (edge_below(board, row, col) and 
            ((obstacle_left_and_right(board, row, col) and empty_square_above(board, row, col)) or (obstacle_above(board,row,col) and (empty_square_left(board, row,col) or empty_square_right(board, row, col))))) or  # Below Edge
        (edge_left(board, row, col) and 
            ((obstacle_above_and_below(board,row,col) and empty_square_right(board, row,col)) or (obstacle_right(board, row, col) and (empty_square_above(board, row, col) or empty_square_below(board, row, col))))) or  # Left Edge
        (edge_right(board, row, col) and 
            ((obstacle_above_and_below(board,row,col) and empty_square_left(board, row,col)) or (obstacle_left(board, row, col) and (empty_square_above(board, row, col) or empty_square_below(board, row, col))))) or  # Right Edge
        (is_in_middle(board, row, col) and (
            (obstacle_above_and_below(board, row, col) and (empty_square_left(board, row, col) or empty_square_right(board, row, col))) or
            (obstacle_left_and_right(board, row, col) and (empty_square_above(board, row, col) or empty_square_below(board, row, col))) # Middle
        ))
    )

# =================================================================================================
# Returns a list of zones based on the board and deadends
def get_zones_of_board(board, deadends):
    rows, cols = len(board), len(board[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    deadends_set = set(deadends)
    visited = set()
    zones_pre = [] # Set of zones before adding connections and sections
    zones = [] # Set of Zone objects
    zone_id = -1
    
    # Breadth first search through board
    def bfs(start):
        queue = [start]
        zone = []
        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited or (r, c) in deadends_set or board[r][c] == 'O':
                continue
            visited.add((r, c))
            zone.append((r, c))
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    queue.append((nr, nc))
        return zone
    
    # Mark what section the zones are in
    def mark_sections(zones):
        section_counter = -1
        visited = set()
        
        def dfs(zone, section_id):
            stack = [zone]
            while stack:
                current_zone = stack.pop()
                if current_zone.id in visited:
                    continue
                visited.add(current_zone.id)
                current_zone.section = section_id
                for connected_zone_id in current_zone.connected_zones:
                    connected_zone = next(z for z in zones if z.id == connected_zone_id)
                    if connected_zone.id not in visited:
                        stack.append(connected_zone)
        
        for zone in zones:
            if zone.id not in visited:
                section_counter += 1
                dfs(zone, section_counter)

    # Get the points in the zones
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == empty_square and (r, c) not in visited:
                if (r, c) in deadends_set:
                    zones_pre.append([(r, c)])  # Add deadend as individual zone
                else:
                    new_zone = bfs((r, c))
                    if new_zone:
                        zones_pre.append(sorted(new_zone))
    
    # Sort the zones based on their top-left coordinate
    zones_pre.sort(key=lambda zone: zone[0] if zone else (rows, cols))
    
    # Marks the is_deaded property of the zone if the zone is a deadend
    for z in zones_pre:
        zone_id = zone_id + 1
        is_a_deadend = False
        if len(z) == 1 and z[0] in deadends:
            is_a_deadend = True
        new_zone = Zone(section = 0, id=zone_id, is_deadend=is_a_deadend)
        new_zone.points = z
        zones.append(new_zone)

    # Assigns the connected_zones property of the zones:
    for i in range(len(zones)):
        for j in range(i + 1, len(zones)):  # Only compare each pair of zones once
            connected = False
            for point1 in zones[i].points:
                for point2 in zones[j].points:
                    if is_cardinally_adjacent(point1, point2):
                        connected = True
                        break
                if connected:
                    break
            if connected:
                zones[i].connected_zones.append(zones[j].id)
                zones[j].connected_zones.append(zones[i].id)

    for z in zones:
        for c in z.connected_zones:
            if zones[c].is_deadend:
                z.connected_deadend_zones.append(c)

    mark_sections(zones)

    return zones

# =================================================================================================
def find_chokepoints(board):
    chokepoints = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_chokepoint(board, row, col):
                chokepoints.append((row, col))
    return chokepoints

# =================================================================================================
# Evaluates both boards and identifies obstacles into one board
def get_obstacle_board(board_terrain, board_pos, obstacles):
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

# =================================================================================================
def find_deadends(board, chokepoints):
    barriers = []
    for chokepoint in chokepoints:
        if is_deadend(board, chokepoints, chokepoint):
            barriers.append(chokepoint)
    return barriers

# =================================================================================================
# PRINT METHODS
# =================================================================================================
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

# =================================================================================================
# HERO METHODS
# =================================================================================================
# Returns the point of the hero id on the board
def get_hero_pos(board, hero_id):
    id_str = str(hero_id)
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == id_str:
                return (row_index, col_index)
    return None  # Return None if the id is not found

# =================================================================================================
# 
def init_heroes():
    heroes = []
    id = 0
    for hero in hero_inputs:
        h = get_hero(hero)
        h.id = id
        h.starting_point = get_hero_pos(positions, id)
        h.current_point = h.starting_point
        heroes.append(h)
        id = id + 1
    return heroes

# =================================================================================================
def get_hero(hero_name):
    name = hero_name.lower()
    # melee4_heroes = ['assassin', 'knight']
    # melee8_heroes = ['monk', 'rouge', 'barbarian']
    # range4_heroes = []
    # range8_heroes = ['ranger']
    # magic4_heroes = ['mage']
    # magic8_heroes = ['elementalist']

    hero = Hero()
    hero.name = hero_name

    if name == 'monk':
        hero.attack_type = 1
    elif name == 'barbarian':
        hero.attack_type = 1
    elif name == 'assassin':
        hero.attack_type = 1
    elif name == 'rouge':
        hero.attack_type = 1
    elif name == 'knight':
        hero.attack_type = 1
    elif name == 'warrior':
        hero.attack_type = 1
    elif name == 'guardian':
        hero.attack_type = 1
    elif name == 'pirate':
        hero.attack_type = 1
    elif name == 'ranger':
        hero.attack_type = 1
    elif name == 'archer':
        hero.attack_type = 1
    elif name == 'hunter':
        hero.attack_type = 1
    elif name == 'jav':
        hero.attack_type = 1
    elif name == 'mage':
        hero.attack_type = 1
    elif name == 'elemental':
        hero.attack_type = 1
    elif name == 'warlock':
        hero.attack_type = 1
    elif name == 'wizard':
        hero.attack_type = 1
    elif name == 'healer':
        hero.attack_type = 1
    elif name == 'paladin':
        hero.attack_type = 1
    elif name == 'druid':
        hero.attack_type = 1
    elif name == 'bard':
        hero.attack_type = 1
    elif name == 'princess':
        hero.attack_type = 1

    return hero

# =================================================================================================
# LOOP METHODS
# =================================================================================================
class Section():
    paths = []

class Path():
    zones = []

class Zone2():
    maps = []

class Map():
    points = []


def init_master_list():
    main_list: list[Section] = []

    return main_list


# =================================================================================================
# Gets all the sections of a give list of zones
def get_sections_in_zones(zones):
    sections = []
    for z in zones:
        if z.section not in sections:
            sections.append(z.section)
    return sections

# =================================================================================================
# 
def get_all_paths(zones: list[Zone]) -> list[list[int]]:
    def dfs(current_zone, visited):
        visited.append(current_zone.id)
        paths.append(visited.copy())
        for neighbor_id in current_zone.connected_zones:
            if neighbor_id not in visited:
                neighbor_zone = next(z for z in section_zones if z.id == neighbor_id)
                dfs(neighbor_zone, visited)
        visited.pop()

    # Organize zones by sections
    sections = {}
    for zone in zones:
        if zone.section not in sections:
            sections[zone.section] = []
        sections[zone.section].append(zone)
    
    all_paths = []
    
    for section, section_zones in sections.items():
        paths = []
        for zone in section_zones:
            dfs(zone, [])
        all_paths.extend(paths)
    
    return all_paths

# =================================================================================================
# Gets a list of paths between the zones of a section. Every combination is included.
def get_paths_in_section(section: int, zones: list[Zone]) -> list[list[int]]:
    # Helper function to perform DFS and find all paths
    def dfs(current_zone, visited):
        visited.append(current_zone.id)
        paths.append(visited.copy())
        for neighbor_id in current_zone.connected_zones:
            if neighbor_id not in visited:
                neighbor_zone = next(z for z in zones if z.id == neighbor_id)
                dfs(neighbor_zone, visited)
        visited.pop()

    # Filter zones by the given section
    section_zones = [z for z in zones if z.section == section]

    paths = []
    for zone in section_zones:
        dfs(zone, [])
    return paths

# =================================================================================================
# Gets the path where start_zone is the first and end_zone is the last
def get_path_from_start_to_end(paths: list[list[int]], start_zone: int, end_zone: int) -> list[int] | None:
    for p in paths:
        if p[0] == start_zone and p[-1] == end_zone:
            return p
    return None

# =================================================================================================
# 
def get_path_id(paths, start_zone, end_zone):
    for i in range(len(paths)):
        if paths[i][0] == start_zone and paths[i][len(paths[i])-1] == end_zone:
            return i
    return None  # Return None if no such path is found

# =================================================================================================
# Gets the zone id of the point given
def get_zone_of_pivot(zones: list[Zone], point: tuple) -> Zone | None:
    for zone in zones:
        if point in zone.points:
            return zone
    return None  # Return None if no zone contains the point

# =================================================================================================
# Gets a minimized list of Zone objects of only the section given
def get_zones_in_section(section: int, zones: list[Zone]) -> list[Zone]:
    result = []
    for zone in zones:
        if zone.section == section:
            result.append(zone)
    return result

# =================================================================================================
# 
def get_points_in_zone(zone: int, zones: list[Zone]) -> list[int] | None:
    for z in zones:
        if z.id == zone:
            return z.points
    return None

# =================================================================================================
# Gets a list of all allowable points for a moveable hero who is on the main path of the pivot
# zones = a list of Zone objects for the given board (should only be 1 section)
# main_path = the id of the current main path of the pivot (from pivot start zone to current pivot point)
# start_zone = the starting zone of the movable hero
#TODO needs rigourous testing
def get_points_main(zones: list[Zone], main_path_of_pivot: list[int], hero_start_zone: int):
    allowable_points = []

    points_in_current_zone = get_points_in_zone(hero_start_zone, zones)
    if points_in_current_zone:
        allowable_points.extend(points_in_current_zone)

    # Check if the start_zone is a deadend zone
    if is_deadend_zone(hero_start_zone, zones):
        previous_zone_id = get_previous_zone(hero_start_zone, main_path_of_pivot)
        if hero_start_zone <= 1:
            print(f"main_path: {main_path_of_pivot}, hero start zone: {hero_start_zone}, previous zone id: {previous_zone_id}")
        if previous_zone_id is not None:
            previous_zone = next((z for z in zones if z.id == previous_zone_id), None)
            if hero_start_zone <= 1:
                print(f"previous_zone: {previous_zone}")
            if previous_zone:
                allowable_points.extend(previous_zone.points)
                connected_deadend_zones = get_connected_deadend_zones(previous_zone_id, zones)
                for z_id in connected_deadend_zones:
                    if z_id != hero_start_zone:
                        zone = next((z for z in zones if z.id == z_id), None)
                        if zone:
                            allowable_points.extend(zone.points)
    else:
        current_zone = next((z for z in zones if z.id == hero_start_zone), None)
        if current_zone:
            allowable_points.extend(current_zone.points)
            connected_deadend_zones = get_connected_deadend_zones(hero_start_zone, zones)
            next_deadend_zone_id = get_next_deadend_zone(hero_start_zone, main_path_of_pivot, zones)
            for z_id in connected_deadend_zones:
                if z_id != next_deadend_zone_id:
                    zone = next((z for z in zones if z.id == z_id), None)
                    if zone:
                        allowable_points.extend(zone.points)

    unique_points = remove_duplicates(allowable_points)
    # Sort the resulting list of points by row and then by column
    allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

    return allowable_points

# =================================================================================================
# Gets a list of all allowable points for a moveable hero on an alternate path of the pivot
# zones = a list of Zone objects for the given board (should only be 1 section)
# main_path = the id of the current main path of the pivot (from pivot start zone to current pivot point)
# alt_path = the id of the alternate path of the pivot (from pivot start zone to hero start zone)
# start_zone = the starting zone of the movable hero
#TODO needs rigourous testing
def get_points_alt(zones: list[Zone], main_path_of_pivot: list[int], alt_path_of_pivot: list[int], hero_start_zone: int):
    allowable_points = []  # Allow duplicates

    # current_zone = next((z for z in zones if z.id == hero_start_zone), None)
    # if current_zone:
    #     allowable_points.extend(current_zone.points)

    points_in_current_zone = get_points_in_zone(hero_start_zone, zones)
    if points_in_current_zone:
        allowable_points.extend(points_in_current_zone)

    if is_deadend_zone(hero_start_zone, zones):
        previous_alt_zone_id = get_previous_zone(hero_start_zone, alt_path_of_pivot)
        if previous_alt_zone_id:
            previous_alt_zone = next((z for z in zones if z.id == previous_alt_zone_id), None)
            if previous_alt_zone and not previous_alt_zone.is_deadend:
                allowable_points.extend(previous_alt_zone.points)
                connected_deadend_zones = get_connected_deadend_zones(previous_alt_zone_id, zones)

                if zone_is_on_main_path(previous_alt_zone_id, main_path_of_pivot):
                    unallowable_zone = get_next_deadend_zone(previous_alt_zone_id, main_path_of_pivot, zones)
                else:
                    unallowable_zone = get_previous_deadend_zone(previous_alt_zone_id, alt_path_of_pivot, zones)

                for z_id in connected_deadend_zones:
                    if z_id != unallowable_zone:
                        zone = next((z for z in zones if z.id == z_id), None)
                        if zone:
                            allowable_points.extend(zone.points)
    else:
        connected_deadend_zones = get_connected_deadend_zones(hero_start_zone, zones)
        unallowable_zone = get_previous_deadend_zone(hero_start_zone, alt_path_of_pivot, zones)
        for z_id in connected_deadend_zones:
            if z_id != unallowable_zone:
                zone = next((z for z in zones if z.id == z_id), None)
                if zone:
                    allowable_points.extend(zone.points)

    unique_points = remove_duplicates(allowable_points)
    # Sort the resulting list of points by row and then by column
    allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

    return allowable_points

# =================================================================================================
def remove_duplicates(list):
    return [t for t in (set(tuple(i) for i in list))]

# =================================================================================================
def is_deadend_zone(zone_id, zones):
    for z in zones:
        if z.id == zone_id and z.is_deadend:
            return True
    return False

# =================================================================================================
# Gets the previous zone before the zone_id on the path given
def get_previous_zone(zone_id: int, path: list[int]):
    for p in range(len(path) - 1):
        if zone_id == path[p+1]:
            return p
    return None

# =================================================================================================
def zone_is_on_main_path(zone_id, main_path: list[int]):
    return zone_id in main_path

# =================================================================================================
# Get all connected deadend zones to the zone_id given
def get_connected_deadend_zones(zone_id, zones: list[Zone]):
    connected_deadend_zones = []
    for z in zones:
        if z.id == zone_id:
            for conn_id in z.connected_zones:
                if is_deadend_zone(conn_id, zones):
                    connected_deadend_zones.append(conn_id)
    return connected_deadend_zones

# =================================================================================================
# Returns the previous deadend zone prior to the zone_id on the path of zones given
def get_previous_deadend_zone(zone_id, path: list[Zone], zones: list[Zone]):
    if zone_id in path:
        index_of_zone = path.index(zone_id)
        if index_of_zone <= 0:
            return None
        for i in range(index_of_zone - 1, -1, -1):
            if is_deadend_zone(path[i], zones):
                return path[i]
    return None

# =================================================================================================
# Returns the next deadend zone after the zone_id on the path of zones given
def get_next_deadend_zone(zone_id, path: list[int], zones: list[Zone]):
    if zone_id in path:
        index_of_zone = path.index(zone_id)
        if index_of_zone >= len(path) - 1:
            return None
        for i in range(index_of_zone + 1, len(path)):
            if is_deadend_zone(path[i], zones):
                return path[i]
    return None

# =================================================================================================
# 
def get_allowable_points(all_sections: list[int], all_zones: list[Zone], all_paths: list[list[int]]) -> list[list[list[list[tuple]]]]:
    allowable_points = []

    for s in range(len(all_sections)):
        section_points = []
        zones_in_this_section = get_zones_in_section(all_sections[s], all_zones)
        paths_in_this_section = get_paths_in_section(s, all_zones)
        # print(f"section: {s}, zones in this section: ")
        # for j in zones_in_this_section:
        #     print(j)
        # print("paths in this section: ")
        # for i in paths_in_this_section:
        #     print(i)
        for p in range(len(paths_in_this_section)):
            path_points = []
            path = paths_in_this_section[p]
            pivot_start_zone = path[0]
            pivot_end_zone = path[len(path)-1]

            main_path_id = get_path_id(all_paths, pivot_start_zone, pivot_end_zone)

            for z in range(len(zones_in_this_section)):
                zone_points: Allowable_Points = Allowable_Points()
                zone = zones_in_this_section[z]
                current_zone_id = zone.id

                if current_zone_id in path:
                    points = get_points_main(zones_in_this_section, path, current_zone_id)  # Replace with your logic
                    zone_points.alt_path = None
                    zone_points.alt_path = None
                else:
                    alt_path_id = get_path_id(all_paths, pivot_start_zone, current_zone_id)
                    alt_path = get_path_from_start_to_end(paths_in_this_section, pivot_start_zone, current_zone_id)  # Replace with your logic
                    points = get_points_alt(zones_in_this_section, path, alt_path, current_zone_id)  # Replace with your logic
                    zone_points.alt_path = alt_path_id
                    zone_points.alt_path = alt_path

                zone_points.zone_id = current_zone_id
                zone_points.section = s
                zone_points.main_path_id = main_path_id
                zone_points.main_path = all_paths[p]
                zone_points.points.extend(points)
                # zone_points.extend(points)  # Extend zone_points with tuples of points
                
                path_points.append(zone_points)  # Append zone_points to path_points
            
            section_points.append(path_points)  # Append path_points to section_points
        
        allowable_points.append(section_points)  # Append section_points to allowable_points
    
    return allowable_points

# =================================================================================================
# 
def loop(board, positions, zones, heroes):
    
    # configs = []

    # get master list of allowable points
    # get master list of allowable points for pivot

    # pivot_ids = [0,1,2,3,4,5]
    # movable_heroes = []

    # get pivot id of current pivot
    # current_config = []

# for pivot in pivots:
    # pivot_allowable_points = 
    # for point in pivot_allowable_points:

        # section_id = heroes[pivot].section
        # current_path = get_pivot_path()
        # hero_starting_zone = heroes[current_pivot].starting_point
        # hero_board_map = heroes[current_pivot].board_map
        # current_config.append()

        # for point in master_list[section_id].paths[current_path].zones[hero_starting_zone].map[hero_board_map].points:
            
            # hero2 loop:
                # hero3 loop:
                    # hero4 loop:
                        # hero5 loop:


    # def get_pivot_path():


    pivot = 1



# =================================================================================================
# SCRIPT
# =================================================================================================

if validate_inputs is False:
    exit()

board_terrain = parse_input(format_input(terrain))
board_pos = parse_input(format_input(positions))
board_obstacles = get_obstacle_board(board_terrain, board_pos, obstacles)
board_obstacles_lava = get_obstacle_board(board_terrain, board_pos, obstacles_lava)
board_obstacles_water = get_obstacle_board(board_terrain, board_pos, obstacles_water)
board_obstacles_flying = get_obstacle_board(board_terrain, board_pos, obstacles_flying)
board_obstacles_rubble = get_obstacle_board(board_terrain, board_pos, obstacles_rubble)

boards = [board_obstacles, board_obstacles_lava, board_obstacles_water, board_obstacles_flying, board_obstacles_rubble]

print("\nTerrain:")
print_board(board_terrain)
print("\nPositions:")
print_board(board_pos)
print("board_obstacles:\n", board_obstacles)

# Obstacle board
print("\n--------------------------------")
print("\nObstacles:")
print_board(board_obstacles)
chokepoints = find_chokepoints(board_obstacles)
deadends = find_deadends(board_obstacles, chokepoints)
print("\nchokepoints: ", chokepoints)
print("deadends (", len(deadends), "): ", deadends)
zones = get_zones_of_board(board_obstacles, deadends)
for z in zones:
    print(z)

# # Obstacle board for lava walkers
# print("\n--------------------------------")
# print("\nObstacles Lava:")
# print_board(board_obstacles_lava)
# chokepoints_lava = find_chokepoints(board_obstacles_lava)
# deadends_lava = find_deadends(board_obstacles_lava, chokepoints_lava)
# print("\nchokepoints_lava: ", chokepoints_lava)
# print("deadends_lava: ", deadends_lava)
# zones_lava = get_zones(board_obstacles_lava, deadends_lava)
# for z in zones_lava:
#     print(z)

# # Obstacle board for water walkers
# print("\n--------------------------------")
# print("\nObstacles water:")
# print_board(board_obstacles_water)
# chokepoints_water = find_chokepoints(board_obstacles_water)
# deadends_water = find_deadends(board_obstacles_water, chokepoints_water)
# print("\nchokepoints_water: ", chokepoints_water)
# print("deadends_water: ", deadends_water)
# zones_water = get_zones(board_obstacles_water, deadends_water)
# for z in zones_water:
#     print(z)

# # Obstacle board for flying heroes
# print("\n--------------------------------")
# print("\nObstacles flying:")
# print_board(board_obstacles_flying)
# chokepoints_flying = find_chokepoints(board_obstacles_flying)
# deadends_flying = find_deadends(board_obstacles_flying, chokepoints_flying)
# print("\nchokepoints_flying: ", chokepoints_flying)
# print("deadends_flying: ", deadends_flying)
# zones_flying = get_zones(board_obstacles_flying, deadends_flying)
# for z in zones_flying:
#     print(z)

# # Obstacle board for rubble walkers
# print("\n--------------------------------")
# print("\nObstacles rubble:")
# print_board(board_obstacles_rubble)
# chokepoints_rubble = find_chokepoints(board_obstacles_rubble)
# deadends_rubble = find_deadends(board_obstacles_rubble, chokepoints_rubble)
# print("\nchokepoints_rubble: ", chokepoints_rubble)
# print("deadends_rubble: ", deadends_rubble)
# zones_rubble = get_zones(board_obstacles_rubble, deadends_rubble)
# for z in zones_rubble:
#     print(z)


heroes = init_heroes()

# for h in heroes:
#     print(h)

loop(board_obstacles, board_pos, zones, heroes)

sections = get_sections_in_zones(zones)
print(sections)

print("================================================================")
paths = get_all_paths(zones)
# print("paths:", paths, "\n")

zones_section1 = get_zones_in_section(1, zones)

my_main_hero_start_zone = 2
my_main_hero_end_zone = 25
my_main_hero_zone = 9
my_alt_hero_zone = 19

my_main_path = get_path_from_start_to_end(paths, my_main_hero_start_zone,my_main_hero_end_zone)
print("main path id: ", my_main_path)
print("main hero starting zone id:", my_main_hero_zone)

allowable_points_main = get_points_main(zones_section1, my_main_path, my_main_hero_zone)
print("\nmain allowable_points:\n", allowable_points_main)

my_alt_path = get_path_from_start_to_end(paths, my_main_hero_start_zone, my_alt_hero_zone)

print("\nalt path id: ", my_alt_path)
print("alt hero starting zone id:", my_alt_hero_zone)

allowable_points_alt = get_points_alt(zones_section1, my_main_path, my_alt_path, my_alt_hero_zone)
print("\nAlt allowable_points:\n", allowable_points_alt)

main_list = get_allowable_points(sections, zones, paths)

# for p in main_list[1][575][20].points:
#     print(p)

# Open the file for writing
debug_file = open("logs/debug_log.txt", "w")

# Iterate through each element in the 4D list and write to the file
for s in range(len(main_list)):
    for p in range(len(main_list[s])):
        path_id = main_list[s][p][0].main_path_id
        debug_file.write(f"\n******************************\nSection {s} - Path {path_id} = {paths[path_id]}\n******************************\n")
        for z in range(len(main_list[s][p])):
            zone_id = main_list[s][p][z].zone_id
            debug_file.write(f"Zone {zone_id}: {main_list[s][p][z].points}\n")

# Close the file
debug_file.close()