from typing import Optional
import copy

class Hero:
    def __init__(self, 
                 cls: str = None, 
                 name: str = "", 
                 pivot: bool = False, 
                 terrain_id: int = 0, 
                 rubble: int = 0, 
                 push: int = 0, 
                 tumble: int = 0, 
                 mighty_blow: int = 0) -> None:
        self.id: int = None
        self.cls: str = cls
        self.name: str = name
        self.pivot: bool = pivot
        self.attack: int = None
        self.attack_type: int = None
        self.support: int = None
        self.support_type: int = None
        self.rubble: int = rubble
        self.push: int = push
        self.tumble: int = tumble
        self.mighty_blow: int = mighty_blow
        self.section: int = None
        self.starting_point: tuple[int, int] = (0, 0)
        self.terrain_id: int = terrain_id
        self.pivot_points = []

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Cls: {self.cls}, Board ID: {self.terrain_id}, Start Pos: {self.starting_point}, section: {self.section}'
    
    # Returns the point of the hero id on the board
    def get_hero_pos(self, board: list[str]):
        id_str = str(self.id)
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == id_str:
                    return (row_index, col_index)
        return None  # Return None if the id is not found

    def copy(self):
        return copy.deepcopy(self)
    