from enums import Board_Codes, Terrain_Codes
from modules.point import Allowable_Point
from modules.zone import Zone

class Map:
    empty_square_code = Board_Codes.empty_square_code.value
    obstacle_code = Board_Codes.obstacle_code.value
    basic_map_id = Terrain_Codes.basic_terrain.value
    flying_map_id = Terrain_Codes.flying_hero.value
    
    def __init__(self, id=0, name="", board=None):
        self.id = 0
        self.name = name
        self.board = board if board is not None else []
        self.chokepoints = self.find_chokepoints()
        self.deadends = self.find_deadends()
        self.zones = self.get_zones_of_map()
        self.sections = self.get_sections_in_zones()
        self.paths = self.get_all_paths()
        self.points_new = self.get_all_points_of_map()
        self.points_same = self.get_all_allowable_points_same()
        # Don't need these points unless the inputs call for them
        self.points_lava_basic = []
        self.points_water_basic = []
        self.points_rubble_basic = []
        self.points_flying_basic = []
        self.points_flying_lava = []
        self.points_flying_water = []
        self.points_flying_rubble = []

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
                    if self.board[i][j] == Board_Codes.obstacle_code.value:
                        print('[]', end=' ')
                    else:
                        print('..', end=' ')

            print('|')

        print("------", end = "")
        for i in range(len(self.board[0])):
            print("---", end = "")
        print("\n")
    
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
        
        return not self.does_path_exist(self.board, start, end, chokepoint)

# # =================================================================================================
# True if a path exists on the board from start to end and not passing through the chokepoint
    def does_path_exist(self, board: list[list[chr]], start: tuple[int, int], end: tuple[int, int], chokepoint: tuple[int, int] = None) -> bool:
        rows, cols = len(board), len(board[0])
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
    def is_deadend_zone(self, zone_id, zones):
        for z in zones:
            if z.id == zone_id and z.is_deadend:
                return True
        return False
    
# =================================================================================================
# Get all connected deadend zones to the zone_id given
    def get_connected_deadend_zone_ids(self, zone_id, zones: list[Zone]) -> list[int]:
        connected_deadend_zones = []
        for z in zones:
            if z.id == zone_id:
                for conn_id in z.connected_zones:
                    if self.is_deadend_zone(conn_id, zones):
                        connected_deadend_zones.append(conn_id)
        return connected_deadend_zones

# =================================================================================================
# Returns the previous deadend zone prior to the zone_id on the path of zones given
    def get_previous_deadend_zone_id(self, zone_id, path: list[Zone], zones: list[Zone]) -> int | None:
        if zone_id in path:
            index_of_zone = path.index(zone_id)
            if index_of_zone <= 0:
                return None
            for i in range(index_of_zone - 1, -1, -1):
                if self.is_deadend_zone(path[i], zones):
                    return path[i]
        return None

# =================================================================================================
# Returns the next deadend zone after the zone_id on the path of zones given
    def get_next_deadend_zone_id(self, zone_id, path: list[int], zones: list[Zone]):
        if zone_id in path:
            index_of_zone = path.index(zone_id)
            if index_of_zone >= len(path) - 1:
                return None
            for i in range(index_of_zone + 1, len(path)):
                if self.is_deadend_zone(path[i], zones):
                    return path[i]
        return None

# =================================================================================================
#
    def is_pivot_deadend(self, pivot_map: 'Map', point: tuple) -> bool:
        return self.get_zone_of_point(point, pivot_map.zones).is_deadend

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
    def zone_is_on_main_path(self, zone_id, main_path: list[int]):
        return zone_id in main_path

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

# endregion

# =================================================================================================
# SECTIONS
# =================================================================================================
# region SECTIONS
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
# endregion
    
# =================================================================================================
# POINTS
# =================================================================================================
# region POINTS

# Gets all allowable points of this map if both the pivot and the movable hero share this map.
# For example, if this map is a Lava map and both the pivot and the hero are lava walkers,
# then this will get all allowable points the hero can move to based on what section and path
# the pivot is on and what zone the hero is in.
# The list is a nested list that represents: 
#       start_zone_of_pivot > end_zone_of_pivot > hero_zone
# For example, if the pivot is moving from zone 2 to 9 and the movable hero is in zone 10,
# you can get the hero's allowable points by: list[2][9][10]
    def get_all_points_of_map(self):
        num_zones = len(self.zones)
        allowable_points = [[[None for _ in range(num_zones)] for _ in range(num_zones)] for _ in range(num_zones)]

        # s represents Pivot Start Zone
        # e represents Pivot End Zone
        # h represents Hero Zone
        for s in range(len(self.zones)):
            for e in range(len(self.zones)):
                main_path_id = self.get_path_id(s, e)
                if main_path_id is None:
                    continue
                main_path = self.paths[main_path_id]
                for h in range(len(self.zones)):
                    if h in main_path:
                        points = self.get_points_main(self.zones, main_path, h)
                    else:
                        alt_path_id = self.get_path_id(s, h)
                        if alt_path_id is None:
                            continue
                        alt_path = self.paths[alt_path_id]
                        points = self.get_points_alt(self.zones, main_path, alt_path, h)
                    allowable_points[s][e][h] = points
        return allowable_points


# Gets all allowable points of this map if both the pivot and the movable hero share this map.
# For example, if this map is a Lava map and both the pivot and the hero are lava walkers,
# then this will get all allowable points the hero can move to based on what section and path
# the pivot is on and what zone the hero is in.
# The list is a nested list that represents: section > path > zone > points
# For example, if the pivot is in section 1, on path id 49, and the hero is in zone 3, then you
# can get the hero's allowable points by list[1][49][3].points
    def get_all_allowable_points_same(self) -> list[list[list[list[tuple]]]]:
        allowable_points = []

        for s in range(len(self.sections)):
            section_points = []
            zones_in_this_section = self.get_zones_in_section(self.sections[s])
            paths_in_this_section = self.get_paths_in_section(self.sections[s])
            # print(f"section: {s}, zones in this section: ")
            # for j in zones_in_this_section:
            #     print(j)
            # print("paths in this section: ")
            # for i in paths_in_this_section:
            #     print(i)
            for p in range(len(paths_in_this_section)):
                path_points = []
                main_path = paths_in_this_section[p]
                pivot_start_zone = main_path[0]
                pivot_end_zone = main_path[len(main_path)-1]
                main_path_id = self.get_path_id(pivot_start_zone, pivot_end_zone)

                for z in range(len(zones_in_this_section)):
                    zone_points: Allowable_Point = Allowable_Point()
                    zone = zones_in_this_section[z]
                    current_zone_id = zone.id

                    if current_zone_id in main_path:
                        points = self.get_points_main(zones_in_this_section, main_path, current_zone_id)
                        zone_points.alt_path = None
                    else:
                        alt_path_id = self.get_path_id(pivot_start_zone, current_zone_id)
                        alt_path = self.get_path_from_start_to_end(pivot_start_zone, current_zone_id)
                        points = self.get_points_alt(zones_in_this_section, main_path, alt_path, current_zone_id)
                        zone_points.alt_path = alt_path_id
                        zone_points.alt_path = alt_path

                    zone_points.zone_id = current_zone_id
                    zone_points.section = s
                    zone_points.main_path_id = main_path_id
                    zone_points.main_path = self.paths[p]
                    zone_points.points.extend(points)
                    
                    path_points.append(zone_points)  # Append zone_points to path_points
                
                section_points.append(path_points)  # Append path_points to section_points
            
            allowable_points.append(section_points)  # Append section_points to allowable_points
        
        return allowable_points

# =================================================================================================
#
    def get_allowable_points_mismatch_old(self, pivot_terrain_code: int, pivot_map: 'Map') -> list[list[list[list[tuple]]]]:
        allowable_points = []
        num_rows = len(self.board[0])
        num_cols = len(self.board)
        num_entries = num_rows * num_cols
        
        allowable_points = [[None for _ in range(num_entries)] for _ in 2]

        return allowable_points


    def get_all_points_mismatch_maps(self, pivot_terrain_code: int, pivot_map: 'Map') -> dict[tuple[tuple[int, int], tuple[int, int]], str]:
        result = {}
        rows = len(pivot_map.board)
        cols = len(pivot_map.board[0]) if rows > 0 else 0

        for r1 in range(rows):
            for c1 in range(cols):
                for r2 in range(rows):
                    for c2 in range(cols):
                        if r1 == r2 and c1 == c2:
                            continue
                        point_pivot = (r1, c1)
                        point_hero = (r2, c2)
                        path_exists = self.does_path_exist(pivot_map.board, point_pivot, point_hero)
                        if path_exists:
                            hero_zone = self.get_zone_of_point(point_hero)
                            allowable_points = []
                            allowable_points.extend(self.get_points_in_zone(hero_zone))
                            is_pivot_de = self.is_pivot_deadend(pivot_map, point_hero)
                            if is_pivot_de:
                                pass
                            else:
                                pass
                            result[(point_pivot, point_hero)] = allowable_points

        return result
    

# =================================================================================================
# Gets a list of all allowable points for a moveable hero who is on the main path of the pivot
# zones = a list of Zone objects for the given board (should only be 1 section)
# main_path = a list of zones the pivot moves through
# start_zone = the starting zone of the movable hero
    def get_points_main(self, zones: list[Zone], main_path_of_pivot: list[int], hero_start_zone_id: int):
        allowable_points = []
        allowable_zones = []

        # A movable hero can move anywhere in his current zone unless it is a DE
        # because being on the main path of the pivot, he is forced off his DE to the previous zone
        if not self.is_deadend_zone(hero_start_zone_id, zones):
            allowable_zones.append(hero_start_zone_id)

        # Hero starts on a deadend zone
        if self.is_deadend_zone(hero_start_zone_id, zones):
            previous_zone_id = self.get_previous_zone_id(hero_start_zone_id, main_path_of_pivot)
            if previous_zone_id is not None:
                # Hero can move anywhere in the previous zone
                allowable_zones.append(previous_zone_id)
                # Hero can move to previous zones connected deadend zones, with exceptions
                connected_deadend_zones = self.get_connected_deadend_zone_ids(previous_zone_id, zones)
                connected_deadend_zones.remove(hero_start_zone_id) # Cannot move to his start zone because it is a DE on the main path
                # If the previous zone from the hero start is a DE
                if self.is_deadend_zone(previous_zone_id, zones):
                    previous_previous_zone_id = self.get_previous_zone_id(previous_zone_id, main_path_of_pivot)
                    # If the previous zone from the previous zone from the hero start is a DE
                    # This is describing a single row or column of DEs
                    if previous_previous_zone_id and self.is_deadend_zone(previous_previous_zone_id, zones):
                        # Cannot move to the DE prior to the DE the hero got displaced on because it is a single row/col of DEs
                        connected_deadend_zones.remove(previous_previous_zone_id)
                allowable_zones.extend(connected_deadend_zones)

        # Movable hero starts on a nondeadend zone
        else:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the downstream zone on the main path
            connected_deadend_zones = self.get_connected_deadend_zone_ids(hero_start_zone_id, zones)
            next_deadend_zone_id = self.get_next_deadend_zone_id(hero_start_zone_id, main_path_of_pivot, zones) # downstream deadend zone
            if next_deadend_zone_id:
                connected_deadend_zones.remove(next_deadend_zone_id)
            allowable_zones.extend(connected_deadend_zones)

        # Add the points from the allowable zones to the list
        for z in allowable_zones:
            allowable_points.extend(self.get_points_in_zone(z, zones))

        # Remove dups
        unique_points = self.remove_duplicates(allowable_points)

        # Sort the resulting list of points by row and then by column
        allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

        return allowable_points

# =================================================================================================
# Gets a list of all allowable points for a moveable hero on an alternate path of the pivot
# zones = a list of Zone objects for the given board (should only be 1 section)
# main_path = the id of the current main path of the pivot (from pivot start zone to current pivot point)
# alt_path = the id of the alternate path of the pivot (from pivot start zone to hero start zone)
# start_zone = the starting zone of the movable hero
#TODO needs rigourous testing
    def get_points_alt(self, zones: list[Zone], main_path_of_pivot: list[int], alt_path_of_pivot: list[int], hero_start_zone_id: int):
        allowable_points = []  # Allow duplicates
        allowable_zones = []

        # A movable hero can move anywhere in his current zone
        allowable_zones.append(hero_start_zone_id)

        # Movable hero starts on a deadend zone
        if self.is_deadend_zone(hero_start_zone_id, zones):
            previous_zone_id = self.get_previous_zone_id(hero_start_zone_id, alt_path_of_pivot)
            if previous_zone_id is not None:
                # If the previous zone is a deadend:
                if self.is_deadend_zone(previous_zone_id, zones):
                    pass # No allowable points in the previous zone
                else: # If the previous zone is not a deadend
                    # Hero starts on deadend zone can move to the previous nondeadend zone
                    allowable_zones.append(previous_zone_id)
                    connected_deadend_zones = self.get_connected_deadend_zone_ids(previous_zone_id, zones)
                    # Previous nondeadend zone is on the main path
                    if self.zone_is_on_main_path(previous_zone_id, main_path_of_pivot):
                        restricted_zone_id = self.get_next_deadend_zone_id(previous_zone_id, main_path_of_pivot, zones) # Downstream
                    # Previous nondeadend zone is not on the main path
                    else:
                        restricted_zone_id = self.get_previous_deadend_zone_id(previous_zone_id, alt_path_of_pivot, zones) # Upstream

                    # Add the allowable connected deadend zones
                    if restricted_zone_id:
                        connected_deadend_zones.remove(restricted_zone_id)

                    allowable_zones.extend(connected_deadend_zones)

        # Movable hero starts on a nondeadend zone
        else:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the upstream zone on the alt path
            connected_deadend_zones = self.get_connected_deadend_zone_ids(hero_start_zone_id, zones)
            restricted_zone_id = self.get_previous_deadend_zone_id(hero_start_zone_id, alt_path_of_pivot, zones)
            connected_deadend_zones.remove(restricted_zone_id)
            allowable_zones.extend(connected_deadend_zones)

        # Add the points from the allowable zones to the list
        for z in allowable_zones:
            allowable_points.extend(self.get_points_in_zone(z, zones))

        # Remove dups
        unique_points = self.remove_duplicates(allowable_points)
        
        # Sort the resulting list of points by row and then by column
        allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

        return allowable_points

# =================================================================================================
    def remove_duplicates(self, list):
        return [t for t in (set(tuple(i) for i in list))]

# =================================================================================================
    def get_points_in_zone(self, zone: int, zones: list[Zone]) -> list[int] | None:
        for z in zones:
            if z.id == zone:
                return z.points
        return None

# =================================================================================================
    def get_points_in_section(self, section: int) -> list[tuple]:
        points: list[tuple] = []
        for z in self.zones:
            if z.section == section:
                points.extend(z.points)
        self.remove_duplicates(points)
        points = sorted(points, key=lambda p: (p[0], p[1]))
        return points
#endregion
