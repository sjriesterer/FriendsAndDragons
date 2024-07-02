class Hero:
    def __init__(self):
        self.id = 0
        self.name: str = None
        self.pivot = False
        self.move: int = None
        self.attack: int = None
        self.attack_type: int = None
        self.support: int = None
        self.support_type: int = None
        self.fly = False
        self.lava: bool = False
        self.water: bool = False
        self.rubbler: int = 0
        self.push: int = 0
        self.tumble: int = 0
        self.mighty_blow: int = 0
        self.section = 0
        self.starting_point: tuple = (0,0)
        self.board_map_id = 0
        self.board_map = 0
        self.pivot_points = []

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Attack: {self.attack}, Start Pos: {self.starting_point}, Current Pos: {self.current_point}'
    
    # Returns the point of the hero id on the board
    def get_hero_pos(self, board: list[list[str]]):
        id_str = str(self.id)
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == id_str:
                    return (row_index, col_index)
        return None  # Return None if the id is not found
