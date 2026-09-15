from datetime import datetime

from Package import PackageStatus


class Truck:
    """
    Represents one WGUPS delivery truck.

    Stores the truck's package list, current location,
    current time, mileage, and delivery capacity.
    """

    MAX_CAPACITY = 16
    SPEED = 18.0

    def __init__(self, truck_id, start_time):
        """
        Creates a Truck object.

        @param truck_id: Unique truck number.
        @param start_time: Departure time as a string such as
                           "8:00 AM", or None if the truck waits
                           for a driver.
        """

        self.truck_id = truck_id

        # Trucks with a known departure time are converted
        # to datetime objects for routing calculations.
        if start_time is None:
            self.start_time = None
            self.current_time = None
        else:
            self.start_time = datetime.strptime(
                start_time,
                "%I:%M %p"
            )

            self.current_time = self.start_time

        # Location 0 represents the WGUPS hub.
        self.current_location = 0

        # Total mileage traveled by this truck.
        self.miles = 0.0

        # Stores the Package objects assigned to this truck.
        self.packages = []

    def add_package(self, package):
        """
        Adds a package to the truck if capacity is available.

        @param package: Package object to load onto the truck.
        @return: True if added successfully, otherwise False.
        """

        if package is None:
            return False

        # Each truck can carry a maximum of 16 packages.
        if len(self.packages) >= self.MAX_CAPACITY:
            return False

        self.packages.append(package)

        # Store the truck assignment on the package so the
        # interface can display which truck carries it.
        package.truck_id = self.truck_id

        return True

    def has_undelivered_packages(self):
        """
        Checks whether the truck still has packages to deliver.

        @return: True if at least one package has not been
                 delivered, otherwise False.
        """

        for package in self.packages:
            if package.status != PackageStatus.DELIVERED:
                return True

        return False

    def set_en_route(self):
        """
        Marks all undelivered packages on the truck as en route
        and records the truck departure time on each package.
        """

        for package in self.packages:

            if package.status != PackageStatus.DELIVERED:
                package.status = PackageStatus.EN_ROUTE
                package.departure_time = self.start_time

    def set_start_time(self, start_time):
        """
        Sets the start time for a truck that was waiting
        for an available driver.

        @param start_time: datetime value representing the
                           truck's actual departure time.
        """

        self.start_time = start_time
        self.current_time = start_time