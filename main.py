# Author: Samuel Riesterer
# Date: 6/1/24
# Titles: Friends & Dragons Planning

# =================================================================================================
# IMPORTS
# =================================================================================================
import sys
import os
import time
from modules.configuration import Configuration
from modules.hero import Hero
from modules.setup import Setup
from modules.zone import Zone
from modules.allowable import Allowable
from modules.map import Map

from enums import *
from inputs import Inputs
from logger import log
from random_map import Random_Map

# sys.path.append('/modules')
# sys.path.append('/test')

# =================================================================================================
# INPUTS
# =================================================================================================

inputs = Inputs()
input_board_terrain = inputs.terrain
input_board_positions = inputs.positions
input_heroes = inputs.heroes

# =================================================================================================
# GLOBALS
# =================================================================================================

# board_terrain = None
# board_positions = None
maps: list[Map] = []
heroes: list[Hero] = []
points: list[Allowable] = []
setups: list[Setup] = []
configurations: list[Configuration] = []

# Number of specific obstacles in terrain:
num_lava_obstacles: int = None
num_water_obstacles: int = None
num_rubble_obstacles: int = None
num_flying_obstacles: int = None

# Only certain maps are needed, assume False unless proved True:
need_basic_map = False
need_lava_map = False
need_water_map = False
need_rubble_map = False
need_flying_map = False

# =================================================================================================
# CODES & IDS
# =================================================================================================
# Terrain codes
code_lava = Board_Codes.lava_code.value
code_water = Board_Codes.water_code.value
code_rubble = Board_Codes.rubble_code.value
code_ice = Board_Codes.lava_code.value
code_obstacle = Board_Codes.obstacle_code.value
code_empty = Board_Codes.empty_square_code.value

# Monster codes
monster_codes = [Monsters_Codes.monster1.value, Monsters_Codes.monster2.value, Monsters_Codes.monster3.value, Monsters_Codes.monster4.value]

# Terrain Map Ids
map_type_basic = Terrain_Codes.basic_terrain.value
map_type_lava = Terrain_Codes.lava_walker.value
map_type_water = Terrain_Codes.water_walker.value
map_type_rubble = Terrain_Codes.rubble_walker.value
map_type_flying = Terrain_Codes.flying_hero.value

# Map Matchup Ids
map_match_basic = Map_Matchups.basic.value
map_match_lava = Map_Matchups.lava.value
map_match_water = Map_Matchups.water.value
map_match_rubble = Map_Matchups.rubble.value
map_match_flying = Map_Matchups.flying.value
map_match_lava_basic = Map_Matchups.lava_basic.value
map_match_water_basic = Map_Matchups.water_basic.value
map_match_rubble_basic = Map_Matchups.rubble_basic.value
map_match_flying_basic = Map_Matchups.flying_basic.value
map_match_flying_lava = Map_Matchups.flying_lava.value
map_match_flying_water = Map_Matchups.flying_water.value
map_match_flying_rubble = Map_Matchups.flying_rubble.value
map_matches = [map_match_basic, map_match_lava, map_match_water, map_match_rubble, map_match_lava_basic, map_match_water_basic, map_match_rubble_basic, map_match_flying_basic, map_match_flying_lava, map_match_flying_water, map_match_flying_rubble]

# Attack Type codes
# melee_code = Attack_Types.melee
# range_code = Attack_Types.ranged
# pirate_code = Attack_Types.pirate
# magic_code = Attack_Types.magic

# =================================================================================================
# INIT METHODS
# =================================================================================================
# Use a list comprehension to convert each string into a list of characters
def parse_input(input: list[str]):
    board = [list(row) for row in input]
    return board

# =================================================================================================
# Remove spaces and convert to uppercase
def format_input(input: list[str]):
    new_input = []
    for item in input:
        new_input.append(item.upper().replace(' ', ''))
    return new_input

# =================================================================================================
# Parses the terrain and position board inputs, counts num obstacles in board
def init_input_boards():
    global num_lava_obstacles, num_water_obstacles, num_rubble_obstacles, num_flying_obstacles

    def count_obstacles(board: list[list[chr]], chars: list[chr]) -> int:
        lower_chars = [c.lower() for c in chars]
        count = 0
        for row in board:
            for char in row:
                if char.lower() in lower_chars:
                    count += 1
        return count

    # Parse input boards from list of strings to lists of list of characters:
    s = Setup()
    s.board_positions = parse_input(format_input(input_board_positions))
    s.board_terrain = parse_input(format_input(input_board_terrain))
    setups.append(s)

    # board_terrain = parse_input(format_input(input_board_terrain))
    # board_positions = parse_input(format_input(input_board_positions))

    for r in s.board_terrain:
        print(r)
    print("")
    for r in s.board_positions:
        print(r)
    print("")

    # Count specific number of obstacles:
    num_lava_obstacles = count_obstacles(s.board_terrain, [code_lava])
    num_water_obstacles = count_obstacles(s.board_terrain, [code_water])
    num_rubble_obstacles = count_obstacles(s.board_terrain, [code_rubble])
    num_flying_obstacles = num_lava_obstacles + num_water_obstacles + num_rubble_obstacles

# =================================================================================================
# Inits if certain maps are needed.
# Only need a lava map if there are lava obstacles and a lava walking pivot
def init_needed_maps() -> list[int]:
    global need_basic_map, need_lava_map, need_water_map, need_rubble_map, need_flying_map

    for hero in input_heroes:
        if hero.terrain_id == map_type_basic:
            need_basic_map = True
        if hero.terrain_id == map_type_lava and hero.pivot and num_lava_obstacles > 0:
            need_lava_map = True
        if hero.terrain_id == map_type_water and hero.pivot and num_water_obstacles > 0:
            need_water_map = True
        if hero.terrain_id == map_type_rubble and hero.pivot and num_rubble_obstacles > 0:
            need_rubble_map = True
        if hero.terrain_id == map_type_flying and hero.pivot and num_flying_obstacles > 0:
            need_flying_map = True

# =================================================================================================
# Gets all the maps that will be needed
def init_maps():
    global maps

    # Init the different types of maps. Only need to init if they are going to be used.
    # Init basic map
    obstacles_basic_codes = [code_obstacle, code_lava, code_water, code_rubble]
    board_obstacles_basic = get_obstacle_board(setups[0].board_terrain, setups[0].board_positions, obstacles_basic_codes)
    map_basic: Map = Map(map_type_basic, "Basic", board_obstacles_basic)

    # Init lava map
    map_lava = None
    if need_lava_map:
        obstacles_lava_codes = [code_obstacle, code_water, code_rubble]
        board_obstacles_lava = get_obstacle_board(setups[0].board_terrain, setups[0].board_positions, obstacles_lava_codes)
        map_lava: Map = Map(map_type_lava, "Lava", board_obstacles_lava)

    # Init water map
    map_water = None
    if need_water_map:
        obstacles_water_codes = [code_obstacle, code_lava, code_rubble]
        board_obstacles_water = get_obstacle_board(setups[0].board_terrain, setups[0].board_positions, obstacles_water_codes)
        map_water: Map = Map(map_type_water, "Water", board_obstacles_water)

    # Init rubble map
    map_rubble = None
    if need_rubble_map:
        obstacles_rubble_codes = [code_obstacle, code_lava, code_water]
        board_obstacles_rubble = get_obstacle_board(setups[0].board_terrain, setups[0].board_positions, obstacles_rubble_codes)
        map_rubble: Map = Map(map_type_rubble, "Rubble", board_obstacles_rubble)

    # Init flying map
    map_flying = None
    if need_flying_map:
        obstacles_flying_codes = [code_obstacle]
        board_obstacles_flying = get_obstacle_board(setups[0].board_terrain, setups[0].board_positions, obstacles_flying_codes)
        map_flying: Map = Map(map_type_flying, "Flying", board_obstacles_flying)

    maps = [map_basic, map_lava, map_water, map_rubble, map_flying]

# =================================================================================================
# Inits all the hero objects based on the hero inputs
def init_heroes():
    global heroes
    id = 0
    
    for hero in input_heroes:
        new_hero = get_hero(hero)
        new_hero.id = id
        new_hero.starting_point = new_hero.get_hero_pos(input_board_positions)
        # Only need to set hero section and pivot points if he can be a pivot:
        if new_hero.pivot:
            # Assume the hero's map is basic:
            new_hero.section = maps[map_type_basic].get_section_of_point(new_hero.starting_point)
            new_hero.pivot_points = maps[map_type_basic]. get_points_in_section(new_hero.section)
            # If the hero is a special walker and that obstacle is present in the terrain, then set:
            if new_hero.terrain_id == map_type_lava and num_lava_obstacles > 0:
                new_hero.section = maps[new_hero.terrain_id].get_section_of_point(new_hero.starting_point)
                new_hero.pivot_points = maps[map_type_lava]. get_points_in_section(new_hero.section)
            elif new_hero.terrain_id == map_type_water and num_water_obstacles > 0:
                new_hero.section = maps[new_hero.terrain_id].get_section_of_point(new_hero.starting_point)
                new_hero.pivot_points = maps[map_type_water]. get_points_in_section(new_hero.section)
            elif new_hero.terrain_id == map_type_rubble and num_rubble_obstacles > 0:
                new_hero.section = maps[new_hero.terrain_id].get_section_of_point(new_hero.starting_point)
                new_hero.pivot_points = maps[map_type_rubble]. get_points_in_section(new_hero.section)
            elif new_hero.terrain_id == map_type_flying and num_flying_obstacles > 0:
                new_hero.section = maps[new_hero.terrain_id].get_section_of_point(new_hero.starting_point)
                new_hero.pivot_points = maps[map_type_flying]. get_points_in_section(new_hero.section)
        heroes.append(new_hero)
        id = id + 1

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
    final_board = [[code_empty for _ in range(cols)] for _ in range(rows)]
    
    # Iterate through each position in the boards
    for i in range(rows):
        for j in range(cols):
            # Check if the terrain board has an obstacle
            if board_terrain[i][j] in obstacles:
                final_board[i][j] = code_obstacle
            # Check if the position board has a monster character
            elif board_pos[i][j] in monster_codes:
                final_board[i][j] = code_obstacle
            # Otherwise, keep the square empty
            else:
                final_board[i][j] = code_empty
    
    return final_board

# =================================================================================================
# 
def init_points():
    global points

    points_basic = None
    points_lava = None
    points_water = None
    points_rubble = None
    points_flying = None
    points_lava_basic = None
    points_water_basic = None
    points_rubble_basic = None
    points_flying_basic = None
    points_flying_lava = None
    points_flying_water = None
    points_flying_rubble = None

    if need_basic_map:
        points_basic = Allowable(map_match_basic, hero_map=maps[map_type_basic])
    if need_lava_map:
        points_lava = Allowable(map_match_lava, hero_map=maps[map_type_lava])
        if need_basic_map:
            points_lava_basic = Allowable(map_match_lava_basic, maps[map_type_lava], maps[map_type_basic])
    if need_water_map:
        points_water = Allowable(map_match_water, hero_map=maps[map_type_water])
        if need_basic_map:
            points_water_basic = Allowable(map_match_water_basic, maps[map_type_water], maps[map_type_basic])
    if need_rubble_map:
        points_rubble = Allowable(map_match_rubble, hero_map=maps[map_type_rubble])
        if need_basic_map:
            points_rubble_basic = Allowable(map_match_rubble_basic, maps[map_type_rubble], maps[map_type_basic])
    if need_flying_map:
        points_flying = Allowable(map_match_flying, hero_map=maps[map_type_flying])
        if need_basic_map:
            points_flying_basic = Allowable(map_match_flying_basic, maps[map_type_flying], maps[map_type_basic])
        if need_lava_map:
            points_flying_lava = Allowable(map_match_flying_lava, maps[map_type_flying], maps[map_type_lava])
        if need_water_map:
            points_flying_water = Allowable(map_match_flying_water, maps[map_type_flying], maps[map_type_water])
        if need_rubble_map:
            points_flying_rubble = Allowable(map_match_flying_rubble, maps[map_type_flying], maps[map_type_rubble])

    points = [points_basic, points_lava, points_water, points_rubble, points_flying, points_lava_basic, points_water_basic, points_rubble_basic, points_flying_basic, points_flying_lava, points_flying_water, points_flying_rubble]

# =================================================================================================
# 
def init_setups() -> list[Setup]:
    # for h in heroes:
    #     if h.push > 0
    list = []

    return list

# =================================================================================================
# VALIDATION METHODS
# =================================================================================================
# Determine if inputs are valid
def validate_inputs():
    #TODO
    return True

# =================================================================================================
# LOOP METHODS
# =================================================================================================
# 
def get_next_hero_id(pivot_id: int, current_id: int) -> int:
    for h in heroes[current_id:]:
        if h.id == pivot_id:
            continue
        else:
            return h.id
        
def get_next_hero_id_list(pivot_id: int) -> list[int]:
    list = []
    for h in heroes:
        if h.id != pivot_id:
            list.append(h.id)
    return list

def get_map_matchup_list(pivot_id: int) -> list[int]:
    list = []
    for h in heroes:
        if h.id != pivot_id:
            id = get_map_matchup(pivot_id, h.id)
            list.append(id)
    return list

def get_map_list(pivot_id: int) -> list[int]:
    list = []
    for h in heroes:
        if h.id != pivot_id:
            list.append(h.terrain_id)
    return list

def get_map_matchup(pivot_id: int, hero_id: int) -> int:
    if heroes[pivot_id].terrain_id == map_type_lava:
        if heroes[hero_id].terrain_id == map_type_lava or heroes[hero_id].terrain_id == map_type_flying:
            return map_match_lava
    if heroes[pivot_id].terrain_id == map_type_water:
        if heroes[hero_id].terrain_id == map_type_water or heroes[hero_id].terrain_id == map_type_flying:
            return map_match_water
    if heroes[pivot_id].terrain_id == map_type_rubble:
        if heroes[hero_id].terrain_id == map_type_rubble or heroes[hero_id].terrain_id == map_type_flying:
            return map_match_rubble
    if heroes[pivot_id].terrain_id == map_type_flying:
        if heroes[hero_id].terrain_id == map_type_lava:
            return map_match_flying_lava
        if heroes[hero_id].terrain_id == map_type_water:
            return map_match_flying_water
        if heroes[hero_id].terrain_id == map_type_rubble:
            return map_match_flying_rubble
        if heroes[hero_id].terrain_id == map_type_flying:
            return map_match_flying
   
    return map_match_basic


def init_configurations() -> list[Configuration]:
    count = 0

    file_path = "logs/configs.txt"
    configs = []
    
    pivots : list[Hero] = []

    for h in heroes:
        if h.pivot == True:
            pivots.append(h)

    num_heroes = len(heroes)

    start_time = time.time()

    with open(file_path, 'w') as file:
        # Loop through pivot candidates
        for p in pivots:
            pivot_points = p.pivot_points
            pivot_start = p.starting_point
            pivot_start_zone = maps[p.terrain_id].get_zone_id_of_point(pivot_start)
            moveable_hero_list = get_next_hero_id_list(p.id)
            map_matchup_list = get_map_matchup_list(p.id)
            map_list = get_map_list(p.id)


            # Loop through pivot points
            for pivot_current in pivot_points:
                pivot_end_zone = maps[p.terrain_id].get_zone_id_of_point(pivot_current)

                if num_heroes < 2: # Only the pivot is on this board
                    configs.append(get_configuration(None, pivot_current))
                    count = count + 1
                    continue

                hero_start_zone = maps[map_list[0]].get_zone_id_of_point(heroes[moveable_hero_list[0]].starting_point)
                
                # Loop through 1st moveable hero points
                for h1p in points[map_matchup_list[0]].points[pivot_start_zone][pivot_end_zone][hero_start_zone]:
                    
                    if num_heroes < 3: # If there is only the pivot and 1 moveable hero on this board
                        configs.append(get_configuration(None, pivot_current, h1p))
                        count = count + 1
                        continue

                    hero_start_zone = maps[map_list[1]].get_zone_id_of_point(heroes[moveable_hero_list[1]].starting_point)

                    # Loop through 2nd moveable hero points
                    for h2p in points[map_matchup_list[1]].points[pivot_start_zone][pivot_end_zone][hero_start_zone]:

                        if num_heroes < 4: # If there is only the pivot and 2 moveable heroes on this board
                            configs.append(get_configuration(None, pivot_current, h1p, h2p))
                            count = count + 1
                            continue

                        hero_start_zone = maps[map_list[2]].get_zone_id_of_point(heroes[moveable_hero_list[2]].starting_point)

                        # Loop through 3rd moveable hero points
                        for h3p in points[map_matchup_list[2]].points[pivot_start_zone][pivot_end_zone][hero_start_zone]:

                            if num_heroes < 5: # If there is only the pivot and 3 moveable heroes on this board
                                configs.append(get_configuration(None, pivot_current, h1p, h2p, h3p))
                                count = count + 1
                                continue

                            hero_start_zone = maps[map_list[3]].get_zone_id_of_point(heroes[moveable_hero_list[3]].starting_point)

                            # Loop through 4th moveable hero points
                            for h4p in points[map_matchup_list[3]].points[pivot_start_zone][pivot_end_zone][hero_start_zone]:

                                if num_heroes < 6: # If there is only the pivot and 4 moveable heroes on this board
                                    configs.append(get_configuration(None, pivot_current, h1p, h2p, h3p, h4p))
                                    count = count + 1
                                    continue

                                hero_start_zone = maps[map_list[4]].get_zone_id_of_point(heroes[moveable_hero_list[4]].starting_point)

                                # Loop through 5th moveable hero points
                                for h5p in points[map_matchup_list[4]].points[pivot_start_zone][pivot_end_zone][hero_start_zone]:
                                    config = get_configuration(None, pivot_current, h1p, h2p, h3p, h4p, h5p)
                                    configs.append(config)
                                    # file.write(f"{count} : 0:{pivot_current}, 1:{h1p}, 2:{h2p}, 3:{h3p}, 4:{h4p}, 5:{h5p}\n")
                                    count = count + 1
                                    
    end_time = time.time()
    duration = end_time - start_time

    print(f"\n{count} calculations for {duration:.2f} seconds. {len(heroes)} Heroes, {len(pivots)} pivots\n")
    return configs

def get_configuration(board, *args) -> Configuration:
    positions = []
    for arg in args:
        positions.append(arg)

    config = Configuration(positions = positions, board_positions = board)
    return config

# =================================================================================================
# PRINT METHODS
# =================================================================================================
#
def output_to_debug_log(file: str, allowable: Allowable):
    # Open the file for writing
    filename = f"logs/{file}.txt"
    debug_file = open(filename, "w")

    # Iterate through each element in the 3D list and write to the file
    for i in range(len(allowable.points)):
        for j in range(len(allowable.points[0])):
            debug_file.write(f"\n****************\nPivot path: {i} to {j}\n****************\n")
            for k in range(len(allowable.points[0][0])):
                debug_file.write(f"{k:02} : {allowable.points[i][j][k]}\n")

    # Close the file
    debug_file.close()

def output_to_debug_log_new(file: str, allowable: Allowable):
    # Open the file for writing
    filename = f"logs/{file}.txt"
    debug_file = open(filename, "w")

    # Iterate through each element in the 3D list and write to the file
    for i in range(len(allowable.points)):
        for j in range(len(allowable.points[i])):
            if allowable.points[i][j] is not None and len(allowable.points[i][j]) > 0:
                debug_file.write(f"\n************************\nPivot {i} to {j}\n************************\n")
                for k in range(len(allowable.points[i][j])):
                    debug_file.write(f"\n{k:02} : ")
                    if allowable.points[i][j][k] is None:
                        debug_file.write("None")
                    else:
                        for l in range(len(allowable.points[i][j][k])):
                            debug_file.write(f"{allowable.points[i][j][k][l]}")
                            if l < len(allowable.points[i][j][k]) - 1:
                                debug_file.write(", ")
                debug_file.write(f"\n")

    # Close the file
    debug_file.close()

# =================================================================================================
# For printing out all points in a format that can be imported into Excel for comparison
def output_debug_log_excel_basic(file: str, allowable: Allowable):
    filename = f"logs/{file}.txt"

    # Open the debug file for writing
    with open(filename, "w") as debug_file:

        debug_file.write(f"\t")

        # Print paths as first row
        for s in range(len(allowable.points)):
            for e in range(len(allowable.points[0])):
                path_str = f"{s} to {e}"
                debug_file.write(f"{path_str} \t ")

        debug_file.write(f"\n")
        
        num_zones = len(allowable.points[0][0])
        num_pivot_zones = len(allowable.points)
        for h in range(num_zones):
            zone_output = f"{h}\t"
            for s in range(num_pivot_zones):
                for e in range(num_pivot_zones):
                    if allowable.points[s][e][h] is None:
                        path_points = []
                        points_str = str(path_points).replace("[", "").replace("]", "")
                        zone_output += f"{points_str} "
                    else:
                        for p in range(len(allowable.points[s][e][h])):
                            path_points = allowable.points[s][e][h]
                            points_str = str(path_points).replace("[", "").replace("]", "")
                            zone_output += f"{points_str}, "

                    # Remove the trailing tab and space
                    zone_output = zone_output.rstrip(', ')
                    zone_output += '\t'

            # Write the formatted output to the debug file
            debug_file.write(f"{zone_output}\n")

# =================================================================================================
# SCRIPT
# =================================================================================================

# -------------------------------------------------------------------------------------------------
# Setup:
if validate_inputs is False:
    print("Error in inputs. Exiting program.")
    exit()

# -------------------------------------------------------------------------------------------------
random_map = Random_Map()

# -------------------------------------------------------------------------------------------------
# Init
init_input_boards()
init_needed_maps()
init_maps()
init_heroes()
init_setups()


# hero_pos: list[tuple] = []
# for h in heroes:
#     hero_pos.append(h.starting_point)

maps[map_type_basic].print_map_with_zones()
# maps[map_type_lava].print_map_with_zones()
# maps[map_type_water].print_map_with_zones()
# maps[map_type_rubble].print_map_with_zones()
# maps[map_type_flying].print_map_with_zones()

print("chokepoints: ", maps[map_type_basic].chokepoints)
print("deadends: ", maps[map_type_basic].deadends)
for z in maps[map_type_basic].zones:
    print(z)

# maps[map_type_basic].print_map_with_terrains(board_terrain)
# maps[map_type_basic].print_map_with_positions(hero_pos)

init_points()

output_to_debug_log_new("basic", points[map_match_basic])
# output_to_debug_log("lava_basic", points[map_match_lava_basic])
# output_to_debug_log("water_basic", points[map_match_water_basic])
# output_to_debug_log("rubble_basic", points[map_match_rubble_basic])
# output_to_debug_log("flying_basic", points[map_match_flying_basic])
# output_to_debug_log("flying_lava", points[map_match_flying_lava])
# output_to_debug_log("flying_water", points[map_match_flying_water])
# output_to_debug_log("flying_rubble", points[map_match_flying_rubble])
# output_debug_log_excel_basic("lava_basic_excel", points[map_match_lava_basic])

init_configurations()

