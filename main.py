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
from modules.board import Map

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
hero_terrain_inputs = inputs.hero_terrains

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
    # Lists of obstacle valid characters
    obstacles_basic_codes = [obstacle_code, lava_code, water_code, rubble_code]
    obstacles_lava_codes = [obstacle_code, water_code, rubble_code]
    obstacles_water_codes = [obstacle_code, lava_code, rubble_code]
    obstacles_flying_codes = [obstacle_code]
    obstacles_rubble_codes = [obstacle_code, lava_code, water_code]

    # Input boards:
    board_terrain = parse_input(format_input(board_terrain_input))
    board_positions = parse_input(format_input(board_positions_input))
    
    # Boards:
    board_obstacles_basic = get_obstacle_board(board_terrain, board_positions, obstacles_basic_codes)
    board_obstacles_lava = get_obstacle_board(board_terrain, board_positions, obstacles_lava_codes)
    board_obstacles_water = get_obstacle_board(board_terrain, board_positions, obstacles_water_codes)
    board_obstacles_flying = get_obstacle_board(board_terrain, board_positions, obstacles_flying_codes)
    board_obstacles_rubble = get_obstacle_board(board_terrain, board_positions, obstacles_rubble_codes)

    print("\nTerrain:")
    print_map_plain(board_terrain)
    print("\nPositions:")
    print_map_plain(board_positions)

    # Map objects:
    map_basic: Map = Map(basic_map_id, "Basic", board_obstacles_basic)

    map_lava: Map = Map(lava_map_id, "Lava", board_obstacles_lava)
    map_water: Map = Map(water_map_id, "Water", board_obstacles_water)
    map_flying: Map = Map(flying_map_id, "Flying", board_obstacles_flying)
    map_rubble: Map = Map(rubble_map_id, "Rubble", board_obstacles_rubble)

    # if count_obstacles(map_terrain, [lava_code]) == 0:
    #     map_lava: Map = map_basic.get_copy(lava_code, "Lava")
    # else:
    #     map_lava: Map = Map(lava_map_id, "Lava", map_obstacles_lava)
    # if count_obstacles(map_terrain, [water_code]) == 0:
    #     map_water: Map = map_basic.get_copy(water_code, "Water")
    # else:
    #     map_water: Map = Map(water_map_id, "Water", map_obstacles_water)
    # if count_obstacles(map_terrain, [lava_code, water_code, rubble_code]) == 0:
    #     map_flying: Map = map_basic.get_copy(flying_map_id, "Flying")
    # else:
    #     map_flying: Map = Map(flying_map_id, "Flying", map_obstacles_flying)
    # if count_obstacles(map_terrain, [rubble_code]) == 0:
    #     map_rubble: Map = map_basic.get_copy(rubble_map_id, "Rubble")
    # else:
    #     map_rubble: Map = Map(rubble_map_id, "Rubble", map_obstacles_rubble)

    return [map_basic, map_lava, map_water, map_flying, map_rubble]

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
# 
def init_heroes() -> list[Hero]:
    heroes = []
    id = 0
    for hero in hero_inputs:
        new_hero = get_hero(hero)
        new_hero.id = id
        new_hero.starting_point = new_hero.get_hero_pos(board_positions_input)
        new_hero.board_map_id = hero_terrain_inputs[id]
        new_hero.board_map = maps[hero_terrain_inputs[id]]

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
# Evaluates both boards and identifies obstacles into one board
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
#
def validate_inputs():
    #TODO
    return True

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
    for s in range(len(map_.points)):
        for p in range(len(map_.points[s])):
            path_id = map_.points[s][p][0].main_path_id
            if path_id < 26:
                path_char = chr(65 + path_id - 3)  # A = 0, B = 1, ..., Z = 25
            else:
                first_char = chr(65 + (path_id - 26 - 3) // 26)  # A-Z
                second_char = chr(65 + (path_id - 26 - 3) % 26)  # A-Z
                path_char = f"{first_char}{second_char}"  # AA, AB, ...
            
            debug_file.write(f"\n******************************\nSection {s} - Path {path_char} : {path_id} = {map_.paths[path_id]}\n******************************\n")
            for z in range(len(map_.points[s][p])):
                zone_id = map_.points[s][p][z].zone_id
                debug_file.write(f"Zone {zone_id}: {map_.points[s][p][z].points}\n")

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
        for s in range(len(map_.points)):
            # Get the number of zones in the current section
            num_zones = len(map_.points[s][0])
            
            # Loop through each zone in the section
            for z in range(num_zones):
                zone_output = f"{z}\t"
                # Loop through each path in the section
                for p in range(len(map_.points[s])):
                    path_points = map_.points[s][p][z].points
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
    exit()

maps = init_maps()
map_basic: Map = maps[basic_map_id]
main_list = map_basic.get_all_allowable_points()

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

output_to_debug_log(map_basic)
output_debug_log_excel(map_basic)
