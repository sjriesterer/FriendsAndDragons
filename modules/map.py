from enums import Board_Codes

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

    def print_map_with_zones(self):
        print("\nZone Map: ", self.name)

        # Track which zones have been printed in this row
        printed_zones = []

        # Print column numbers
        print('    ', end='')
        for col in range(len(self.board[0])):
            if col == 10:
                print(" ", end= "")
            print(f'{col:2}', end=' ')
        print()

        print("------", end = "")
        for i in range(len(self.board[0])):
            print("---", end = "")
        print("\n", end = "")

        # Loop through the rows
        for i in range(len(self.board)):
            print(f'{i:2} | ', end='')

            # Loop through the columns
            for j in range(len(self.board[i])):
                found = False
                # Check each zone
                for zone in self.zones:
                    # Find the zone that contains the current board position
                    if (i, j) in zone.points and zone.id not in printed_zones:
                        # Print the zone id as a 2-digit number
                        print(f'{zone.id:02}', end=' ')
                        found = True
                        printed_zones.append(zone.id)
                        break

                # If no zone contains the current position, check for obstacle
                if not found:
                # else:
                    if self.board[i][j] == Board_Codes.obstacle_code.value:
                        print('[]', end=' ')
                    else:
                        print('..', end=' ')

            print('|')

        print("------", end = "")
        for i in range(len(self.board[0])):
            print("---", end = "")
        print("\n")
    
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