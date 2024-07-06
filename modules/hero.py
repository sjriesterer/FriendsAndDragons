from typing import Optional
import copy

class Hero:
    def __init__(self, cls = None, name = "", pivot=False, board_map_id=0, rubble=0, push=0, tumble=0, mighty_blow=0):
        self.id: Optional[int] = 0
        self.cls: str = cls
        self.name: Optional[str] = name
        self.pivot = Optional[False]
        self.attack: Optional[int] = None
        self.attack_type: Optional[int] = None
        self.support: Optional[int] = None
        self.support_type: Optional[int] = None
        self.rubble: Optional[int] = rubble
        self.push: Optional[int] = push
        self.tumble: Optional[int] = tumble
        self.mighty_blow: Optional[int] = mighty_blow
        self.section: Optional[int] = 0
        self.starting_point: Optional[tuple] = (0,0)
        self.board_map_id: Optional[int] = board_map_id
        self.pivot_points: Optional[any] = []

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Cls: {self.cls}, Board ID: {self.board_map_id}, Start Pos: {self.starting_point}, section: {self.section}'
    
    # Returns the point of the hero id on the board
    def get_hero_pos(self, board: list[list[str]]):
        id_str = str(self.id)
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == id_str:
                    return (row_index, col_index)
        return None  # Return None if the id is not found

    def copy(self):
        return copy.deepcopy(self)
    