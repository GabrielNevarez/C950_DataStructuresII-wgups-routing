from datetime import timedelta

from Package import PackageStatus
from Truck import Truck
from DistanceGraph import DistanceGraph


class Router:

    def __init__(self, distance_graph):
        self.distance_graph = distance_graph

    def get_nearest_package(self, truck):
        nearest_package = None
        shortest_distance = float("inf")

        for package in truck.packages:

            if package.status == PackageStatus.DELIVERED:
                continue

            distance = self.distance_graph.get_distance(
                truck.current_location,
                package.location_id
            )

            if distance < shortest_distance:
                shortest_distance = distance
                nearest_package = package

        return nearest_package, shortest_distance

    def deliver_packages(self, truck):
        truck.set_en_route()

        while truck.has_undelivered_packages():

            package, distance = self.get_nearest_package(truck)

            if package is None:
                break

            truck.miles += distance

            travel_minutes = (distance / truck.SPEED) * 60

            truck.current_time += timedelta(minutes=travel_minutes)
            truck.current_location = package.location_id

            package.status = PackageStatus.DELIVERED
            package.delivery_time = truck.current_time

    def return_to_hub(self, truck):
        hub_location = 0

        if truck.current_location == hub_location:
            return

        distance = self.distance_graph.get_distance(
            truck.current_location,
            hub_location
        )

        truck.miles += distance

        travel_minutes = (distance / truck.SPEED) * 60

        truck.current_time += timedelta(minutes=travel_minutes)
        truck.current_location = hub_location