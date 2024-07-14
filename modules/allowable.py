from enums import Map_Matchups
from modules.map import Map
from modules.zone import Zone

class Allowable:
    # Map Matchup Ids
    basic_match_id = Map_Matchups.basic.value
    lava_match_id = Map_Matchups.lava.value
    water_match_id = Map_Matchups.water.value
    rubble_match_id = Map_Matchups.rubble.value
    flying_match_id = Map_Matchups.flying.value
    lava_basic_match_id = Map_Matchups.lava_basic.value
    water_basic_match_id = Map_Matchups.water_basic.value
    rubble_basic_match_id = Map_Matchups.rubble_basic.value
    flying_basic_match_id = Map_Matchups.flying_basic.value
    flying_lava_match_id = Map_Matchups.flying_lava.value
    flying_water_match_id = Map_Matchups.flying_water.value
    flying_rubble_match_id = Map_Matchups.flying_rubble.value

    def __init__(self, id: int):
        self.id = id
        self.points = []
        self.pivot_map = None
        self.hero_map = None

# =================================================================================================
# POINTS
# =================================================================================================
# region POINTS

    def get_points(self, map):
        if self.id == self.map_basic:
            pass
        elif self.id == self.map_lava:
            pass
        elif self.id == self.map_water:
            pass
        elif self.id == self.map_rubble:
            pass
        elif self.id == self.map_flying:
            pass
        elif self.id == self.map_flying_lava:
            pass
        elif self.id == self.map_flying_water:
            pass
        elif self.id == self.map_flying_rubble:
            pass

# =================================================================================================
# Gets all allowable points of this map if both the pivot and the movable hero share this map.
# For example, if this map is a Lava map and both the pivot and the hero are lava walkers,
# then this will get all allowable points the hero can move to based on what section and path
# the pivot is on and what zone the hero is in.
# The list is a nested list that represents: 
#       start_zone_of_pivot > end_zone_of_pivot > hero_zone
# For example, if the pivot is moving from zone 2 to 9 and the movable hero is in zone 10,
# you can get the hero's allowable points by: list[2][9][10]
    def get_all_points_of_map(self, map: 'Map') -> list[list[list[tuple]]]:
        num_zones = len(map.zones)
        allowable_points = [[[None for _ in range(num_zones)] for _ in range(num_zones)] for _ in range(num_zones)]

        # s represents Pivot Start Zone
        # e represents Pivot End Zone
        # h represents Hero Zone
        for s in range(len(map.zones)):
            for e in range(len(map.zones)):
                main_path_id = map.get_path_id(s, e)
                if main_path_id is None:
                    continue
                main_path = map.paths[main_path_id]
                for h in range(len(self.zones)):
                    if h in main_path:
                        points = self.get_points_main_path(map.zones, main_path, h)
                    else:
                        alt_path_id = map.get_path_id(s, h)
                        if alt_path_id is None:
                            continue
                        alt_path = map.paths[alt_path_id]
                        points = self.get_points_alt_path(map.zones, main_path, alt_path, h)
                    allowable_points[s][e][h] = points
        return allowable_points

# =================================================================================================
# This assumes the hero is on a basic map and the pivot is not
    def get_allowable_points_mismatch_old(self, pivot_terrain_code: int, pivot_map: 'Map') -> list[list[list[tuple]]]:
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
                        points = self.get_points_main_path(self.zones, main_path, h)
                    else:
                        alt_path_id = self.get_path_id(s, h)
                        if alt_path_id is None:
                            continue
                        alt_path = self.paths[alt_path_id]
                        points = self.get_points_alt_path(self.zones, main_path, alt_path, h)
                    allowable_points[s][e][h] = points
        return allowable_points

# =================================================================================================
#
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
    def get_points_main_path(self, zones: list[Zone], main_path_of_pivot: list[int], hero_start_zone_id: int):
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
    def get_points_alt_path(self, zones: list[Zone], main_path_of_pivot: list[int], alt_path_of_pivot: list[int], hero_start_zone_id: int):
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

# =================================================================================================
#
    # def get_point_of_zone_in_map(self, zone: int, map: 'Map') -> tuple:


# =================================================================================================
#
    def is_point_in_section(self, section: int, point: tuple) -> bool:
        for z in self.zones:
            if point in z:
                if section == z.section:
                    return True
                else:
                    return False
        return False
    
#endregion
