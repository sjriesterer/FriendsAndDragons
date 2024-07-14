import random

class Random_Map():
    def __init__(self):
        self.rows = self.get_random_number(8,8)
        self.cols = self.get_random_number(6,6)
        self.num_obstacles = self.get_random_number(4,10)
        self.num_lava = self.get_random_number(8,12)
        self.num_water = self.get_random_number(0,0)
        self.num_rubble = self.get_random_number(0,0)
        self.num_heroes = self.get_random_number(1,6)
        self.board_terrain = self.get_random_terrain()
        self.board_positions = self.get_random_positions()
        self.print_board_terrain()
        self.print_board_positions()

# =================================================================================================
    def get_random_number(self, min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

# =================================================================================================
    def get_random_terrain(self) -> list[list[str]]:
        terrain = [['.' for _ in range(self.cols)] for _ in range(self.rows)]

        def place_group(char, count):
            placed = 0
            attempts = 0
            max_attempts = 100
            
            while placed < count and attempts < max_attempts:
                attempts += 1
                start_row = random.randint(0, self.rows - 1)
                start_col = random.randint(0, self.cols - 1)
                orientation = random.choice(['horizontal', 'vertical'])
                
                if orientation == 'vertical' and start_row + count - placed <= self.rows:
                    if all(terrain[start_row + i][start_col] == '.' for i in range(count - placed)):
                        for i in range(count - placed):
                            terrain[start_row + i][start_col] = char
                        placed = count
                        return
                
                elif orientation == 'horizontal' and start_col + count - placed <= self.cols:
                    if all(terrain[start_row][start_col + i] == '.' for i in range(count - placed)):
                        for i in range(count - placed):
                            terrain[start_row][start_col + i] = char
                        placed = count
                        return

            # Place remaining characters individually if we run out of attempts
            while placed < count:
                empty_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if terrain[r][c] == '.']
                if not empty_positions:
                    break
                r, c = random.choice(empty_positions)
                terrain[r][c] = char
                placed += 1

        def place_scattered(char, count):
            empty_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if terrain[r][c] == '.']
            positions = random.sample(empty_positions, min(count, len(empty_positions)))
            for r, c in positions:
                terrain[r][c] = char

        if self.num_lava is not None:
            place_group('L', self.num_lava)
        if self.num_water is not None:
            place_group('W', self.num_water)
        if self.num_rubble is not None:
            place_group('R', self.num_rubble)
        if self.num_obstacles is not None:
            place_scattered('O', self.num_obstacles)

        return terrain

# =================================================================================================
    def get_random_positions(self) -> list[list[str]]:
        # Initialize the board with '.' for all positions
        board = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Find all empty positions ('.') on the terrain
        empty_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.board_terrain[r][c] == '.']
        
        if len(empty_positions) < self.num_heroes:
            raise ValueError("Not enough empty positions to place the heroes")
        
        # Shuffle the empty positions and pick the first `num_heros` positions
        random.shuffle(empty_positions)
        hero_positions = empty_positions[:self.num_heroes]
        
        # Place the heroes on the board with incremental numbers
        for i, (r, c) in enumerate(hero_positions):
            board[r][c] = str(i + 1)
        
        return board

# =================================================================================================
    def convert_to_string_list(self, char_list: list[list[str]]) -> list[str]:
        return ["".join(row) for row in char_list]
    
# =================================================================================================
    def print_board_terrain(self):
        print("Random Terrain")
        # Print column numbers
        print('    ', end='')
        for col in range(len(self.board_terrain[0])):
            print(f'{col:2}', end='')
        print()
        print(" ---------------------------------")

        # Print board rows with row numbers
        for i, row in enumerate(self.board_terrain):
            print(f'{i:2} | ', end='')
            print(' '.join(row))
        print("")

# =================================================================================================
    def print_board_positions(self):
        print("Random Hero Positions")
        # Print column numbers
        print('    ', end='')
        for col in range(len(self.board_positions[0])):
            print(f'{col:2}', end='')
        print()
        print(" ---------------------------------")

        # Print board rows with row numbers
        for i, row in enumerate(self.board_positions):
            print(f'{i:2} | ', end='')
            print(' '.join(row))
        print("")
