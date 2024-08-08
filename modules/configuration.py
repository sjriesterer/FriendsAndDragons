
class Configuration:

    def __init__(self, positions: list[tuple], board_positions: list[list[chr]] = None) -> None:
        self.positions = positions
        self.board_positions = board_positions
