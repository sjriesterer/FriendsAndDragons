# This class includes all the inputs for the program

class Inputs():
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
    # List of heros on the board.
    # The index of the hero matches the index on the board.
    heroes = [
        "monk", "knight", "mage", "rogue", "hunter", "pirate"
    ]

# =================================================================================================
    # List of index ids of the heroes who can be the pivot.
    # A smaller list of candidates will speed up the results.
    # pivot_candidates = [] # If list is blank, all heros are pivot candidates
    pivot_candidates = [0,1] 

# =================================================================================================

    # basic_map = 0
    # lava_map = 1
    # water_map = 2
    # flying_map = 3
    # rubble_map = 4

    hero_terrains = [
        0,1,0,1,0,0
    ]