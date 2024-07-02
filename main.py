# Author: Samuel Riesterer
# Date: 6/1/24
# Titles: Friends & Dragons Planning

# =================================================================================================
# IMPORTS
# =================================================================================================
import sys
import os
from modules.hero import Hero
from modules.map import Map

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
hero_terrains = inputs.hero_terrains

# =================================================================================================
# GLOBALS
# =================================================================================================

maps: list[Map] = []
heros: list[Hero] = []

# =================================================================================================
# Codes
# =================================================================================================


# Map Ids
basic_map_id = Map_Codes.basic_map.value
lava_map_id = Map_Codes.lava_map.value
water_map_id = Map_Codes.water_map.value
flying_map_id = Map_Codes.flying_map.value
rubble_map_id = Map_Codes.rubble_map.value

# Terrain codes
lava_code = Board_Codes.lava_code.value
water_code = Board_Codes.water_code.value
rubble_code = Board_Codes.rubble_code.value
ice_code = Board_Codes.lava_code.value
obstacle_code = Board_Codes.obstacle_code.value
empty_square_code = Board_Codes.empty_square_code.value

# Monster codes
monster_codes = [Monsters_Codes.monster1.value, Monsters_Codes.monster2.value, Monsters_Codes.monster3.value, Monsters_Codes.monster4.value]

# Attack Type codes
# melee_code = Attack_Types.melee
# range_code = Attack_Types.ranged
# pirate_code = Attack_Types.pirate
# magic_code = Attack_Types.magic

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
        return f'{self.id} : Section: {self.section}, IsDeadend: {self.is_deadend}, Connected Zones: {self.connected_zones}, Conn.Deadends: {self.connected_deadend_zones}\n\tPoints: {self.points}'

class Allowable_Points:
    def __init__(self):
        self.section = 0
        self.main_path_id = 0
        self.main_path = []
        self.alt_path_id = None
        self.alt_path = []
        self.zone_id = 0
        self.points = []

# class Map:
#     def __init__(self, id=0, name="", board=None, chokepoints=None, deadends=None, zones=None):
#         self.id = id
#         self.name = name
#         self.board = board if board is not None else []
#         self.chokepoints = chokepoints if chokepoints is not None else []
#         self.deadends = deadends if deadends is not None else []
#         self.zones = zones if zones is not None else []

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
# 
def init_maps() -> list[Map]:
    maps: list[Map] = []

    # Lists of obstacle valid characters
    obstacles_basic_codes = [obstacle_code, lava_code, water_code, rubble_code]
    obstacles_lava_codes = [obstacle_code, water_code, rubble_code]
    obstacles_water_codes = [obstacle_code, lava_code, rubble_code]
    obstacles_flying_codes = [obstacle_code]
    obstacles_rubble_codes = [obstacle_code, lava_code, water_code]

    map_terrain = parse_input(format_input(terrain))
    map_positions = parse_input(format_input(positions))
    map_obstacles_basic = get_obstacle_board(map_terrain, map_positions, obstacles_basic_codes)
    map_obstacles_lava = get_obstacle_board(map_terrain, map_positions, obstacles_lava_codes)
    map_obstacles_water = get_obstacle_board(map_terrain, map_positions, obstacles_water_codes)
    map_obstacles_flying = get_obstacle_board(map_terrain, map_positions, obstacles_flying_codes)
    map_obstacles_rubble = get_obstacle_board(map_terrain, map_positions, obstacles_rubble_codes)

    print("\nTerrain:")
    print_map_plain(map_terrain)
    print("\nPositions:")
    print_map_plain(map_positions)
    
    # Basic Obstacle map
    chokepoints_basic = find_chokepoints(map_obstacles_basic)
    deadends_basic = find_deadends(map_obstacles_basic, chokepoints_basic)
    zones_basic = get_zones_of_map(map_obstacles_basic, deadends_basic)
    map_basic: Map = Map(basic_map_id, "Basic", map_obstacles_basic, chokepoints_basic, deadends_basic, zones_basic)

    # Obstacle map for lava walkers
    if count_obstacles(map_terrain, [lava_code]) == 0:
        map_lava: Map = Map(lava_map_id, "Lava", map_obstacles_basic, chokepoints_basic, deadends_basic, zones_basic)
    else:
        chokepoints_lava = find_chokepoints(map_obstacles_lava)
        deadends_lava = find_deadends(map_obstacles_lava, chokepoints_lava)
        zones_lava = get_zones_of_map(map_obstacles_lava, deadends_lava)
        map_lava: Map = Map(lava_map_id, "Lava", map_obstacles_lava, chokepoints_lava, deadends_lava, zones_lava)

    # Obstacle map for water walkers
    if count_obstacles(map_terrain, [water_code]) == 0:
        map_water: Map = Map(lava_map_id, "Water", map_obstacles_basic, chokepoints_basic, deadends_basic, zones_basic)
    else:
        chokepoints_water = find_chokepoints(map_obstacles_water)
        deadends_water = find_deadends(map_obstacles_water, chokepoints_water)
        zones_water = get_zones_of_map(map_obstacles_water, deadends_water)
        map_water: Map = Map(water_map_id, "Water", map_obstacles_water, chokepoints_water, deadends_water, zones_water)

    # Obstacle map for flying heroes
    if count_obstacles(map_terrain, [lava_code, water_code, rubble_code]) == 0:
        map_flying: Map = Map(lava_map_id, "Flying", map_obstacles_basic, chokepoints_basic, deadends_basic, zones_basic)
    else:
        chokepoints_flying = find_chokepoints(map_obstacles_flying)
        deadends_flying = find_deadends(map_obstacles_flying, chokepoints_flying)
        zones_flying = get_zones_of_map(map_obstacles_flying, deadends_flying)
        map_flying: Map = Map(flying_map_id, "Flying", map_obstacles_flying, chokepoints_flying, deadends_flying, zones_flying)

    # Obstacle map for rubble walkers
    if count_obstacles(map_terrain, [rubble_code]) == 0:
        map_rubble: Map = Map(rubble_map_id, "Rubble", map_obstacles_basic, chokepoints_basic, deadends_basic, zones_basic)
    else:
        chokepoints_rubble = find_chokepoints(map_obstacles_rubble)
        deadends_rubble = find_deadends(map_obstacles_rubble, chokepoints_rubble)
        zones_rubble = get_zones_of_map(map_obstacles_rubble, deadends_rubble)
        map_rubble: Map = Map(rubble_map_id, "Rubble", map_obstacles_rubble, chokepoints_rubble, deadends_rubble, zones_rubble)

    maps.extend([map_basic, map_lava, map_water, map_flying, map_rubble])

    return maps

# =================================================================================================
# 
def count_obstacles(board: list[list[chr]], chars: list[chr]) -> int:
    # Convert the list of characters to lowercase once
    lower_chars = [c.lower() for c in chars]
    count = 0
    for row in board:
        for char in row:
            if char.lower() in lower_chars:
                count += 1
    return count

# =================================================================================================
# VALIDATION METHODS
# =================================================================================================
# Function to check if a point is within the bounds of the board
def within_bounds(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

# =================================================================================================
def is_valid_position(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

# =================================================================================================
def is_valid_point(board, point):
    return 0 <= point[0] < len(board) and 0 <= point[1] < len(board[0])

# =================================================================================================
def is_valid_move(board, visited, row, col, chokepoint) -> bool:
    rows = len(board)
    cols = len(board[0])
    # Check if the move is within the board boundaries
    if not (0 <= row < rows and 0 <= col < cols):
        return False
    # Check if the position is the chokepoint or already visited
    if visited[row][col] or (row, col) == chokepoint:
        return False
    # Check if the position is not an obstacle
    return board[row][col] != obstacle_code

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
    return board[row][col] == empty_square_code
def square_is_obstacle(board, row, col):
    return board[row][col] == obstacle_code
# =================================================================================================
# Diagnoal obstacles check
def obstacle_above_left(board, row, col):
    return board[row-1][col-1] == obstacle_code
def obstacle_above_right(board, row, col):
    return board[row-1][col+1] == obstacle_code
def obstacle_below_left(board, row, col):
    return board[row+1][col-1] == obstacle_code
def obstacle_below_right(board, row, col):
    return board[row+1][col+1] == obstacle_code
# =================================================================================================
# Empty squares check
def empty_square_left(board, row, col):
    return board[row][col-1] == empty_square_code
def empty_square_right(board, row, col):
    return board[row][col+1] == empty_square_code
def empty_square_above(board, row, col):
    return board[row-1][col] == empty_square_code
def empty_square_below(board, row, col):
    return board[row+1][col] == empty_square_code
def empty_square_left_and_right(board, row, col):
    return empty_square_left(board, row, col) and empty_square_right(board, row, col)
def empty_square_above_and_below(board, row, col):
    return empty_square_above(board, row, col) and empty_square_below(board, row, col)
# =================================================================================================
# Obstacles check
def obstacle_left(board, row, col):
    return board[row][col-1] == obstacle_code
def obstacle_right(board, row, col):
    return board[row][col+1] == obstacle_code
def obstacle_above(board, row, col):
    return board[row-1][col] == obstacle_code
def obstacle_below(board, row, col):
    return board[row+1][col] == obstacle_code
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
def is_deadend(board: list[list[chr]], chokepoint: tuple):
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

# # =================================================================================================
# # True if a path exists on the board from start to end and not passing through the chokepoint
def does_path_exist(board: list[list[chr]], start: tuple[int, int], end: tuple[int, int], chokepoint: tuple[int, int]) -> bool:
    rows, cols = len(board), len(board[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def is_valid_move(board, visited, row, col, chokepoint) -> bool:
        # Check if the move is within the board boundaries
        if not (0 <= row < rows and 0 <= col < cols):
            return False
        # Check if the position is the chokepoint or already visited
        if visited[row][col] or (row, col) == chokepoint:
            return False
        # Check if the position is not an obstacle
        return board[row][col] != 'O'
    
    def backtrack(row, col) -> bool:
        # Check if we've reached the end point
        if (row, col) == end:
            return True
        # Mark the current position as visited
        visited[row][col] = True
        
        # Define possible movement directions (right, down, left, up)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(board, visited, new_row, new_col, chokepoint):
                if backtrack(new_row, new_col):
                    return True
        
        # No need to unmark the current position (backtracking)
        return False

    start_row, start_col = start
    return backtrack(start_row, start_col)

# =================================================================================================
# Checks if the point is a chokepoint
def is_chokepoint(board: list[list[chr]], row: int, col: int) -> bool:
    # Ensure the current cell is an empty square
    if board[row][col] != empty_square_code:
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
def get_zones_of_map(board: list[list[chr]], deadends: list[tuple]) -> list[Zone]:
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
            if board[r][c] == empty_square_code and (r, c) not in visited:
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
def find_chokepoints(board) -> list[tuple]:
    chokepoints = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_chokepoint(board, row, col):
                chokepoints.append((row, col))
    return chokepoints

# =================================================================================================
# Evaluates both boards and identifies obstacles into one board
def get_obstacle_board(board_terrain: list[list[chr]], board_pos: list[list[chr]], obstacles: list[chr]) -> list[list[str]]:
    # Determine the size of the boards
    rows = len(board_terrain)
    cols = len(board_terrain[0])

    # Create an empty board for the final output
    final_board = [[empty_square_code for _ in range(cols)] for _ in range(rows)]
    
    # Iterate through each position in the boards
    for i in range(rows):
        for j in range(cols):
            # Check if the terrain board has an obstacle
            if board_terrain[i][j] in obstacles:
                final_board[i][j] = obstacle_code
            # Check if the position board has a monster character
            elif board_pos[i][j] in monster_codes:
                final_board[i][j] = obstacle_code
            # Otherwise, keep the square empty
            else:
                final_board[i][j] = empty_square_code
    
    return final_board

# =================================================================================================
def find_deadends(board: list[list[chr]], chokepoints: tuple) -> list[tuple]:
    obstacles = []
    for chokepoint in chokepoints:
        if is_deadend(board, chokepoint):
            obstacles.append(chokepoint)
    return obstacles

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
def init_heroes() -> list[Hero]:
    heroes = []
    id = 0
    for hero in hero_inputs:
        new_hero = get_hero(hero)
        new_hero.id = id
        new_hero.starting_point = get_hero_pos(positions, id)
        new_hero.current_point = new_hero.starting_point
        new_hero.board_map_id = hero_terrains[id]
        new_hero.board_map = maps[hero_terrains[id]]



        heroes.append(new_hero)
        id = id + 1
    return heroes

# =================================================================================================
def get_hero(hero_name) -> Hero:
    name = hero_name.lower()
    # melee4_heroes = ['assassin', 'knight']
    # melee8_heroes = ['monk', 'rouge', 'barbarian']
    # range4_heroes = []
    # range8_heroes = ['ranger']
    # magic4_heroes = ['mage']
    # magic8_heroes = ['elementalist']

    new_hero = Hero()
    new_hero.name = hero_name

    if name == 'monk':
        new_hero.attack_type = 1
    elif name == 'barbarian':
        new_hero.attack_type = 1
    elif name == 'assassin':
        new_hero.attack_type = 1
    elif name == 'rouge':
        new_hero.attack_type = 1
    elif name == 'knight':
        new_hero.attack_type = 1
    elif name == 'warrior':
        new_hero.attack_type = 1
    elif name == 'guardian':
        new_hero.attack_type = 1
    elif name == 'pirate':
        new_hero.attack_type = 1
    elif name == 'ranger':
        new_hero.attack_type = 1
    elif name == 'archer':
        new_hero.attack_type = 1
    elif name == 'hunter':
        new_hero.attack_type = 1
    elif name == 'jav':
        new_hero.attack_type = 1
    elif name == 'mage':
        new_hero.attack_type = 1
    elif name == 'elemental':
        new_hero.attack_type = 1
    elif name == 'warlock':
        new_hero.attack_type = 1
    elif name == 'wizard':
        new_hero.attack_type = 1
    elif name == 'healer':
        new_hero.attack_type = 1
    elif name == 'paladin':
        new_hero.attack_type = 1
    elif name == 'druid':
        new_hero.attack_type = 1
    elif name == 'bard':
        new_hero.attack_type = 1
    elif name == 'princess':
        new_hero.attack_type = 1

    return new_hero

# =================================================================================================
# LOOP METHODS
# =================================================================================================


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
def get_points_main_old(zones: list[Zone], main_path_of_pivot: list[int], hero_start_zone_id: int):
    allowable_points = []

    # A movable hero can move anywhere in his current zone unless it is a DE
    # because being on the main path of the pivot, he is forced off his DE to the previous zone
    points_in_current_zone = get_points_in_zone(hero_start_zone_id, zones)
    if points_in_current_zone and not is_deadend_zone(hero_start_zone_id, zones):
        allowable_points.extend(points_in_current_zone)

    # Hero starts on a deadend zone
    if is_deadend_zone(hero_start_zone_id, zones):
        previous_zone_id = get_previous_zone_id(hero_start_zone_id, main_path_of_pivot)
        if previous_zone_id is not None:
            previous_zone: Zone = next((z for z in zones if z.id == previous_zone_id), None)
            if previous_zone:
                # Hero can move anywhere in the previous zone
                allowable_points.extend(previous_zone.points)
                # Hero can move to previous zones connected deadend zones, with exceptions
                connected_deadend_zones = get_connected_deadend_zone_ids(previous_zone_id, zones)
                restricted_zones = [hero_start_zone_id] # Cannot move to his start zone because it is a DE on the main path
                # If the previous zone from the hero start is a DE
                if is_deadend_zone(previous_zone_id, zones):
                    previous_previous_zone_id = get_previous_zone_id(previous_zone_id, main_path_of_pivot)
                    # If the previous zone from the previous zone from the hero start is a DE
                    # This is describing a single row or column of DEs
                    if previous_previous_zone_id and is_deadend_zone(previous_previous_zone_id, zones):
                        # Cannot move to the DE prior to the DE the hero got displaced on because it is a single row/col of DEs
                        restricted_zones.append(previous_previous_zone_id) 
                for z_id in connected_deadend_zones:
                    if z_id not in restricted_zones:
                        zone: Zone = next((z for z in zones if z.id == z_id), None)
                        if zone:
                            # Add all other connected DEs to the previous zone because they are allowed
                            allowable_points.extend(zone.points) 

    # Movable hero starts on a nondeadend zone
    else:
        current_zone: Zone = next((z for z in zones if z.id == hero_start_zone_id), None)
        if current_zone:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the downstream zone on the main path
            connected_deadend_zones = get_connected_deadend_zone_ids(hero_start_zone_id, zones)
            next_deadend_zone_id = get_next_deadend_zone_id(hero_start_zone_id, main_path_of_pivot, zones) # downstream deadend zone
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
# Gets a list of all allowable points for a moveable hero who is on the main path of the pivot
# zones = a list of Zone objects for the given board (should only be 1 section)
# main_path = a list of zones the pivot moves through
# start_zone = the starting zone of the movable hero
def get_points_main(zones: list[Zone], main_path_of_pivot: list[int], hero_start_zone_id: int):
    allowable_points = []
    allowable_zones = []

    # A movable hero can move anywhere in his current zone unless it is a DE
    # because being on the main path of the pivot, he is forced off his DE to the previous zone
    if not is_deadend_zone(hero_start_zone_id, zones):
        allowable_zones.append(hero_start_zone_id)

    # Hero starts on a deadend zone
    if is_deadend_zone(hero_start_zone_id, zones):
        previous_zone_id = get_previous_zone_id(hero_start_zone_id, main_path_of_pivot)
        if previous_zone_id is not None:
            # Hero can move anywhere in the previous zone
            allowable_zones.append(previous_zone_id)
            # Hero can move to previous zones connected deadend zones, with exceptions
            connected_deadend_zones = get_connected_deadend_zone_ids(previous_zone_id, zones)
            connected_deadend_zones.remove(hero_start_zone_id) # Cannot move to his start zone because it is a DE on the main path
            # If the previous zone from the hero start is a DE
            if is_deadend_zone(previous_zone_id, zones):
                previous_previous_zone_id = get_previous_zone_id(previous_zone_id, main_path_of_pivot)
                # If the previous zone from the previous zone from the hero start is a DE
                # This is describing a single row or column of DEs
                if previous_previous_zone_id and is_deadend_zone(previous_previous_zone_id, zones):
                    # Cannot move to the DE prior to the DE the hero got displaced on because it is a single row/col of DEs
                    connected_deadend_zones.remove(previous_previous_zone_id)
            allowable_zones.extend(connected_deadend_zones)

    # Movable hero starts on a nondeadend zone
    else:
        # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
        # start zone except the downstream zone on the main path
        connected_deadend_zones = get_connected_deadend_zone_ids(hero_start_zone_id, zones)
        next_deadend_zone_id = get_next_deadend_zone_id(hero_start_zone_id, main_path_of_pivot, zones) # downstream deadend zone
        if next_deadend_zone_id:
            connected_deadend_zones.remove(next_deadend_zone_id)
        allowable_zones.extend(connected_deadend_zones)

    # Add the points from the allowable zones to the list
    for z in allowable_zones:
        allowable_points.extend(get_points_in_zone(z, zones))

    # Remove dups
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
def get_points_alt(zones: list[Zone], main_path_of_pivot: list[int], alt_path_of_pivot: list[int], hero_start_zone_id: int):
    allowable_points = []  # Allow duplicates
    allowable_zones = []

    # A movable hero can move anywhere in his current zone
    allowable_zones.append(hero_start_zone_id)

    # Movable hero starts on a deadend zone
    if is_deadend_zone(hero_start_zone_id, zones):
        previous_zone_id = get_previous_zone_id(hero_start_zone_id, alt_path_of_pivot)
        if previous_zone_id is not None:
            # If the previous zone is a deadend:
            if is_deadend_zone(previous_zone_id, zones):
                pass # No allowable points in the previous zone
            else: # If the previous zone is not a deadend
                # Hero starts on deadend zone can move to the previous nondeadend zone
                allowable_zones.append(previous_zone_id)
                connected_deadend_zones = get_connected_deadend_zone_ids(previous_zone_id, zones)
                # Previous nondeadend zone is on the main path
                if zone_is_on_main_path(previous_zone_id, main_path_of_pivot):
                    restricted_zone_id = get_next_deadend_zone_id(previous_zone_id, main_path_of_pivot, zones) # Downstream
                # Previous nondeadend zone is not on the main path
                else:
                    restricted_zone_id = get_previous_deadend_zone_id(previous_zone_id, alt_path_of_pivot, zones) # Upstream

                # Add the allowable connected deadend zones
                if restricted_zone_id:
                    connected_deadend_zones.remove(restricted_zone_id)

                allowable_zones.extend(connected_deadend_zones)

    # Movable hero starts on a nondeadend zone
    else:
        # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
        # start zone except the upstream zone on the alt path
        connected_deadend_zones = get_connected_deadend_zone_ids(hero_start_zone_id, zones)
        restricted_zone_id = get_previous_deadend_zone_id(hero_start_zone_id, alt_path_of_pivot, zones)
        connected_deadend_zones.remove(restricted_zone_id)
        allowable_zones.extend(connected_deadend_zones)

    # Add the points from the allowable zones to the list
    for z in allowable_zones:
        allowable_points.extend(get_points_in_zone(z, zones))

    # Remove dups
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
def get_previous_zone_id(zone_id: int, path: list[int]):
    for p in range(len(path) - 1):
        if zone_id == path[p+1]:
            return path[p]
    return None

# =================================================================================================
def zone_is_on_main_path(zone_id, main_path: list[int]):
    return zone_id in main_path

# =================================================================================================
# Get all connected deadend zones to the zone_id given
def get_connected_deadend_zone_ids(zone_id, zones: list[Zone]) -> list[int]:
    connected_deadend_zones = []
    for z in zones:
        if z.id == zone_id:
            for conn_id in z.connected_zones:
                if is_deadend_zone(conn_id, zones):
                    connected_deadend_zones.append(conn_id)
    return connected_deadend_zones

# =================================================================================================
# Returns the previous deadend zone prior to the zone_id on the path of zones given
def get_previous_deadend_zone_id(zone_id, path: list[Zone], zones: list[Zone]) -> int | None:
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
def get_next_deadend_zone_id(zone_id, path: list[int], zones: list[Zone]):
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
def get_all_allowable_points(all_sections: list[int], all_zones: list[Zone], all_paths: list[list[int]]) -> list[list[list[list[tuple]]]]:
    allowable_points = []

    for s in range(len(all_sections)):
        section_points = []
        zones_in_this_section = get_zones_in_section(all_sections[s], all_zones)
        paths_in_this_section = get_paths_in_section(all_sections[s], all_zones)
        # print(f"section: {s}, zones in this section: ")
        # for j in zones_in_this_section:
        #     print(j)
        # print("paths in this section: ")
        # for i in paths_in_this_section:
        #     print(i)
        for p in range(len(paths_in_this_section)):
            path_points = []
            main_path = paths_in_this_section[p]
            pivot_start_zone = main_path[0]
            pivot_end_zone = main_path[len(main_path)-1]
            main_path_id = get_path_id(all_paths, pivot_start_zone, pivot_end_zone)

            for z in range(len(zones_in_this_section)):
                zone_points: Allowable_Points = Allowable_Points()
                zone = zones_in_this_section[z]
                current_zone_id = zone.id

                if current_zone_id in main_path:
                    points = get_points_main(zones_in_this_section, main_path, current_zone_id)  # Replace with your logic
                    zone_points.alt_path = None
                else:
                    alt_path_id = get_path_id(all_paths, pivot_start_zone, current_zone_id)
                    alt_path = get_path_from_start_to_end(paths_in_this_section, pivot_start_zone, current_zone_id)  # Replace with your logic
                    points = get_points_alt(zones_in_this_section, main_path, alt_path, current_zone_id)  # Replace with your logic
                    zone_points.alt_path = alt_path_id
                    zone_points.alt_path = alt_path

                zone_points.zone_id = current_zone_id
                zone_points.section = s
                zone_points.main_path_id = main_path_id
                zone_points.main_path = all_paths[p]
                zone_points.points.extend(points)
                
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
# PRINT METHODS
# =================================================================================================
def print_map_plain(board):
    # Print column numbers
    print('    ', end='')
    for col in range(len(board[0])):
        print(f'{col:2}', end='')
    print()
    print(" ---------------------------------")

    # Print board rows with row numbers
    for i, row in enumerate(board):
        print(f'{i:2} | ', end='')
        print(' '.join(row))

# =================================================================================================
def print_map_with_zones(map: Map):
    print("Zone Map: ", map.name, "\n")

    # Track which zones have been printed in this row
    printed_zones = []

    # Print column numbers
    print('    ', end='')
    for col in range(len(map.board[0])):
        if col == 10:
            print(" ", end= "")
        print(f'{col:2}', end=' ')
    print()

    print("------", end = "")
    for i in range(len(map.board[0])):
        print("---", end = "")
    print("\n", end = "")

    # Loop through the rows
    for i in range(len(map.board)):
        print(f'{i:2} | ', end='')

        # Loop through the columns
        for j in range(len(map.board[i])):
            found = False
            # Check each zone
            for zone in map.zones:
                # Find the zone that contains the current board position
                if (i, j) in zone.points and zone.id not in printed_zones:
                    # Print the zone id as a 2-digit number
                    print(f'{zone.id:02}', end=' ')
                    found = True
                    printed_zones.append(zone.id)
                    break

            # If no zone contains the current position, check for obstacle
            if not found:
            # else:
                if map.board[i][j] == obstacle_code:
                    print('[]', end=' ')
                else:
                    print('..', end=' ')

        print('|')

    print("------", end = "")
    for i in range(len(map.board[0])):
        print("---", end = "")
    print("\n")

# =================================================================================================
def print_map_details(name, board, zones, chokepoints, deadends):
    print(name)
    print("\n--------------------------------")
    print_map_with_zones(board, zones)
    print("\nchokepoints: ", chokepoints)
    print("deadends (", len(deadends), "): ", deadends)
    for z in zones:
        print(z)

# =================================================================================================
def print_debug_log(main_list):
    # Open the file for writing
    debug_file = open("logs/debug_log.txt", "w")

    # Iterate through each element in the 4D list and write to the file
    for s in range(len(main_list)):
        for p in range(len(main_list[s])):
            path_id = main_list[s][p][0].main_path_id
            if path_id < 26:
                path_char = chr(65 + path_id - 3)  # A = 0, B = 1, ..., Z = 25
            else:
                first_char = chr(65 + (path_id - 26 - 3) // 26)  # A-Z
                second_char = chr(65 + (path_id - 26 - 3) % 26)  # A-Z
                path_char = f"{first_char}{second_char}"  # AA, AB, ...
            
            debug_file.write(f"\n******************************\nSection {s} - Path {path_char} : {path_id} = {paths[path_id]}\n******************************\n")
            for z in range(len(main_list[s][p])):
                zone_id = main_list[s][p][z].zone_id
                debug_file.write(f"Zone {zone_id}: {main_list[s][p][z].points}\n")

    # Close the file
    debug_file.close()

# =================================================================================================
def print_debug_log_excel(paths, main_list):
    # Open the debug file for writing
    with open("logs/debug_log2.txt", "w") as debug_file:

        debug_file.write(f"\t")

        # Print paths as first row
        for p in paths:
            path_str = ", ".join(map(str, p))
            debug_file.write(f"{path_str} \t ")
        debug_file.write(f"\n")

        # Loop through the sections
        for s in range(len(main_list)):
            # Get the number of zones in the current section
            num_zones = len(main_list[s][0])
            
            # Loop through each zone in the section
            for z in range(num_zones):
                zone_output = f"{z}\t"
                # Loop through each path in the section
                for p in range(len(main_list[s])):
                    path_points = main_list[s][p][z].points
                    # Convert list of points to a string and remove brackets
                    points_str = str(path_points).replace("[", "").replace("]", "")
                    zone_output += f"{points_str} \t"
                
                # Remove the trailing tab and space
                zone_output = zone_output.rstrip('\t ')
                # Write the formatted output to the debug file
                debug_file.write(f"{zone_output}\n")

# =================================================================================================
# SCRIPT
# =================================================================================================

if validate_inputs is False:
    exit()

# Init all boards
maps = init_maps()

# for i in range(5):
#     print_map_with_zones(maps[i])

heroes = init_heroes()

# for h in heroes:
#     print(h)


# obstacle_basic_chrs = [Board_Codes.lava_code, Board_Codes.obstacle_code, Board_Codes.rubble_code, Board_Codes.water_code, Board_Codes.monster_code]
# obstacles_basic_codes = [char.value for char in obstacle_basic_chrs]
# print("obstacles_basic_codes: \n", obstacles_basic_codes)
# map_terrain = parse_input(format_input(terrain))
# print("map terrain: ")
# print_map_plain(map_terrain)
# map_positions = parse_input(format_input(positions))
# print("map pos: ")
# print_map_plain(map_positions)
# map_obstacles_basic = get_obstacle_board(map_terrain, map_positions, obstacles_basic_codes)
# print("map_obstacle_basic:")
# print_map_plain(map_obstacles_basic)

# chokepoints_basic = find_chokepoints(map_obstacles_basic)
# deadends_basic = find_deadends(map_obstacles_basic, chokepoints_basic)
# print(deadends_basic)

# zones_basic = get_zones_of_map(map_obstacles_basic, deadends_basic)
# map_basic: Map_Ids = Map_Ids(basic_map_id, "Basic", map_obstacles_basic, chokepoints_basic, deadends_basic, zones_basic)
    
zones_basic = maps[basic_map_id].zones

# zones_basic = get_zones_of_map(map_obstacles_basic, deadends_basic)

# for z in zones_basic:
#     print("zones:\n", z)

sections = get_sections_in_zones(zones_basic)
print(sections)

print("================================================================")
paths = get_all_paths(zones_basic)
# print("paths:", paths, "\n")

zones_section1 = get_zones_in_section(1, zones_basic)

my_main_hero_start_zone = 2
my_main_hero_end_zone = 25
my_main_hero_zone = 9
my_alt_hero_zone = 19

# my_main_path = get_path_from_start_to_end(paths, my_main_hero_start_zone,my_main_hero_end_zone)
# print("main path id: ", my_main_path)
# print("main hero starting zone id:", my_main_hero_zone)

# allowable_points_main = get_points_main(zones_section1, my_main_path, my_main_hero_zone)
# print("\nmain allowable_points:\n", allowable_points_main)

# my_alt_path = get_path_from_start_to_end(paths, my_main_hero_start_zone, my_alt_hero_zone)

# print("\nalt path id: ", my_alt_path)
# print("alt hero starting zone id:", my_alt_hero_zone)

# allowable_points_alt = get_points_alt(zones_section1, my_main_path, my_alt_path, my_alt_hero_zone)
# print("\nAlt allowable_points:\n", allowable_points_alt)

# main_list = get_all_allowable_points(sections, zones_basic, paths)

# for p in main_list[1][575][20].points:
#     print(p)


