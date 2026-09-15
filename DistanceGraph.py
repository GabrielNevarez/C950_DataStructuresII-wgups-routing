from Location import Location


class DistanceGraph:
    """
    Stores the mileage between WGUPS delivery locations.

    Distances are stored in a two-dimensional matrix using
    numeric location IDs. Because the provided distance table
    is symmetric, each distance is stored in both directions.
    """

    def __init__(self, locations):
        """
        Creates a DistanceGraph for the supplied locations.

        @param locations: List of Location objects ordered by
                          their numeric location ID.
        """

        self.locations = locations

        size = len(locations)
        self.distances = []

        # Create an empty square matrix large enough
        # to store every location-to-location distance.
        for i in range(size):
            self.distances.append(
                [None] * size
            )

        # The distance from a location to itself
        # is always zero miles.
        for i in range(size):
            self.distances[i][i] = 0.0

    def set_distance(
        self,
        location1_id,
        location2_id,
        distance
    ):
        """
        Stores the distance between two locations.

        @param location1_id: ID of the first location.
        @param location2_id: ID of the second location.
        @param distance: Mileage between the two locations.
        """

        # The WGUPS distance table is symmetric,
        # so store the same value in both directions.
        self.distances[
            location1_id
        ][location2_id] = distance

        self.distances[
            location2_id
        ][location1_id] = distance

    def get_distance(
        self,
        location1_id,
        location2_id
    ):
        """
        Returns the mileage between two locations.

        @param location1_id: ID of the starting location.
        @param location2_id: ID of the destination location.
        @return: Distance in miles between the locations.
        """

        return self.distances[
            location1_id
        ][location2_id]

    def get_location(self, location_id):
        """
        Returns a Location object by its numeric ID.

        @param location_id: Numeric location ID.
        @return: Matching Location object.
        """

        return self.locations[
            location_id
        ]