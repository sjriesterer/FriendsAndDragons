class Zone:
    def __init__(self, section, id, is_deadend=False):
        self.section = section
        self.id = id
        self.is_deadend = is_deadend
        self.points = []
        self.connected_zones = []
        self.connected_deadend_zones = []
    def __str__(self):
        return f'{self.id} : Section: {self.section}, IsDeadend: {self.is_deadend}, Connected Zones: {self.connected_zones}, Conn.Deadends: {self.connected_deadend_zones}\n\tPoints: {self.points}'
