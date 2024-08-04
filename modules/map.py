from enums import Board_Codes, Terrain_Codes
from modules.zone import Zone

class Map:
    empty_square_code = Board_Codes.empty_square_code.value
    obstacle_code = Board_Codes.obstacle_code.value
    lava_code = Board_Codes.lava_code.value
    water_code = Board_Codes.water_code.value
    rubble_code = Board_Codes.rubble_code.value
    
    def __init__(self, id=0, name="", board=None):
        self.id = 0
        self.name = name
        self.board = board if board is not None else []
        self.chokepoints = self.find_chokepoints()
        self.deadends = self.find_deadends()
        self.zones = self.get_zones_of_map()
        self.sections = self.get_sections_in_zones()
        self.paths = self.get_all_paths()

    def __str__(self):
        return (f'ID: {self.id}, Name: {self.name}, '
                f'Board: {self.board}, Chokepoints: {self.chokepoints}, '
                f'Deadends: {self.deadends}, Zones: {self.zones}')

    def get_copy(self, id, name):
        board: Map = Map(id, name, self.board)
        return board

# =================================================================================================
# PRINT
# =================================================================================================
# region PRINT
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

# =================================================================================================
    def print_map_with_zones(self):
        print("Zone Map: ", self.name)

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
                    if self.board[i][j] == self.obstacle_code:
                        print('[]', end=' ')
                    else:
                        print('..', end=' ')

            print('|')

        print("------", end = "")
        for i in range(len(self.board[0])):
            print("---", end = "")
        print("")
    
# =================================================================================================
    def print_map_with_positions(self, hero_pos: list[tuple]):
        print("Position Map: ", self.name)

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
                if self.board[i][j] == self.obstacle_code:
                    print('[]', end=' ')
                else:
                    found = False
                    for h in range(len(hero_pos)):
                        if hero_pos[h][0] == i and hero_pos[h][1] == j:
                            found = True
                            print(f'{h:02}', end=' ')
                    if not found:
                        print('..', end=' ')
                    else:
                        found = False
            print('|')

        print("------", end = "")
        for i in range(len(self.board[0])):
            print("---", end = "")
        print("")

# =================================================================================================
    def print_map_with_terrains(self, terrain: list[list[chr]]):
        print("Terrain Map: ", self.name)

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
        for i in range(len(terrain)):
            print(f'{i:2} | ', end='')
            # Loop through the columns
            for j in range(len(terrain[i])):
                if terrain[i][j] == self.obstacle_code:
                    print('[]', end=' ')
                elif terrain[i][j] == self.lava_code:
                    print('LL', end=' ')
                elif terrain[i][j] == self.water_code:
                    print('//', end=' ')
                elif terrain[i][j] == self.rubble_code:
                    print(';;', end=' ')
                else:
                    print('..', end=' ')

            print('|')

        print("------", end = "")
        for i in range(len(self.board[0])):
            print("---", end = "")
        print("")

# =================================================================================================
    def print_map_details(self):
        print(self.name)
        print("\n--------------------------------")
        self.print_map_with_zones(self)
        print("\nchokepoints: ", self.chokepoints)
        print("deadends (", len(self.deadends), "): ", self.deadends)
        for z in self.zones:
            print(z)
# endregion

# =================================================================================================
# CHOKEPOINTS
# =================================================================================================
# region CHOKEPOINTS
#
    def find_chokepoints(self) -> list[tuple]:
        chokepoints = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.is_chokepoint(row, col):
                    chokepoints.append((row, col))
        return chokepoints
# =================================================================================================
# Checks if the point is a chokepoint
    def is_chokepoint(self, row: int, col: int) -> bool:
        # Ensure the current cell is an empty square
        if self.board[row][col] != self.empty_square_code:
            return False

        # Define the conditions for different types of chokepoints
    def is_chokepoint(self, row: int, col: int) -> bool:
        # Ensure the current cell is an empty square
        if self.board[row][col] != self.empty_square_code:
            return False

        # Top left corner
        if self.is_top_left_corner(row, col):
            if (self.obstacle_below(row, col) and self.empty_square_right(row, col)) or (self.obstacle_right(row, col) and self.empty_square_below(row, col)):
                return True
            else:
                return False
            
        # Top right corner
        if self.is_top_right_corner(row, col):
            if (self.obstacle_below(row, col) and self.empty_square_left(row, col)) or (self.obstacle_left(row, col) and self.empty_square_below(row, col)):
                return True
            else:
                return False

        # Bottom left corner
        if self.is_bottom_left_corner(row, col):
            if (self.obstacle_above(row, col) and self.empty_square_right(row, col)) or (self.obstacle_right(row, col) and self.empty_square_above(row, col)):
                return True
            else:
                return False

        # Bottom right corner
        if self.is_bottom_right_corner(row, col):
            if (self.obstacle_above(row, col) and self.empty_square_left(row, col)) or (self.obstacle_left(row, col) and self.empty_square_above(row, col)):
                return True
            else:
                return False

        # Above edge
        if self.edge_above(row, col):
            if (self.obstacle_left_and_right(row, col) and self.empty_square_below(row, col)) or (self.obstacle_below(row, col) and (self.empty_square_left(row, col) or self.empty_square_right(row, col))):
                return True
            else:
                return False

        # Below edge
        if self.edge_below(row, col):
            if (self.obstacle_left_and_right(row, col) and self.empty_square_above(row, col)) or (self.obstacle_above(row, col) and (self.empty_square_left(row, col) or self.empty_square_right(row, col))):
                return True
            else:
                return False

        # Left edge
        if self.edge_left(row, col):
            if (self.obstacle_above_and_below(row, col) and self.empty_square_right(row, col)) or (self.obstacle_right(row, col) and (self.empty_square_above(row, col) or self.empty_square_below(row, col))):
                return True
            else:
                return False

        # Right edge
        if self.edge_right(row, col):
            if (self.obstacle_above_and_below(row, col) and self.empty_square_left(row, col)) or (self.obstacle_left(row, col) and (self.empty_square_above(row, col) or self.empty_square_below(row, col))):
                return True
            else:
                return False

        # Middle
        if self.is_in_middle(row, col):
            if (self.obstacle_above_and_below(row, col) and (self.empty_square_left(row, col) or self.empty_square_right(row, col))) or (self.obstacle_left_and_right(row, col) and (self.empty_square_above(row, col) or self.empty_square_below(row, col))):
                return True
            else:
                return False

# endregion

# =================================================================================================
# SQUARE CHECK METHODS
# =================================================================================================
# region SQUARE CHECKS
# =================================================================================================
    # Specific check
    def square_is(self, row, col, type):
        return self.board[row][col] == type
    def square_is_empty(self, row, col):
        return self.board[row][col] == self.empty_square_code
    def square_is_obstacle(self, row, col):
        return self.board[row][col] == self.obstacle_code
# =================================================================================================
    # Diagonal obstacles check
    def obstacle_above_left(self, row, col):
        return self.board[row-1][col-1] == self.obstacle_code
    def obstacle_above_right(self, row, col):
        return self.board[row-1][col+1] == self.obstacle_code
    def obstacle_below_left(self, row, col):
        return self.board[row+1][col-1] == self.obstacle_code
    def obstacle_below_right(self, row, col):
        return self.board[row+1][col+1] == self.obstacle_code
# =================================================================================================
    # Empty squares check
    def empty_square_left(self, row, col):
        return self.board[row][col-1] == self.empty_square_code
    def empty_square_right(self, row, col):
        return self.board[row][col+1] == self.empty_square_code
    def empty_square_above(self, row, col):
        return self.board[row-1][col] == self.empty_square_code
    def empty_square_below(self, row, col):
        return self.board[row+1][col] == self.empty_square_code
    def empty_square_left_and_right(self, row, col):
        return self.empty_square_left(row, col) and self.empty_square_right(row, col)
    def empty_square_above_and_below(self, row, col):
        return self.empty_square_above(row, col) and self.empty_square_below(row, col)
# =================================================================================================
    # Obstacles check
    def obstacle_left(self, row, col):
        return self.board[row][col-1] == self.obstacle_code
    def obstacle_right(self, row, col):
        return self.board[row][col+1] == self.obstacle_code
    def obstacle_above(self, row, col):
        return self.board[row-1][col] == self.obstacle_code
    def obstacle_below(self, row, col):
        return self.board[row+1][col] == self.obstacle_code
    def obstacle_left_and_right(self, row, col):
        return self.obstacle_left(row, col) and self.obstacle_right(row, col)
    def obstacle_above_and_below(self, row, col):
        return self.obstacle_above(row, col) and self.obstacle_below(row, col)
# =================================================================================================
    # Edges check
    def edge_left(self, row, col):
        return col == 0
    def edge_right(self, row, col):
        return col == len(self.board[0]) - 1
    def edge_above(self, row, col):
        return row == 0
    def edge_below(self, row, col):
        return row == len(self.board) - 1
# =================================================================================================
    # Corners check
    def is_top_left_corner(self, row, col):
        return (row == 0 and col == 0)
    def is_top_right_corner(self, row, col):
        return (row == 0 and col == len(self.board[0]) -1)
    def is_bottom_left_corner(self, row, col):
        return (row == len(self.board) - 1 and col == 0)
    def is_bottom_right_corner(self, row, col):
        return (row == len(self.board) - 1 and col == len(self.board[0]) - 1)
# =================================================================================================
    # Middle check
    def is_in_middle(self, row, col):
        return 0 < row < len(self.board) - 1 and 0 < col < len(self.board[0]) - 1
    # endregion

# =================================================================================================
# DEADENDS
# =================================================================================================
# region DEADENDS
    def find_deadends(self) -> list[tuple]:
        obstacles = []
        for chokepoint in self.chokepoints:
            if self.is_deadend(chokepoint):
                obstacles.append(chokepoint)
        return obstacles

# =================================================================================================
# Checks if the chokepoint is a deadend 
    def is_deadend(self, chokepoint: tuple):
        row, col = chokepoint
        left = (row, col-1)
        right = (row, col+1)
        above = (row-1, col)
        below = (row+1, col)
        start = (0,0)
        end = (0,0)

        if self.is_in_middle(row, col):
            # If chokepoint is in the middle surrounded by empty_squares, need to evaulate paths 
            if self.empty_square_left_and_right(row, col):
                start = left
                end = right
            elif self.empty_square_above_and_below(row, col):
                start = above
                end = below
            # Chokepoints surrounded by 3 obstacles are deadends only if burried 2 or more squares deep
            elif self.obstacle_above_and_below(row, col):
                if self.obstacle_left(row, col) and self.obstacle_above_right(row, col) and self.obstacle_below_right(row, col):
                    return True
                elif self.obstacle_right(row, col) and self.obstacle_above_left(row, col) and self.obstacle_below_left(row, col):
                    return True
            elif self.obstacle_left_and_right(row, col) :
                if self.obstacle_above(row, col) and self.obstacle_below_left(row, col) and self.obstacle_below_right(row, col):
                    return True
                elif self.obstacle_below(row, col) and self.obstacle_above_left(row, col) and self.obstacle_above_right(row, col):
                    return True
        # Corners are only deadends if burried with 2 or more obstacles
        elif self.is_top_left_corner(row, col):
            if (self.obstacle_below(row, col) or self.obstacle_right(row, col)) and self.obstacle_below_right(row, col):
                return True
        elif self.is_top_right_corner(row, col):
            if (self.obstacle_below(row, col) or self.obstacle_left(row, col)) and self.obstacle_below_left(row, col):
                return True
        elif self.is_bottom_left_corner(row, col):
            if (self.obstacle_above(row, col) or self.obstacle_right(row, col)) and self.obstacle_above_right(row, col):
                return True
        elif self.is_bottom_right_corner(row, col):
            if (self.obstacle_above(row, col) or self.obstacle_left(row, col)) and self.obstacle_above_left(row, col):
                return True
        # Edge chokepoints surrounded by empty sqaures need to evaluate paths
        elif (self.edge_above(row, col) or self.edge_below(row, col)) and self.empty_square_left_and_right(row, col):
                start = left
                end = right
        elif (self.edge_left(row, col) or self.edge_right(row, col)) and self.empty_square_above_and_below(row, col):
                start = above
                end = below
        # Edge chokepoints 
        elif self.edge_left(row, col):
            if self.obstacle_above_and_below(row, col) and self.obstacle_above_right(row, col) and self.obstacle_below_right(row, col):
                return True
            elif self.obstacle_above(row, col) and self.obstacle_right(row, col) and self.obstacle_below_right(row, col):
                return True
            elif self.obstacle_below(row, col) and self.obstacle_right(row, col) and self.obstacle_above_right(row, col):
                return True
        elif self.edge_right(row, col):
            if self.obstacle_above_and_below(row, col) and self.obstacle_above_left(row, col) and self.obstacle_below_left(row, col):
                return True
            elif self.obstacle_above(row, col) and self.obstacle_left(row, col) and self.obstacle_below_left(row, col):
                return True
            elif self.obstacle_below(row, col) and self.obstacle_left(row, col) and self.obstacle_above_left(row, col):
                return True
        elif self.edge_above(row, col):
            if self.obstacle_left_and_right(row, col) and self.obstacle_below_left(row, col) and self.obstacle_below_right(row, col):
                return True
            elif self.obstacle_left(row, col) and self.obstacle_below(row, col) and self.obstacle_below_right(row, col):
                return True
            elif self.obstacle_right(row, col) and self.obstacle_below(row, col) and self.obstacle_below_left(row, col):
                return True
        elif self.edge_below(row, col):
            if self.obstacle_left_and_right(row, col) and self.obstacle_above_left(row, col) and self.obstacle_above_left(row, col):
                return True
            elif self.obstacle_left(row, col) and self.obstacle_above(row, col) and self.obstacle_above_right(row, col):
                return True
            elif self.obstacle_right(row, col) and self.obstacle_above(row, col) and self.obstacle_above_left(row, col):
                return True
        
        return not self.does_path_exist(start, end, chokepoint)

# # =================================================================================================
# True if a path exists on the board from start to end and not passing through the chokepoint
    def does_path_exist(self, start: tuple[int, int], end: tuple[int, int], chokepoint: tuple[int, int] = None) -> bool:
        rows, cols = len(self.board), len(self.board[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]

        def is_valid_move(board, visited, row, col, chokepoint) -> bool:
            # Check if the move is within the board boundaries
            if not (0 <= row < rows and 0 <= col < cols):
                return False
            # Check if the position is the chokepoint or already visited
            if visited[row][col] or (chokepoint is not None and (row, col) == chokepoint):
                return False
            # Check if the position is not an obstacle
            return board[row][col] != self.obstacle_code
        
        def backtrack(row, col) -> bool:
            # Check if we've reached the end point
            if (row, col) == end:
                return True
            # Mark the current position as visited
            visited[row][col] = True
            
            # Define possible movement directions (right, down, left, up)
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if is_valid_move(self.board, visited, new_row, new_col, chokepoint):
                    if backtrack(new_row, new_col):
                        return True
            
            # No need to unmark the current position (backtracking)
            return False

        start_row, start_col = start
        return backtrack(start_row, start_col)

# =================================================================================================
    def is_deadend_zone(self, zone_id):
        for z in self.zones:
            if z.id == zone_id and z.is_deadend:
                return True
        return False
    
# =================================================================================================
# Get all connected deadend zones to the zone_id given
    def get_connected_deadend_zone_ids(self, zone_id) -> list[int]:
        connected_deadend_zones = []
        for z in self.zones:
            if z.id == zone_id:
                for conn_id in z.connected_zones:
                    if self.is_deadend_zone(conn_id):
                        connected_deadend_zones.append(conn_id)
        return connected_deadend_zones

# =================================================================================================
# Returns the previous deadend zone prior to the zone_id on the path of zones given
    def get_previous_deadend_zone_id(self, zone_id, path: list[int]) -> int | None:
        if zone_id in path:
            index_of_zone = path.index(zone_id)
            if index_of_zone <= 0:
                return None
            for i in range(index_of_zone - 1, -1, -1):
                if self.is_deadend_zone(path[i]):
                    return path[i]
        return None

# =================================================================================================
# Returns the next deadend zone after the zone_id on the path of zones given
    def get_next_deadend_zone_id(self, zone_id, path: list[int]):
        if zone_id in path:
            index_of_zone = path.index(zone_id)
            if index_of_zone >= len(path) - 1:
                return None
            for i in range(index_of_zone + 1, len(path)):
                if self.is_deadend_zone(path[i]):
                    return path[i]
        return None

# =================================================================================================
#
    def is_pivot_deadend(self, hero_zone_id: int, hero_map: 'Map') -> bool:
        if hero_map.zones[hero_zone_id].is_deadend:
            point = hero_map.zones[hero_zone_id].points[0]
            return self.get_zone_of_point(point, self.zones).is_deadend
        else:
            return False

# =================================================================================================
#
    
# endregion

# =================================================================================================
# ZONES
# =================================================================================================
# region ZONES
# Returns a list of zones based on the board and deadends
    def get_zones_of_map(self) -> list[Zone]:
        rows, cols = len(self.board), len(self.board[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        deadends_set = set(self.deadends)
        visited = set()
        zones_pre = [] # Set of zones before adding connections and sections
        zones: list[Zone] = [] # Set of Zone objects
        zone_id = -1
        
        # Breadth first search through board
        def bfs(start):
            queue = [start]
            zone = []
            while queue:
                r, c = queue.pop(0)
                if (r, c) in visited or (r, c) in deadends_set or self.board[r][c] == self.obstacle_code:
                    continue
                visited.add((r, c))
                zone.append((r, c))
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                        queue.append((nr, nc))
            return zone
        
        # Mark what section the zones are in
        def mark_sections(zones):
            section_counter = -1
            visited = set()
            
            def dfs(zone, section_id):
                stack = [zone]
                while stack:
                    current_zone = stack.pop()
                    if current_zone.id in visited:
                        continue
                    visited.add(current_zone.id)
                    current_zone.section = section_id
                    for connected_zone_id in current_zone.connected_zones:
                        connected_zone = next(z for z in zones if z.id == connected_zone_id)
                        if connected_zone.id not in visited:
                            stack.append(connected_zone)
            
            for zone in zones:
                if zone.id not in visited:
                    section_counter += 1
                    dfs(zone, section_counter)

        # Get the points in the zones
        for r in range(rows):
            for c in range(cols):
                if self.board[r][c] == self.empty_square_code and (r, c) not in visited:
                    if (r, c) in deadends_set:
                        zones_pre.append([(r, c)])  # Add deadend as individual zone
                    else:
                        new_zone = bfs((r, c))
                        if new_zone:
                            zones_pre.append(sorted(new_zone))
        
        # Sort the zones based on their top-left coordinate
        zones_pre.sort(key=lambda zone: zone[0] if zone else (rows, cols))
        
        # Marks the is_deaded property of the zone if the zone is a deadend
        for z in zones_pre:
            zone_id = zone_id + 1
            is_a_deadend = False
            if len(z) == 1 and z[0] in self.deadends:
                is_a_deadend = True
            new_zone = Zone(section = 0, id=zone_id, is_deadend=is_a_deadend)
            new_zone.points = z
            zones.append(new_zone)

        # Assigns the connected_zones property of the zones:
        for i in range(len(zones)):
            for j in range(i + 1, len(zones)):  # Only compare each pair of zones once
                connected = False
                for point1 in zones[i].points:
                    for point2 in zones[j].points:
                        if self.is_cardinally_adjacent(point1, point2):
                            connected = True
                            break
                    if connected:
                        break
                if connected:
                    zones[i].connected_zones.append(zones[j].id)
                    zones[j].connected_zones.append(zones[i].id)

        for z in zones:
            for c in z.connected_zones:
                if zones[c].is_deadend:
                    z.connected_deadend_zones.append(c)

        mark_sections(zones)

        return zones

# =================================================================================================
# True if point1 is cardinally adjacent to point2
    def is_cardinally_adjacent(self, point1, point2):
        return (abs(point1[0] - point2[0]) == 1 and point1[1] == point2[1]) or (abs(point1[1] - point2[1]) == 1 and point1[0] == point2[0])

# =================================================================================================
# Gets a minimized list of Zone objects of only the section given
    def get_zones_in_section(self, section: int) -> list[Zone]:
        result = []
        for zone in self.zones:
            if zone.section == section:
                result.append(zone)
        return result

# =================================================================================================
# Gets the zone id of the point given
    def get_zone_of_point(self, point: tuple, zones: list[Zone] = None) -> Zone | None:
        if zones is None:
            zones = self.zones
        for zone in zones:
            if point in zone.points:
                return zone
        return None  # Return None if no zone contains the point

# =================================================================================================
#
    def get_zone_id_of_point(self, point: tuple, zones: list[Zone] = None) -> int | None:
        if zones is None:
            zones = self.zones
        for zone in zones:
            if point in zone.points:
                return zone.id
        return None

# =================================================================================================
# Gets a minimized list of Zone objects of only the section given
    def get_zones_in_section(self, section: int) -> list[Zone]:
        result = []
        for zone in self.zones:
            if zone.section == section:
                result.append(zone)
        return result
    
# =================================================================================================
# Gets the previous zone before the zone_id on the path given
    def get_previous_zone_id(self, zone_id: int, path: list[int]):
        for p in range(len(path) - 1):
            if zone_id == path[p+1]:
                return path[p]
        return None

# =================================================================================================
    def zone_is_on_path(self, zone_id, path: list[int]):
        return zone_id in path

# endregion

# =================================================================================================
# PATHS
# =================================================================================================
# region PATHS
#
    def get_all_paths(self) -> list[list[int]]:
        def dfs(current_zone, visited):
            visited.append(current_zone.id)
            paths.append(visited.copy())
            for neighbor_id in current_zone.connected_zones:
                if neighbor_id not in visited:
                    neighbor_zone = next(z for z in section_zones if z.id == neighbor_id)
                    dfs(neighbor_zone, visited)
            visited.pop()

        # Organize zones by sections
        sections = {}
        for zone in self.zones:
            if zone.section not in sections:
                sections[zone.section] = []
            sections[zone.section].append(zone)
        
        all_paths = []
        
        for section, section_zones in sections.items():
            paths = []
            for zone in section_zones:
                dfs(zone, [])
            all_paths.extend(paths)
        
        return all_paths

# =================================================================================================
# Gets a list of paths between the zones of a section. Every combination is included.
    def get_paths_in_section(self, section: int) -> list[list[int]]:
        # Helper function to perform DFS and find all paths
        def dfs(current_zone, visited):
            visited.append(current_zone.id)
            paths.append(visited.copy())
            for neighbor_id in current_zone.connected_zones:
                if neighbor_id not in visited:
                    neighbor_zone = next(z for z in self.zones if z.id == neighbor_id)
                    dfs(neighbor_zone, visited)
            visited.pop()

        # Filter zones by the given section
        section_zones = [z for z in self.zones if z.section == section]

        paths = []
        for zone in section_zones:
            dfs(zone, [])
        return paths

# =================================================================================================
# Gets the path where start_zone is the first and end_zone is the last
    def get_path_from_start_to_end(self, start_zone: int, end_zone: int) -> list[int] | None:
        for p in self.paths:
            if len(p) == 1 and p[0] == start_zone == end_zone:
                return p
            if p[0] == start_zone and p[-1] == end_zone:
                return p
        return None

# =================================================================================================
# 
    def get_path_id(self, start_zone: int, end_zone: int) -> int | None:
        for i in range(len(self.paths)):
            if len(self.paths[i]) == 1 and self.paths[i][0] == start_zone == end_zone:
                return i
            if self.paths[i][0] == start_zone and self.paths[i][len(self.paths[i])-1] == end_zone:
                return i
        return None  # Return None if no such path is found

# =================================================================================================
# 

# endregion

# =================================================================================================
# SECTIONS & POINTS
# =================================================================================================
# region SECTIONS AND POINTS

# Gets all the sections of the board
    def get_sections_in_zones(self) -> list[int]:
        sections = []
        for z in self.zones:
            if z.section not in sections:
                sections.append(z.section)
        return sections

# =================================================================================================
#
    def get_section_of_point(self, point: tuple) -> int | None:
        for z in self.zones:
            if point in z.points:
                return z.section
        return None

# =================================================================================================
#
    def get_points_in_zone(self, zone: int) -> list[int] | None:
        for z in self.zones:
            if z.id == zone:
                return z.points
        return None

# =================================================================================================
#
    def get_points_in_section(self, section: int) -> list[tuple]:
        points: list[tuple] = []
        for z in self.zones:
            if z.section == section:
                points.extend(z.points)
        self.remove_duplicates(points)
        points = sorted(points, key=lambda p: (p[0], p[1]))
        return points

# =================================================================================================
#
    def remove_duplicates(self, list):
        return [t for t in (set(tuple(i) for i in list))]

# endregion

