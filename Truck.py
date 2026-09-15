from datetime import datetime

from Package import PackageStatus


class Truck:
    MAX_CAPACITY = 16
    SPEED = 18.0

    def __init__(self, truck_id, start_time):
        self.truck_id = truck_id

        if start_time is None:
            self.start_time = None
            self.current_time = None
        else:
            self.start_time = datetime.strptime(start_time, "%I:%M %p")
            self.current_time = self.start_time

        self.current_location = 0
        self.miles = 0.0
        self.packages = []

    def add_package(self, package):
        if package is None:
            return False

        if len(self.packages) >= self.MAX_CAPACITY:
            return False

        self.packages.append(package)
        package.truck_id = self.truck_id

        return True

    def has_undelivered_packages(self):
        for package in self.packages:
            if package.status != PackageStatus.DELIVERED:
                return True

        return False

    def set_en_route(self):
        for package in self.packages:
            if package.status != PackageStatus.DELIVERED:
                package.status = PackageStatus.EN_ROUTE
                package.departure_time = self.start_time

    def set_start_time(self, start_time):
        self.start_time = start_time
        self.current_time = start_time