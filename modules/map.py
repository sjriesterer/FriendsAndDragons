# modules/map.py
class Map:
    def __init__(self, id=0, name="", board=None, chokepoints=None, deadends=None, zones=None):
        self.id = id
        self.name = name
        self.board = board if board is not None else []
        self.chokepoints = chokepoints if chokepoints is not None else []
        self.deadends = deadends if deadends is not None else []
        self.zones = zones if zones is not None else []

    def __str__(self):
        return (f'ID: {self.id}, Name: {self.name}, '
                f'Board: {self.board}, Chokepoints: {self.chokepoints}, '
                f'Deadends: {self.deadends}, Zones: {self.zones}')
