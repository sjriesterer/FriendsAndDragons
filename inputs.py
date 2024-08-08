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
    terrain1 = [
        "..o...",
        "ooo...",
        ".....l",
        "oo..ll",
        ".....i",
        ".....i",
        "www...",
        "l...rr"
    ]
    
    terrain2 = [
        "..o...o.....",
        "ooo...o.rrr.",
        ".....lo.....",
        "oor.llollll.",
        "............",
        "...ll.ooo.oo",
        "lll...o..www",
        "l...rro...ww"
    ]


    terrain3 = [
        "..ooo.....",
        ".o........",
        "o...wwwww.",
        "o.ooo...l.",
        "o.oo....o.",
        "ollooo....",
        "...o......",
        ".oo..l.rrr",
        "...oo.....",
        "....o.....",
    ]

    terrain4 = [
        "..ooo.....",
        ".o........",
        "o...wwwwww",
        "o.ooo...l.",
        "o.oo....o.",
        "ollooo....",
        "...o...r.r",
        "roo..l....",
        "...oo..o..",
        "....o..o.o",
    ]

# =================================================================================================
    terrain = [
        ".rl..w",
        "......",
        ".oo..o",
        ".oo..o",
        ".oo..o",
    ]
    positions = [
        "0..1..",
        "2..3..",
        "4.....",
        "......",
        "......",
    ]
    heroes = [
        Hero(cls="monk",   name="Blaise", pivot=True, terrain_id=lava_map_id, push = 3, mighty_blow=2),
        Hero(cls="barbarian", pivot=True),
        Hero(cls="mage", name="Elethas1", pivot=True, mighty_blow=2),
        Hero(cls="mage", name= "Elethas2", terrain_id=lava_map_id, mighty_blow=1),
        Hero(cls="healer"),
        # Hero(cls="rogue",  name="Gloom", rubble=1, tumble=2),
        # Hero(cls="healer", pivot=True, terrain_id=lava_map_id),
        # Hero(cls="healer", pivot=True, terrain_id=water_map_id),
        # Hero(cls="healer", pivot=True, terrain_id=flying_map_id),
    ]

# =================================================================================================
    # The positions of the monsters and heros on the board. (case insensitive, spaces will be eliminated)
    # Heros are ids 0-6
    # Monster ids are any letter
    # Empty squares are '.'

    positions3 = [
        "1.........",
        "....6.....",
        "..........",
        ".7.......2",
        ".....4....",
        "..........",
        ".5........",
        "......3...",
        "..........",
        "8........0",
    ]

    positions2 = [
        "............",
        "............",
        "............",
        "............",
        "012345678...",
        "............",
        "............",
        "............",
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

    heroes2 = [
        Hero(cls="monk",   name="Blaise", pivot=True, push = 3, mighty_blow=2),
        Hero(cls="barbarian", terrain_id=water_map_id),
        Hero(cls="mage", name="Elethas1", mighty_blow=2),
        Hero(cls="mage", name= "Elethas2", mighty_blow=1),
        Hero(cls="healer", terrain_id=lava_map_id),
        Hero(cls="rogue",  name="Gloom", pivot=True, terrain_id=rubble_map_id, rubble=1, tumble=2),
        Hero(cls="healer", pivot=True, terrain_id=lava_map_id),
        Hero(cls="healer", pivot=True, terrain_id=water_map_id),
        Hero(cls="healer", pivot=True, terrain_id=flying_map_id),
    ]
