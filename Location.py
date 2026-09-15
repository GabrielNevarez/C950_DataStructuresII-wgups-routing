class Location:
    """
    Represents one WGUPS delivery location.

    Each location has a numeric ID used by the distance graph
    and a delivery address used for package matching.
    """

    def __init__(self, location_id, address):
        """
        Creates a Location object.

        @param location_id: Numeric ID used by the distance graph.
        @param address: Street address of the delivery location.
        """

        self.location_id = location_id
        self.address = address

    def __str__(self):
        """
        Returns a readable representation of the location.

        @return: String containing the location ID and address.
        """

        return (
            f"{self.location_id}: "
            f"{self.address}"
        )