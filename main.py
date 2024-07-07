# Author: Samuel Riesterer
# Date: 6/1/24
# Titles: Friends & Dragons Planning

# =================================================================================================
# IMPORTS
# =================================================================================================
import sys
import os
from modules.hero import Hero
from modules.zone import Zone
from modules.point import Allowable_Point
from modules.map import Map

from enums import *
from inputs import Inputs
from logger import log

sys.path.append('/modules')

# =================================================================================================
# INPUTS
# =================================================================================================

inputs = Inputs()
board_terrain_input = inputs.terrain
board_positions_input = inputs.positions
hero_inputs = inputs.heroes

# =================================================================================================
# GLOBALS
# =================================================================================================

board_terrain = None
board_positions = None
maps: list[Map] = []
heros: list[Hero] = []

# Number of specific obstacles in terrain:
num_lava: int = None
num_water: int = None
num_rubble: int = None
num_flying: int = None

# Only certain maps are needed, assume False unless proved True:
need_lava_map = False
need_water_map = False
need_rubble_map = False
need_flying_map = False

# =================================================================================================
# Codes
# =================================================================================================

# Terrain codes
lava_code = Board_Codes.lava_code.value
water_code = Board_Codes.water_code.value
rubble_code = Board_Codes.rubble_code.value
ice_code = Board_Codes.lava_code.value
obstacle_code = Board_Codes.obstacle_code.value
empty_square_code = Board_Codes.empty_square_code.value

# Monster codes
monster_codes = [Monsters_Codes.monster1.value, Monsters_Codes.monster2.value, Monsters_Codes.monster3.value, Monsters_Codes.monster4.value]

# Map Ids
basic_map_id = Map_Codes.basic_map.value
lava_map_id = Map_Codes.lava_map.value
water_map_id = Map_Codes.water_map.value
rubble_map_id = Map_Codes.rubble_map.value
flying_map_id = Map_Codes.flying_map.value

# Map Matchup Ids
basic_match_id = Map_Matchups.basic.value
lava_match_id = Map_Matchups.lava.value
water_match_id = Map_Matchups.water.value
rubble_match_id = Map_Matchups.rubble.value
flying_match_id = Map_Matchups.flying.value
lava_basic_match_id = Map_Matchups.lava_basic.value
water_basic_match_id = Map_Matchups.water_basic.value
rubble_basic_match_id = Map_Matchups.rubble_basic.value
flying_basic_match_id = Map_Matchups.flying_basic.value
flying_lava_match_id = Map_Matchups.flying_lava.value
flying_water_match_id = Map_Matchups.flying_water.value
flying_rubble_match_id = Map_Matchups.flying_rubble.value

# Attack Type codes
# melee_code = Attack_Types.melee
# range_code = Attack_Types.ranged
# pirate_code = Attack_Types.pirate
# magic_code = Attack_Types.magic

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
def get_maps() -> list[Map]:
    # Init the different types of maps. Only need to init if they are going to be used.
    # Init basic map
    obstacles_basic_codes = [obstacle_code, lava_code, water_code, rubble_code]
    board_obstacles_basic = get_obstacle_board(board_terrain, board_positions, obstacles_basic_codes)
    map_basic: Map = Map(basic_map_id, "Basic", board_obstacles_basic)

    # Init lava map
    map_lava = None
    if need_lava_map:
        obstacles_lava_codes = [obstacle_code, water_code, rubble_code]
        board_obstacles_lava = get_obstacle_board(board_terrain, board_positions, obstacles_lava_codes)
        map_lava: Map = Map(lava_map_id, "Lava", board_obstacles_lava)

    # Init water map
    map_water = None
    if need_water_map:
        obstacles_water_codes = [obstacle_code, lava_code, rubble_code]
        board_obstacles_water = get_obstacle_board(board_terrain, board_positions, obstacles_water_codes)
        map_water: Map = Map(water_map_id, "Water", board_obstacles_water)

    # Init rubble map
    map_rubble = None
    if need_rubble_map:
        obstacles_rubble_codes = [obstacle_code, lava_code, water_code]
        board_obstacles_rubble = get_obstacle_board(board_terrain, board_positions, obstacles_rubble_codes)
        map_rubble: Map = Map(rubble_map_id, "Rubble", board_obstacles_rubble)

    # Init flying map
    map_flying = None
    if need_flying_map:
        obstacles_flying_codes = [obstacle_code]
        board_obstacles_flying = get_obstacle_board(board_terrain, board_positions, obstacles_flying_codes)
        map_flying: Map = Map(flying_map_id, "Flying", board_obstacles_flying)

    return [map_basic, map_lava, map_water, map_rubble, map_flying]

# =================================================================================================
# 
def init_heroes() -> list[Hero]:
    heroes: list[Hero] = []
    id = 0
    for hero in hero_inputs:
        new_hero = get_hero(hero)
        new_hero.id = id
        new_hero.starting_point = new_hero.get_hero_pos(board_positions_input)
        # new_hero.section = maps[new_hero.board_map_id].get_section_of_point(new_hero.starting_point)
        
        # new_hero.pivot_points = maps[new_hero.board_map_id].get_points_in_section(new_hero.section)
        heroes.append(new_hero)
        id = id + 1
    return heroes

# =================================================================================================
# 
def init_needed_maps() -> list[int]:
    global need_lava_map, need_water_map, need_rubble_map, need_flying_map

    for h in hero_inputs:
        if h.board_map_id == lava_map_id and h.pivot and num_lava > 0:
            need_lava_map = True
        if h.board_map_id == water_map_id and h.pivot and num_water > 0:
            need_water_map = True
        if h.board_map_id == rubble_map_id and h.pivot and num_rubble > 0:
            need_rubble_map = True
        if h.board_map_id == flying_map_id and h.pivot and num_flying > 0:
            need_flying_map = True

# =================================================================================================
# 
def init_boards():
    global board_terrain, board_positions, num_lava, num_water, num_rubble, num_flying

    def count_obstacles(board: list[list[chr]], chars: list[chr]) -> int:
        lower_chars = [c.lower() for c in chars]
        count = 0
        for row in board:
            for char in row:
                if char.lower() in lower_chars:
                    count += 1
        return count

    # Parse input boards from list of strings to lists of list of characters:
    board_terrain = parse_input(format_input(board_terrain_input))
    board_positions = parse_input(format_input(board_positions_input))
    print("\nTerrain:")
    print_map_plain(board_terrain)
    print("\nPositions:")
    print_map_plain(board_positions)

    # Count specific number of obstacles:
    num_lava = count_obstacles(board_terrain, [lava_code])
    num_water = count_obstacles(board_terrain, [water_code])
    num_rubble = count_obstacles(board_terrain, [rubble_code])
    num_flying = num_lava + num_water + num_rubble

# =================================================================================================
#
def get_hero(hero: Hero) -> Hero:
    cls = hero.cls.lower()

    new_hero = hero.copy()

    if cls == 'monk':
        new_hero.attack_type = 1
    elif cls == 'barbarian':
        new_hero.attack_type = 1
    elif cls == 'assassin':
        new_hero.attack_type = 1
    elif cls == 'rouge':
        new_hero.attack_type = 1
    elif cls == 'knight':
        new_hero.attack_type = 1
    elif cls == 'warrior':
        new_hero.attack_type = 1
    elif cls == 'guardian':
        new_hero.attack_type = 1
    elif cls == 'pirate':
        new_hero.attack_type = 1
    elif cls == 'ranger':
        new_hero.attack_type = 1
    elif cls == 'archer':
        new_hero.attack_type = 1
    elif cls == 'hunter':
        new_hero.attack_type = 1
    elif cls == 'jav':
        new_hero.attack_type = 1
    elif cls == 'mage':
        new_hero.attack_type = 1
    elif cls == 'elemental':
        new_hero.attack_type = 1
    elif cls == 'warlock':
        new_hero.attack_type = 1
    elif cls == 'wizard':
        new_hero.attack_type = 1
    elif cls == 'healer':
        new_hero.attack_type = 1
    elif cls == 'paladin':
        new_hero.attack_type = 1
    elif cls == 'druid':
        new_hero.attack_type = 1
    elif cls == 'bard':
        new_hero.attack_type = 1
    elif cls == 'princess':
        new_hero.attack_type = 1

    return new_hero

# =================================================================================================
# Evaluates both boards (terrain and positions) and identifies obstacles into one board
# obstacles is a list of characters that will be identified as an obstacle (e.g. L for lava, W for 
# water, etc.)
def get_obstacle_board(board_terrain: list[list[chr]], board_pos: list[list[chr]], obstacles: list[chr]) -> list[list[chr]]:
    # Determine the size of the boards
    rows = len(board_terrain)
    cols = len(board_terrain[0])
    # board: Board = Board()

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
# VALIDATION METHODS
# =================================================================================================
# Determine if inputs are valid
def validate_inputs():
    #TODO
    return True

# =================================================================================================
#
def validate_maps(heros: list[Hero]) -> list[int]:
    maps_needed = []

    
    for h in heroes:
        
        pass


    return maps_needed

# =================================================================================================
# LOOP METHODS
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
def output_to_debug_log(map_: Map):
    # Open the file for writing
    debug_file = open("logs/debug_log.txt", "w")

    # Iterate through each element in the 4D list and write to the file
    for s in range(len(map_.points_same)):
        for p in range(len(map_.points_same[s])):
            path_id = map_.points_same[s][p][0].main_path_id
            if path_id < 26:
                path_char = chr(65 + path_id - 3)  # A = 0, B = 1, ..., Z = 25
            else:
                first_char = chr(65 + (path_id - 26 - 3) // 26)  # A-Z
                second_char = chr(65 + (path_id - 26 - 3) % 26)  # A-Z
                path_char = f"{first_char}{second_char}"  # AA, AB, ...
            
            debug_file.write(f"\n******************************\nSection {s} - Path {path_char} : {path_id} = {map_.paths[path_id]}\n******************************\n")
            for z in range(len(map_.points_same[s][p])):
                zone_id = map_.points_same[s][p][z].zone_id
                debug_file.write(f"Zone {zone_id}: {map_.points_same[s][p][z].points}\n")

    # Close the file
    debug_file.close()

# =================================================================================================
def output_to_debug_log2(map_: Map):
    # Open the file for writing
    debug_file = open("logs/debug_log2.txt", "w")

    # Iterate through each element in the 3D list and write to the file
    for i in range(len(map_.zones)):
        for j in range(len(map_.zones)):
            debug_file.write(f"\n****************\nPivot path: {i} to {j}\n****************\n")
            for k in range(len(map_.zones)):
                debug_file.write(f"{k:02} : {map_.points_new[i][j][k]}\n")

    # Close the file
    debug_file.close()

# =================================================================================================
def output_debug_log_excel(map_: Map):
    # Open the debug file for writing
    with open("logs/debug_log2.txt", "w") as debug_file:

        debug_file.write(f"\t")

        # Print paths as first row
        for p in map_.paths:
            path_str = ", ".join(map(str, p))
            debug_file.write(f"{path_str} \t ")
        debug_file.write(f"\n")

        # Loop through the sections
        for s in range(len(map_.points_same)):
            # Get the number of zones in the current section
            num_zones = len(map_.points_same[s][0])
            
            # Loop through each zone in the section
            for z in range(num_zones):
                zone_output = f"{z}\t"
                # Loop through each path in the section
                for p in range(len(map_.points_same[s])):
                    path_points = map_.points_same[s][p][z].points
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

# Setup:
if validate_inputs is False:
    print("Error in inputs. Exiting program.")
    exit()

init_boards()
init_needed_maps()
maps = get_maps()
heroes = init_heroes()

for h in heroes:
    print(h)
    print(h.pivot_points)

map_basic: Map = maps[basic_map_id]
main_list = map_basic.get_all_allowable_points_same()

map_basic.print_map_with_zones()

# Simulation
my_main_hero_start_zone = 2
my_main_hero_end_zone = 25
my_main_hero_zone = 9
my_alt_hero_zone = 19

my_main_path = map_basic.get_path_from_start_to_end(my_main_hero_start_zone, my_main_hero_end_zone)
print("main path id: ", my_main_path)
print("main hero starting zone id:", my_main_hero_zone)

my_alt_path = map_basic.get_path_from_start_to_end(my_main_hero_start_zone, my_alt_hero_zone)
print("\nalt path id: ", my_alt_path)
print("alt hero starting zone id:", my_alt_hero_zone)


# how to iterate through list
for p in main_list[1][575][20].points:
    print(p)

# output_to_debug_log(map_basic)
output_debug_log_excel(map_basic)
output_to_debug_log2(map_basic)
