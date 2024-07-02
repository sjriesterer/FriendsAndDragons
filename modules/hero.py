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