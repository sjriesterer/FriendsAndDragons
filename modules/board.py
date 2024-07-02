class Board:
    def __init__(self, name="", board=None, chokepoints=None, deadends=None, zones=None):
        self.name = name
        self.board = board if board is not None else []
        self.chokepoints = chokepoints if chokepoints is not None else []
        self.deadends = deadends if deadends is not None else []
        self.zones = zones if zones is not None else []

    def print_board(self):
        # Print column numbers
        print('    ', end='')
        for col in range(len(self.board[0])):
            print(f'{col:2}', end='')
        print()
        print(" ---------------------------------")

        # Print board rows with row numbers
        for i, row in enumerate(self.board):
            print(f'{i:2} | ', end='')
            print(' '.join(row))
