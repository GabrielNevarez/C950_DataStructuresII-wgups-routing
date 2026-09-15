from datetime import datetime
from enum import Enum


class PackageStatus(Enum):
    DELAYED = "Delayed"
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"


class Package:
    """
    Represents one package in the WGUPS delivery system.

    Stores package data, truck assignment, departure time,
    delivery time, and determines historical delivery status.
    """

    def __init__(
        self,
        package_id,
        location_id,
        address,
        city,
        state,
        zip_code,
        deadline,
        weight,
        special_notes=""
    ):
        """
        Creates a Package object.

        @param package_id: Unique package ID used as the hash table key.
        @param location_id: Numeric location ID used by the distance graph.
        @param address: Package delivery address.
        @param city: Package delivery city.
        @param state: Package delivery state.
        @param zip_code: Package delivery ZIP code.
        @param deadline: Required delivery deadline.
        @param weight: Package weight in kilograms.
        @param special_notes: Special delivery instructions from the package file.
        """

        self.package_id = package_id
        self.location_id = location_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes

        # Packages begin at the hub unless a historical
        # query determines they were delayed.
        self.status = PackageStatus.AT_HUB

        # Truck assignment is set when TruckLoader
        # adds the package to a truck.
        self.truck_id = None

        # These values are populated during routing.
        self.departure_time = None
        self.delivery_time = None

    def get_status_at(self, query_time):
        """
        Returns the package delivery status at a specific time.

        @param query_time: datetime value representing the requested time.
        @return: PackageStatus showing delayed, at hub,
                 en route, or delivered.
        """

        # These packages are delayed and do not arrive
        # at the hub until 9:05 AM.
        delayed_packages = [
            6,
            25,
            28,
            32
        ]

        delayed_arrival_time = datetime.strptime(
            "9:05 AM",
            "%I:%M %p"
        )

        # Before 9:05 AM, delayed packages have not
        # reached the WGUPS hub.
        if (
            self.package_id in delayed_packages
            and query_time < delayed_arrival_time
        ):
            return PackageStatus.DELAYED

        # If the requested time is at or after the
        # recorded delivery time, the package is delivered.
        if (
            self.delivery_time is not None
            and query_time >= self.delivery_time
        ):
            return PackageStatus.DELIVERED

        # If the truck has already departed but the package
        # has not been delivered, the package is en route.
        if (
            self.departure_time is not None
            and query_time >= self.departure_time
        ):
            return PackageStatus.EN_ROUTE

        # Otherwise the package is still waiting at the hub.
        return PackageStatus.AT_HUB