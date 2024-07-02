from enum import Enum

class Board_Codes(Enum):
    lava_code = 'L'
    water_code = 'W'
    rubble_code = 'R'
    ice_code = 'I'
    obstacle_code = 'O'
    empty_square_code = '.'
    monster_code = 'M'

    def __eq__(self, other):
            if isinstance(other, Board_Codes):
                return self.value == other.value
            elif isinstance(other, str):
                return self.value == other
            return False

class Map(Enum):
    basic_map = 0
    lava_map = 1
    water_map = 2
    flying_map = 3
    rubble_map = 4


class Monsters_Codes(Enum):
    # Monsters
    monster1 = 'A'
    monster2 = 'B'
    monster3 = 'C'
    monster4 = 'D'

class Hero_Class(Enum):
    monk = 'mon'
    barbarian = 'brb'
    assassin = 'ass'
    rouge = 'rou'
    pirate = 'pir'
    knight = 'k'
    warrior = 'wrr'
    guardian = 'g'
    ranger = 'ran'
    archer = 'arc'
    hunter = 'h'
    jav = 'j'
    mage = 'm'
    elemental = 'e'
    warlock = 'wrl'
    wizard = 'wiz'
    healer = 'h'
    paladin = 'pal'
    druid = 'd'
    bard = 'brd'
    princess = 'pri'

class Attack_Types:
    melee: int = 1
    ranged: int = 2
    pirate: int = 3
    magic: int = 4
