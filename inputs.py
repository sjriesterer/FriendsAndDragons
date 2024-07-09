# This class includes all the inputs for the program

from enums import Terrain_Codes
from modules.hero import Hero
import random

class Inputs():
    basic_map_id = Terrain_Codes.basic_terrain.value
    lava_map_id = Terrain_Codes.lava_walker.value
    water_map_id = Terrain_Codes.water_walker.value
    flying_map_id = Terrain_Codes.flying_hero.value
    rubble_map_id = Terrain_Codes.rubble_walker.value

# =================================================================================================
    # The board layout. (case insensitive, spaces will be eliminated)
    # o = Obstacle
    # l = Lava
    # i = Ice
    # w = Water
    # r = Rubble
    # . = Free square
    terrain2 = [
        "..o...",
        "ooo...",
        ".....l",
        "oo..ll",
        ".....i",
        ".....i",
        "www...",
        "l...rr"
    ]
    
    terrain = [
        "..o...o.....",
        "ooo...o.rrr.",
        ".....lo.....",
        "oor.llollll.",
        "............",
        "...ll.ooo.oo",
        "lll...o.....",
        "l...rro....."
    ]


# =================================================================================================
    # The positions of the monsters and heros on the board. (case insensitive, spaces will be eliminated)
    # Heros are ids 0-6
    # Monster ids are any letter
    # Empty squares are '.'
    positions = [
        "0...........",
        "...........5",
        "21..........",
        "............",
        "..34........",
        "............",
        "............",
        "............"
    ]

# =================================================================================================
# Init the heroes. You only need to input the variables that differ from the defaults:
# 
# Variable      Type        Default     Description
#------------------------------------------------------------------------------
# cls           ctring      <required>  Class of hero
# name          string      ""          Name of hero (only for display purposes)
# pivot         bool        False       Is a pivot candidate (will evaulate this hero as the pivot)
# rubble        int         0           How many rubble walk talents
# push          int         0           How many pus talents
# tumble        int         0           How many tumble talents
# mighty_blow   int         0           How many mighty blow talents
# board_map_id  int         basic map   The id of the map this hero traverses on

# Terrain codes:
# basic_terrain = 0 : No special walking abilities
# lava_walker = 1 : Can walk on lava
# water_walker = 2 : Can walk on water
# rubble_walker = 4 : Can traverse through rubble
# flying_hero = 3 : Can fly

    heroes = [
        Hero(cls="monk",   name="Blaise", pivot=True, push = 3, mighty_blow=2),
        Hero(cls="barbarian", terrain_id=water_map_id),
        Hero(cls="mage", name="Elethas1", mighty_blow=2),
        Hero(cls="mage", name= "Elethas2", mighty_blow=1),
        Hero(cls="healer", terrain_id=lava_map_id),
        Hero(cls="rogue",  name="Gloom", pivot=True, terrain_id=rubble_map_id, rubble=1, tumble=2)
    ]

    def get_random_terrain(self, rows: int, cols: int, num_O: int = None, num_L: int = None, num_W: int = None, num_R: int = None) -> list[list[str]]:
        terrain = [['.' for _ in range(cols)] for _ in range(rows)]

        def place_group(char, count):
            placed = 0
            attempts = 0
            max_attempts = 100
            
            while placed < count and attempts < max_attempts:
                attempts += 1
                start_row = random.randint(0, rows - 1)
                start_col = random.randint(0, cols - 1)
                orientation = random.choice(['horizontal', 'vertical'])
                
                if orientation == 'vertical' and start_row + count - placed <= rows:
                    if all(terrain[start_row + i][start_col] == '.' for i in range(count - placed)):
                        for i in range(count - placed):
                            terrain[start_row + i][start_col] = char
                        placed = count
                        return
                
                elif orientation == 'horizontal' and start_col + count - placed <= cols:
                    if all(terrain[start_row][start_col + i] == '.' for i in range(count - placed)):
                        for i in range(count - placed):
                            terrain[start_row][start_col + i] = char
                        placed = count
                        return

            # Place remaining characters individually if we run out of attempts
            while placed < count:
                empty_positions = [(r, c) for r in range(rows) for c in range(cols) if terrain[r][c] == '.']
                if not empty_positions:
                    break
                r, c = random.choice(empty_positions)
                terrain[r][c] = char
                placed += 1

        def place_scattered(char, count):
            empty_positions = [(r, c) for r in range(rows) for c in range(cols) if terrain[r][c] == '.']
            positions = random.sample(empty_positions, min(count, len(empty_positions)))
            for r, c in positions:
                terrain[r][c] = char

        if num_L is not None:
            place_group('L', num_L)
        if num_W is not None:
            place_group('W', num_W)
        if num_R is not None:
            place_group('R', num_R)
        if num_O is not None:
            place_scattered('O', num_O)

        return terrain

    def get_random_positions(self, terrain: list[list[str]], rows: int, cols: int, num_heros: int) -> list[list[str]]:
        # Initialize the board with '.' for all positions
        board = [['.' for _ in range(cols)] for _ in range(rows)]
        
        # Find all empty positions ('.') on the terrain
        empty_positions = [(r, c) for r in range(rows) for c in range(cols) if terrain[r][c] == '.']
        
        if len(empty_positions) < num_heros:
            raise ValueError("Not enough empty positions to place the heroes")
        
        # Shuffle the empty positions and pick the first `num_heros` positions
        random.shuffle(empty_positions)
        hero_positions = empty_positions[:num_heros]
        
        # Place the heroes on the board with incremental numbers
        for i, (r, c) in enumerate(hero_positions):
            board[r][c] = str(i + 1)
        
        return board

    def convert_to_string_list(self, char_list: list[list[str]]) -> list[str]:
        return ["".join(row) for row in char_list]