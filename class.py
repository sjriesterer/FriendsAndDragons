class MyClass:
    def __init__(self):
        self.name = None
        self.move = None
        self.attack = None
        self.attack_type = None
        self.support = None
        self.support_type = None
        self.lava = False
        self.water = False
        self.rubbler = 0
        self.push = 0
        self.tumble = 0
        self.mighty_blow = 0

    def describe(self):
        return f"Character: {self.name}, Move: {self.move}, Attack: {self.attack}"