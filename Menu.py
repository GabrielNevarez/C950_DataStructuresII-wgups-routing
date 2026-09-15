from datetime import datetime
from enum import Enum

from PackageLoader import PackageLoader
from TruckLoader import TruckLoader
from LocationLoader import LocationLoader
from DistanceLoader import DistanceLoader
from Router import Router


class MenuOption(Enum):
    LOOKUP_PACKAGE = 1
    VIEW_STATUS_BY_TIME = 2
    VIEW_ALL_PACKAGES = 3
    VIEW_TOTAL_MILEAGE = 4
    EXIT = 5


class Menu:

    def __init__(self):
        # Load packages.
        self.packages = PackageLoader.load()

        # Load locations and distances.
        self.locations = LocationLoader.load()
        self.distance_graph = DistanceLoader.load(self.locations)

        # Create router.
        self.router = Router(self.distance_graph)

        # Load trucks.
        self.trucks = TruckLoader.load(self.packages)

        self.truck1 = self.trucks[0]
        self.truck2 = self.trucks[1]
        self.truck3 = self.trucks[2]

        # Route Truck 1.
        self.router.deliver_packages(self.truck1)
        self.router.return_to_hub(self.truck1)

        # Route Truck 2.
        self.router.deliver_packages(self.truck2)
        self.router.return_to_hub(self.truck2)

        # Truck 3 starts when the first driver returns.
        if self.truck1.current_time <= self.truck2.current_time:
            self.truck3.set_start_time(self.truck1.current_time)
        else:
            self.truck3.set_start_time(self.truck2.current_time)

        # Route Truck 3.
        self.router.deliver_packages(self.truck3)
        self.router.return_to_hub(self.truck3)

    def display(self):
        print("\nWGUPS Routing Program")
        print("1. Look up package by ID")
        print("2. View delivery status by time")
        print("3. View all packages")
        print("4. View total mileage")
        print("5. Exit")

    def getOption(self, choice):
        try:
            option = MenuOption(int(choice))

            if option == MenuOption.LOOKUP_PACKAGE:
                self.lookup_package()

            elif option == MenuOption.VIEW_STATUS_BY_TIME:
                self.view_status_by_time()

            elif option == MenuOption.VIEW_ALL_PACKAGES:
                self.view_all_packages()

            elif option == MenuOption.VIEW_TOTAL_MILEAGE:
                self.view_total_mileage()

            elif option == MenuOption.EXIT:
                print("Exiting program...")
                return False

        except (ValueError, TypeError):
            print("Please enter a numeric value between 1 and 5.")

        return True

    def print_header(self):
        print()
        print(
            f"{'ID':<4} "
            f"{'Truck':<7} "
            f"{'Address':<28} "
            f"{'City':<18} "
            f"{'State':<6} "
            f"{'Zip':<8} "
            f"{'Deadline':<12} "
            f"{'Weight':<8} "
            f"{'Status':<12} "
            f"{'Delivery Time':<15}"
        )

        print("-" * 135)

    def print_package(self, package, status=None, query_time=None):
        if status is None:
            status = package.status

        # Only show delivery time if the package
        # was delivered by the requested time.
        if (
            package.delivery_time is not None
            and (
                query_time is None
                or query_time >= package.delivery_time
            )
        ):
            delivery_time = package.delivery_time.strftime(
                "%I:%M:%S %p"
            )
        else:
            delivery_time = "N/A"

        truck_id = (
            package.truck_id
            if package.truck_id is not None
            else "N/A"
        )

        print(
            f"{package.package_id:<4} "
            f"{truck_id:<7} "
            f"{package.address:<28} "
            f"{package.city:<18} "
            f"{package.state:<6} "
            f"{package.zip_code:<8} "
            f"{package.deadline:<12} "
            f"{package.weight:<8} "
            f"{status.value:<12} "
            f"{delivery_time:<15}"
        )

    def lookup_package(self):
        try:
            package_id = int(
                input("Enter package ID: ")
            )

            package = self.packages.lookup(package_id)

            if package is None:
                print("Package not found.")
                return

            self.print_header()
            self.print_package(package)

        except ValueError:
            print("Please enter a valid package ID.")

    def view_status_by_time(self):
        time_string = input(
            "Enter time (example 8:35 AM or 08:35): "
        )

        try:
            try:
                query_time = datetime.strptime(
                    time_string,
                    "%I:%M %p"
                )
            except ValueError:
                query_time = datetime.strptime(
                    time_string,
                    "%H:%M"
                )

            print(
                f"\nPackage status at "
                f"{query_time.strftime('%I:%M %p')}"
            )

            self.print_header()

            for package in self.packages.get_all():
                status = package.get_status_at(query_time)

                self.print_package(
                    package,
                    status,
                    query_time
                )

        except ValueError:
            print("Please enter a valid time.")

    def view_all_packages(self):
        self.print_header()

        for package in self.packages.get_all():
            self.print_package(package)

    def view_total_mileage(self):
        total_mileage = 0

        print()

        for truck in self.trucks:
            total_mileage += truck.miles

            print(
                f"Truck {truck.truck_id}: "
                f"{truck.miles:.1f} miles"
            )

        print(
            f"\nTotal Mileage: "
            f"{total_mileage:.1f} miles"
        )