from enum import Enum

class Board_Codes(Enum):
    lava_code = 'L'
    water_code = 'W'
    rubble_code = 'R'
    ice_code = 'I'
    obstacle_code = 'O'
    empty_square_code = '.'
    monster_code = 'M'

class Terrain_Codes(Enum):
    basic_terrain = 0
    lava_walker = 1
    water_walker = 2
    rubble_walker = 3
    flying_hero = 4

# A matchup is a relationship between the pivot's map and the movable hero's map.
# If the pivot is a lava walker and the movable hero is just basic, then the matchup
# is lava_basic. If both are water walkers than the matchup is just water.
# If the pivot is a water walker and the hero is a lava walker, then it is a
# water_basic match up because the hero's lava walking ability is not used.
# When it is time to iterate through the allowable points for the configurations,
# these ids are used to determine the allowable points for the movable hero.
# Each matchup will have a different set of allowable points for that hero because
# of different dynamics of where the pivot can move to as well as the movable hero.
class Map_Matchups(Enum):
    basic = 0
    lava = 1
    water = 2
    rubble = 3
    flying = 4
    lava_basic = 5
    water_basic = 6
    rubble_basic = 7
    flying_basic = 8
    flying_lava = 9
    flying_water = 10
    flying_rubble = 11

class Monsters_Codes(Enum):
    # Monsters
    monster1 = 'A'
    monster2 = 'B'
    monster3 = 'C'
    monster4 = 'D'

class Hero_Class(Enum):
    monk = 'mo'
    barbarian = 'barb'
    assassin = 'as'
    rouge = 'ro'
    pirate = 'pi'
    knight = 'k'
    warrior = 'warr'
    guardian = 'g'
    ranger = 'ra'
    archer = 'ar'
    hunter = 'h'
    jav = 'j'
    mage = 'm'
    elemental = 'e'
    warlock = 'warl'
    wizard = 'wi'
    healer = 'h'
    paladin = 'pa'
    druid = 'd'
    bard = 'bard'
    princess = 'pr'

class Attack_Types:
    melee_4: int = 0
    melee_8: int = 1
    ranged_4: int = 2
    ranged_8: int = 3
    ranged_jav: int = 4
    pirate: int = 5
    magic_4: int = 6
    magic_8: int = 7

class Support_Types:
    princess: int = 0
    heal_4: int = 1
    heal_8: int = 2