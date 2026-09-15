from datetime import timedelta

from Package import PackageStatus
from Truck import Truck
from DistanceGraph import DistanceGraph


class Router:
    """
    Handles truck routing using the Nearest Neighbor algorithm.

    The router repeatedly selects the closest undelivered package
    from the truck's current location, updates mileage and time,
    and records the package delivery information.
    """

    def __init__(self, distance_graph):
        """
        Creates a Router object.

        @param distance_graph: DistanceGraph containing the mileage
                               between delivery locations.
        """

        self.distance_graph = distance_graph

    def get_nearest_package(self, truck):
        """
        Finds the closest undelivered package on the truck.

        @param truck: Truck object currently being routed.
        @return: Tuple containing the nearest Package object
                 and the distance to that package.
        """

        nearest_package = None
        shortest_distance = float("inf")

        # Check every undelivered package currently assigned
        # to the truck.
        for package in truck.packages:

            if package.status == PackageStatus.DELIVERED:
                continue

            distance = self.distance_graph.get_distance(
                truck.current_location,
                package.location_id
            )

            # Keep the package with the shortest distance
            # from the truck's current location.
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_package = package

        return nearest_package, shortest_distance

    def deliver_packages(self, truck):
        """
        Delivers all packages assigned to a truck using
        the Nearest Neighbor algorithm.

        @param truck: Truck object whose packages will be delivered.
        """

        # Mark every package on the truck as en route and
        # record the truck departure time.
        truck.set_en_route()

        # Continue routing until every assigned package
        # has been delivered.
        while truck.has_undelivered_packages():

            package, distance = self.get_nearest_package(
                truck
            )

            # Stop if no valid package can be found.
            if package is None:
                break

            # Add the travel distance to the truck's
            # accumulated mileage.
            truck.miles += distance

            # Travel time is calculated using the required
            # average truck speed of 18 miles per hour.
            travel_minutes = (
                distance / truck.SPEED
            ) * 60

            truck.current_time += timedelta(
                minutes=travel_minutes
            )

            # The truck's current location becomes the
            # location of the package just delivered.
            truck.current_location = (
                package.location_id
            )

            # Record the final delivery status and time.
            package.status = PackageStatus.DELIVERED
            package.delivery_time = truck.current_time

    def return_to_hub(self, truck):
        """
        Returns a truck to the WGUPS hub after completing
        its assigned deliveries.

        @param truck: Truck object returning to the hub.
        """

        hub_location = 0

        # If the truck is already at the hub,
        # no additional travel is needed.
        if truck.current_location == hub_location:
            return

        distance = self.distance_graph.get_distance(
            truck.current_location,
            hub_location
        )

        # Add the return distance to the truck's
        # total mileage.
        truck.miles += distance

        # Calculate how long the return trip takes
        # using the truck's 18 MPH average speed.
        travel_minutes = (
            distance / truck.SPEED
        ) * 60

        truck.current_time += timedelta(
            minutes=travel_minutes
        )

        # Location 0 represents the WGUPS hub.
        truck.current_location = hub_location