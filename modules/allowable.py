from enums import Map_Matchups
from modules.map import Map
from modules.zone import Zone

class Allowable:
    # Map Matchup Ids
    map_match_basic = Map_Matchups.basic.value
    map_match_lava = Map_Matchups.lava.value
    map_match_water = Map_Matchups.water.value
    map_match_rubble = Map_Matchups.rubble.value
    map_match_flying = Map_Matchups.flying.value
    map_match_lava_basic = Map_Matchups.lava_basic.value
    map_match_water_basic = Map_Matchups.water_basic.value
    map_match_rubble_basic = Map_Matchups.rubble_basic.value
    map_match_flying_basic = Map_Matchups.flying_basic.value
    map_match_flying_lava = Map_Matchups.flying_lava.value
    map_match_flying_water = Map_Matchups.flying_water.value
    map_match_flying_rubble = Map_Matchups.flying_rubble.value

    def __init__(self, id: int, pivot_map: 'Map' = None, hero_map: 'Map' = None):
        self.id = id
        self.pivot_map = pivot_map
        self.hero_map = hero_map
        self.points = self.get_points()

# =================================================================================================
# POINTS
# =================================================================================================
# region POINTS

    def get_points(self):
        points = None

        if self.id == self.map_match_basic or self.id == self.map_match_lava or self.id == self.map_match_water or self.id == self.map_match_rubble or self.id == self.map_match_flying:
            points = self.get_all_points_of_map_same(self.hero_map)
        elif self.id == self.map_match_lava_basic:
            pass
        elif self.id == self.map_match_water_basic:
            pass
        elif self.id == self.map_match_rubble_basic:
            pass
        elif self.id == self.map_match_flying_basic:
            pass
        elif self.id == self.map_match_flying_lava:
            pass
        elif self.id == self.map_match_flying_water:
            pass
        elif self.id == self.map_match_flying_rubble:
            pass
        
        return points

# =================================================================================================
# Gets all allowable points of this map if both the pivot and the movable hero share this map.
# For example, if this map is a Lava map and both the pivot and the hero are lava walkers,
# then this will get all allowable points the hero can move to based on what section and path
# the pivot is on and what zone the hero is in.
# The list is a nested list that represents: 
#       start_zone_of_pivot > end_zone_of_pivot > hero_zone
# For example, if the pivot is moving from zone 2 to 9 and the movable hero is in zone 10,
# you can get the hero's allowable points by: list[2][9][10]
    def get_all_points_of_map_same(self, map: 'Map') -> list[list[list[tuple]]]:
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
                for h in range(len(map.zones)):
                    if h in main_path:
                        points = self.get_points_main_path(map, main_path, h)
                    else:
                        alt_path_id = map.get_path_id(s, h)
                        if alt_path_id is None:
                            continue
                        alt_path = map.paths[alt_path_id]
                        points = self.get_points_alt_path(map, main_path, alt_path, h)
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
    def get_all_points_mismatch_maps(self) -> dict[tuple[tuple[int, int], tuple[int, int]], str]:
        result = {}
        rows = len(self.pivot_map.board)
        cols = len(self.pivot_map.board[0]) if rows > 0 else 0

        for r1 in range(rows):
            for c1 in range(cols):
                for r2 in range(rows):
                    for c2 in range(cols):
                        if r1 == r2 and c1 == c2:
                            continue
                        point_pivot = (r1, c1)
                        point_hero = (r2, c2)
                        path_exists = self.does_path_exist(self.pivot_map.board, point_pivot, point_hero)
                        if path_exists:
                            hero_zone = self.get_zone_of_point(point_hero)
                            allowable_points = []
                            allowable_points.extend(self.get_points_in_zone(hero_zone))
                            is_pivot_de = self.is_pivot_deadend(self.pivot_map, point_hero)
                            if is_pivot_de:
                                pass
                            else:
                                pass
                            result[(point_pivot, point_hero)] = allowable_points

        return result

# =================================================================================================
    def get_all_points_of_map_diff(self, pivot_map: 'Map', hero_map: 'Map') -> list[list[list[tuple]]]:
        num_zones = len(pivot_map.zones)
        allowable_points = [[[None for _ in range(num_zones)] for _ in range(num_zones)] for _ in range(num_zones)]

        # s represents Pivot Start Zone
        # e represents Pivot End Zone
        # h represents Hero Zone
        for s in range(len(pivot_map.zones)):
            for e in range(len(pivot_map.zones)):
                main_path = pivot_map.get_path_from_start_to_end(s, e)
                if main_path is None:
                    continue
                for h in range(len(hero_map.zones)):
                    hero_start_zone_pivot_perspective = self.get_zone_pivot_perspective(h, hero_map, pivot_map)
                    if hero_start_zone_pivot_perspective in main_path:
                        points = self.get_points_main_path_diff(hero_map, pivot_map, main_path, h, hero_start_zone_pivot_perspective)
                    else:
                        alt_path = pivot_map.get_path_from_start_to_end(s, hero_start_zone_pivot_perspective)
                        if alt_path is None:
                            continue
                        points = self.get_points_alt_path_diff(hero_map, pivot_map, main_path, alt_path, h, hero_start_zone_pivot_perspective)
                    allowable_points[s][e][h] = points
        return allowable_points
    
# =================================================================================================
# The pivot map and the hero map differ, therfore their zones do not match up.
# This method will get the hero zones for the pivot zone given.
    def get_zones_hero_perspective(self, pivot_zone: int, pivot_map: 'Map', hero_map: 'Map') -> list[int]:
        list = []
        for p in pivot_map.zones[pivot_zone].points:
            for z in hero_map.zones:
                if p in z.points and z.id not in list:
                    list.append(z.id)
                    break
        return list
    
# =================================================================================================
# The pivot map and the hero map differ, therfore their zones do not match up.
# This method will get the pivot zone that corresponds to the hero zone given.
    def get_zone_pivot_perspective(self, hero_zone: int, hero_map: 'Map', pivot_map: 'Map') -> int:
        for z in pivot_map.zones:
            if hero_map.zones[hero_zone].points[0] in z.points:
                return z.id
        return None
    
# =================================================================================================
# Gets a list of all allowable points for a moveable hero who is on the main path of the pivot
# zones = a list of Zone objects for the given board (should only be 1 section)
# main_path = a list of zones the pivot moves through
# start_zone = the starting zone of the movable hero
    def get_points_main_path(self, map: 'Map', main_path_of_pivot: list[int], hero_start_zone_id: int):
        allowable_points = []
        allowable_zones = []

        # A movable hero can move anywhere in his current zone unless it is a DE
        # because being on the main path of the pivot, he is forced off his DE to the previous zone
        if not map.is_deadend_zone(hero_start_zone_id, map.zones):
            allowable_zones.append(hero_start_zone_id)

        # Hero starts on a deadend zone
        if map.is_deadend_zone(hero_start_zone_id, map.zones):
            previous_zone_id = map.get_previous_zone_id(hero_start_zone_id, main_path_of_pivot)
            if previous_zone_id is not None:
                # Hero can move anywhere in the previous zone
                allowable_zones.append(previous_zone_id)
                # Hero can move to previous zones connected deadend zones, with exceptions
                connected_deadend_zones = map.get_connected_deadend_zone_ids(previous_zone_id, map.zones)
                connected_deadend_zones.remove(hero_start_zone_id) # Cannot move to his start zone because it is a DE on the main path
                # If the previous zone from the hero start is a DE
                if map.is_deadend_zone(previous_zone_id, map.zones):
                    previous_previous_zone_id = map.get_previous_zone_id(previous_zone_id, main_path_of_pivot)
                    # If the previous zone from the previous zone from the hero start is a DE
                    # This is describing a single row or column of DEs
                    if previous_previous_zone_id and map.is_deadend_zone(previous_previous_zone_id, map.zones):
                        # Cannot move to the DE prior to the DE the hero got displaced on because it is a single row/col of DEs
                        connected_deadend_zones.remove(previous_previous_zone_id)
                allowable_zones.extend(connected_deadend_zones)

        # Movable hero starts on a nondeadend zone
        else:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the downstream zone on the main path
            connected_deadend_zones = map.get_connected_deadend_zone_ids(hero_start_zone_id, map.zones)
            next_deadend_zone_id = map.get_next_deadend_zone_id(hero_start_zone_id, main_path_of_pivot, map.zones) # downstream deadend zone
            if next_deadend_zone_id:
                connected_deadend_zones.remove(next_deadend_zone_id)
            allowable_zones.extend(connected_deadend_zones)

        # Add the points from the allowable zones to the list
        for z in allowable_zones:
            allowable_points.extend(map.get_points_in_zone(z, map.zones))

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
    def get_points_alt_path(self, map: 'Map', main_path_of_pivot: list[int], alt_path_of_pivot: list[int], hero_start_zone_id: int):
        allowable_points = []  # Allow duplicates
        allowable_zones = []

        # A movable hero can move anywhere in his current zone
        allowable_zones.append(hero_start_zone_id)

        # Movable hero starts on a deadend zone
        if map.is_deadend_zone(hero_start_zone_id, map.zones):
            previous_zone_id = map.get_previous_zone_id(hero_start_zone_id, alt_path_of_pivot)
            if previous_zone_id is not None:
                # If the previous zone is a deadend:
                if map.is_deadend_zone(previous_zone_id, map.zones):
                    pass # No allowable points in the previous zone
                else: # If the previous zone is not a deadend
                    # Hero starts on deadend zone can move to the previous nondeadend zone
                    allowable_zones.append(previous_zone_id)
                    connected_deadend_zones = map.get_connected_deadend_zone_ids(previous_zone_id, map.zones)
                    # Previous nondeadend zone is on the main path
                    if map.zone_is_on_main_path(previous_zone_id, main_path_of_pivot):
                        restricted_zone_id = map.get_next_deadend_zone_id(previous_zone_id, main_path_of_pivot, map.zones) # Downstream
                    # Previous nondeadend zone is not on the main path
                    else:
                        restricted_zone_id = map.get_previous_deadend_zone_id(previous_zone_id, alt_path_of_pivot, map.zones) # Upstream

                    # Add the allowable connected deadend zones
                    if restricted_zone_id:
                        connected_deadend_zones.remove(restricted_zone_id)

                    allowable_zones.extend(connected_deadend_zones)

        # Movable hero starts on a nondeadend zone
        else:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the upstream zone on the alt path
            connected_deadend_zones = map.get_connected_deadend_zone_ids(hero_start_zone_id, map.zones)
            restricted_zone_id = map.get_previous_deadend_zone_id(hero_start_zone_id, alt_path_of_pivot, map.zones)
            connected_deadend_zones.remove(restricted_zone_id)
            allowable_zones.extend(connected_deadend_zones)

        # Add the points from the allowable zones to the list
        for z in allowable_zones:
            allowable_points.extend(map.get_points_in_zone(z, map.zones))

        # Remove dups
        unique_points = self.remove_duplicates(allowable_points)
        
        # Sort the resulting list of points by row and then by column
        allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

        return allowable_points

# =================================================================================================
#
    def get_points_main_path_diff(self, hero_map: 'Map', map: 'Map', main_path_of_pivot: list[int], hero_start_zone_id_hero_perspective: int, hero_start_zone_id: int):
        allowable_points = []
        allowable_zones = []

        # A movable hero can move anywhere in his current zone unless it is a DE
        # because being on the main path of the pivot, he is forced off his DE to the previous zone
        if not map.is_deadend_zone(hero_start_zone_id, map.zones):
            allowable_zones.append(hero_start_zone_id)

        # Hero starts on a deadend zone
        if map.is_deadend_zone(hero_start_zone_id, map.zones):
            previous_zone_id = map.get_previous_zone_id(hero_start_zone_id, main_path_of_pivot)
            if previous_zone_id is not None:
                # Hero can move anywhere in the previous zone
                allowable_zones.append(previous_zone_id)
                # Hero can move to previous zones connected deadend zones, with exceptions
                connected_deadend_zones = map.get_connected_deadend_zone_ids(previous_zone_id, map.zones)
                connected_deadend_zones.remove(hero_start_zone_id) # Cannot move to his start zone because it is a DE on the main path
                # If the previous zone from the hero start is a DE
                if map.is_deadend_zone(previous_zone_id, map.zones):
                    previous_previous_zone_id = map.get_previous_zone_id(previous_zone_id, main_path_of_pivot)
                    # If the previous zone from the previous zone from the hero start is a DE
                    # This is describing a single row or column of DEs
                    if previous_previous_zone_id and map.is_deadend_zone(previous_previous_zone_id, map.zones):
                        # Cannot move to the DE prior to the DE the hero got displaced on because it is a single row/col of DEs
                        connected_deadend_zones.remove(previous_previous_zone_id)
                allowable_zones.extend(connected_deadend_zones)

        # Movable hero starts on a nondeadend zone
        else:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the downstream zone on the main path
            connected_deadend_zones = map.get_connected_deadend_zone_ids(hero_start_zone_id, map.zones)
            next_deadend_zone_id = map.get_next_deadend_zone_id(hero_start_zone_id, main_path_of_pivot, map.zones) # downstream deadend zone
            if next_deadend_zone_id:
                connected_deadend_zones.remove(next_deadend_zone_id)
            allowable_zones.extend(connected_deadend_zones)

        # Add the points from the allowable zones to the list
        for z in allowable_zones:
            allowable_points.extend(map.get_points_in_zone(z, map.zones))

        # Remove dups
        unique_points = self.remove_duplicates(allowable_points)

        # Sort the resulting list of points by row and then by column
        allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

        return allowable_points
    
# =================================================================================================
#
    def get_points_alt_path_diff(self, map: 'Map', pivot_map: 'Map', main_path_of_pivot: list[int], alt_path_of_pivot: list[int], hero_start_zone_id: int, hero_start_zone_id_pivot_eq: int):
        allowable_points = []  # Allow duplicates
        allowable_zones = []

        # A movable hero can move anywhere in his current zone
        allowable_zones.append(hero_start_zone_id)

        # Movable hero starts on a deadend zone
        if map.is_deadend_zone(hero_start_zone_id, map.zones):
            previous_zone_id = map.get_previous_zone_id(hero_start_zone_id, alt_path_of_pivot)
            if previous_zone_id is not None:
                # If the previous zone is a deadend:
                if map.is_deadend_zone(previous_zone_id, map.zones):
                    pass # No allowable points in the previous zone
                else: # If the previous zone is not a deadend
                    # Hero starts on deadend zone can move to the previous nondeadend zone
                    allowable_zones.append(previous_zone_id)
                    connected_deadend_zones = map.get_connected_deadend_zone_ids(previous_zone_id, map.zones)
                    # Previous nondeadend zone is on the main path
                    if map.zone_is_on_main_path(previous_zone_id, main_path_of_pivot):
                        restricted_zone_id = map.get_next_deadend_zone_id(previous_zone_id, main_path_of_pivot, map.zones) # Downstream
                    # Previous nondeadend zone is not on the main path
                    else:
                        restricted_zone_id = map.get_previous_deadend_zone_id(previous_zone_id, alt_path_of_pivot, map.zones) # Upstream

                    # Add the allowable connected deadend zones
                    if restricted_zone_id:
                        connected_deadend_zones.remove(restricted_zone_id)

                    allowable_zones.extend(connected_deadend_zones)

        # Movable hero starts on a nondeadend zone
        else:
            # Movable hero starts on nondeadend zone can move to any connected deadend zone of his
            # start zone except the upstream zone on the alt path
            connected_deadend_zones = map.get_connected_deadend_zone_ids(hero_start_zone_id, map.zones)
            restricted_zone_id = map.get_previous_deadend_zone_id(hero_start_zone_id, alt_path_of_pivot, map.zones)
            connected_deadend_zones.remove(restricted_zone_id)
            allowable_zones.extend(connected_deadend_zones)

        # Add the points from the allowable zones to the list
        for z in allowable_zones:
            allowable_points.extend(map.get_points_in_zone(z, map.zones))

        # Remove dups
        unique_points = self.remove_duplicates(allowable_points)
        
        # Sort the resulting list of points by row and then by column
        allowable_points = sorted(unique_points, key=lambda p: (p[0], p[1]))

        return allowable_points

# =================================================================================================
    def remove_duplicates(self, list):
        return [t for t in (set(tuple(i) for i in list))]
    
#endregion
