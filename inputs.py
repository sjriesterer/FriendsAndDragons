# This class includes all the inputs for the program

from enums import Map_Codes
from modules.hero import Hero


class Inputs():
    basic_map_id = Map_Codes.basic_map.value
    lava_map_id = Map_Codes.lava_map.value
    water_map_id = Map_Codes.water_map.value
    flying_map_id = Map_Codes.flying_map.value
    rubble_map_id = Map_Codes.rubble_map.value

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

# Map codes:
# basic_map = 0 : No special walking abilities
# lava_map = 1 : Can walk on lava
# water_map = 2 : Can walk on water
# flying_map = 3 : Can fly
# rubble_map = 4 : Can traverse through rubble

    heroes = [
        Hero(cls="monk",   name="Blaise", pivot=True, push = 3, mighty_blow=2),
        Hero(cls="barbarian", board_map_id=water_map_id),
        Hero(cls="mage", name="Elethas1", mighty_blow=2),
        Hero(cls="mage", name= "Elethas2", mighty_blow=1),
        Hero(cls="healer"),
        Hero(cls="rogue",  name="Gloom", pivot=True, board_map_id=rubble_map_id, rubble=1, tumble=2)
    ]
