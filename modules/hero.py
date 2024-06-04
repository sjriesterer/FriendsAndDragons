class MyClass:
    def __init__(self):
        self.name: str = None
        self.move: int = None
        self.attack: int = None
        self.attack_type: int = None
        self.support: int = None
        self.support_type: int = None
        self.lava: bool = False
        self.water: bool = False
        self.rubbler: int = 0
        self.push: int = 0
        self.tumble: int = 0
        self.mighty_blow: int = 0

    def describe(self):
        return f"Character: {self.name}, Move: {self.move}, Attack: {self.attack}"