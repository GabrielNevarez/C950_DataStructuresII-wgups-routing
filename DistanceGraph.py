from Location import Location


class DistanceGraph:
    def __init__(self, locations):
        self.locations = locations

        size = len(locations)

        # Create a square distance matrix.
        self.distances = []

        for i in range(size):
            self.distances.append([None] * size)

        # Distance from a location to itself is always 0.
        for i in range(size):
            self.distances[i][i] = 0.0

    def set_distance(self, location1_id, location2_id, distance):
        # Distances are symmetric, so store both directions.
        self.distances[location1_id][location2_id] = distance
        self.distances[location2_id][location1_id] = distance

    def get_distance(self, location1_id, location2_id):
        return self.distances[location1_id][location2_id]

    def get_location(self, location_id):
        return self.locations[location_id]