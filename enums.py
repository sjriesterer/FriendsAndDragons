from enum import Enum

class Board(Enum):
    # board terrain legend
    lava = 'L'
    water = 'W'
    rubble = 'R'
    ice = 'I'
    obstacle = 'O'
    empty_square = '.'
    monster = 'M'

    def __eq__(self, other):
            if isinstance(other, Board):
                return self.value == other.value
            elif isinstance(other, str):
                return self.value == other
            return False

class Monsters(Enum):
    # Monsters
    monster1 = 'A'
    monster2 = 'B'
    monster3 = 'C'
    monster4 = 'D'

class Hero_Class(Enum):
    monk = ''
    barbarian = ''
    assassin = ''
    rouge = ''
    pirate = ''
    knight = ''
    warrior = ''
    guardian = ''
    ranger = ''
    archer = ''
    hunter = ''
    jav = ''
    mage = ''
    elemental = ''
    warlock = ''
    wizard = ''
    healer = ''
    paladin = ''
    druid = ''
    bard = ''
    princess = ''

class Attack_Types:
    melee: int = 1
    ranged: int = 2
    pirate: int = 3
    magic: int = 4
