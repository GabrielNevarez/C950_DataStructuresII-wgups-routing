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
    """
    Controls the WGUPS program flow and user interface.

    The Menu class loads all data, creates the trucks,
    performs the routing simulation, handles Package 9's
    address correction, and provides the user with options
    to view package status and total mileage.
    """

    def __init__(self):
        """
        Initializes the WGUPS delivery simulation.
        """

        self.locations = LocationLoader.load(
            "Locations.csv"
        )

        self.packages = PackageLoader.load(
            "Packages.CSV",
            self.locations
        )

        self.distance_graph = DistanceLoader.load(
            "Distances.csv",
            self.locations
        )

        self.router = Router(
            self.distance_graph
        )

        self.trucks = TruckLoader.load(
            self.packages
        )

        self.truck1 = self.trucks[0]
        self.truck2 = self.trucks[1]
        self.truck3 = self.trucks[2]

        # Route Truck 1.
        self.router.deliver_packages(
            self.truck1
        )

        self.router.return_to_hub(
            self.truck1
        )

        # Route Truck 2.
        self.router.deliver_packages(
            self.truck2
        )

        self.router.return_to_hub(
            self.truck2
        )

        # Find the first available driver.
        if self.truck1.current_time <= self.truck2.current_time:
            driver_available = self.truck1.current_time
        else:
            driver_available = self.truck2.current_time

        # Package 9 address correction time.
        correction_time = datetime.strptime(
            "10:20 AM",
            "%I:%M %p"
        )

        # Truck 3 must wait for both the driver
        # and the corrected Package 9 address.
        if driver_available < correction_time:
            truck3_start = correction_time
        else:
            truck3_start = driver_available

        # Correct Package 9's address.
        package9 = self.packages.lookup(
            9
        )

        package9.address = "410 S State St"
        package9.city = "Salt Lake City"
        package9.state = "UT"
        package9.zip_code = "84111"
        package9.location_id = 19

        # Route Truck 3.
        self.truck3.set_start_time(
            truck3_start
        )

        self.router.deliver_packages(
            self.truck3
        )

        self.router.return_to_hub(
            self.truck3
        )

    def display(self):
        """
        Displays the main menu.
        """

        print()
        print("=" * 35)
        print("       WGUPS Routing Program")
        print("=" * 35)
        print("1. Look up package by ID")
        print("2. View delivery status by time")
        print("3. View all packages")
        print("4. View total mileage")
        print("5. Exit")
        print("=" * 35)

    def getOption(self, choice):
        """
        Executes the selected menu option.

        @param choice: User-entered menu selection.
        @return: False when exiting, otherwise True.
        """

        try:
            option = MenuOption(
                int(choice)
            )

            if option == MenuOption.LOOKUP_PACKAGE:
                self.lookup_package()

            elif option == MenuOption.VIEW_STATUS_BY_TIME:
                self.view_status_by_time()

            elif option == MenuOption.VIEW_ALL_PACKAGES:
                self.view_all_packages()

            elif option == MenuOption.VIEW_TOTAL_MILEAGE:
                self.view_total_mileage()

            elif option == MenuOption.EXIT:
                print(
                    "\nExiting program..."
                )
                return False

        except (ValueError, TypeError):
            print(
                "\nPlease enter a numeric value "
                "between 1 and 5."
            )

        return True

    def get_column_widths(self):
        """
        Calculates column widths using the actual package data.

        @return: Dictionary containing column widths.
        """

        all_packages = self.packages.get_all()

        widths = {
            "id": len("ID"),
            "truck": len("Truck"),
            "address": len("Address"),
            "city": len("City"),
            "state": len("State"),
            "zip": len("Zip"),
            "deadline": len("Deadline"),
            "weight": len("Weight"),
            "status": len("Status"),
            "delivery": len("Delivery Time")
        }

        for package in all_packages:
            widths["id"] = max(
                widths["id"],
                len(str(package.package_id))
            )

            widths["truck"] = max(
                widths["truck"],
                len(str(package.truck_id))
            )

            widths["address"] = max(
                widths["address"],
                len(package.address)
            )

            widths["city"] = max(
                widths["city"],
                len(package.city)
            )

            widths["state"] = max(
                widths["state"],
                len(package.state)
            )

            widths["zip"] = max(
                widths["zip"],
                len(str(package.zip_code))
            )

            widths["deadline"] = max(
                widths["deadline"],
                len(package.deadline)
            )

            widths["weight"] = max(
                widths["weight"],
                len(str(package.weight))
            )

            widths["status"] = max(
                widths["status"],
                len(package.status.value)
            )

            widths["delivery"] = max(
                widths["delivery"],
                len("12:00 PM")
            )

        return widths

    def print_header(self):
        """
        Prints the package table header.
        """

        widths = self.get_column_widths()

        header = (
            f"{'ID':<{widths['id']}}  "
            f"{'Truck':<{widths['truck']}}  "
            f"{'Address':<{widths['address']}}  "
            f"{'City':<{widths['city']}}  "
            f"{'State':<{widths['state']}}  "
            f"{'Zip':<{widths['zip']}}  "
            f"{'Deadline':<{widths['deadline']}}  "
            f"{'Weight':<{widths['weight']}}  "
            f"{'Status':<{widths['status']}}  "
            f"{'Delivery Time':<{widths['delivery']}}"
        )

        print()
        print(header)
        print("-" * len(header))

    def print_package(
        self,
        package,
        status=None,
        query_time=None
    ):
        """
        Prints one package in table format.

        @param package: Package object to display.
        @param status: Status to display.
        @param query_time: Optional historical query time.
        """

        widths = self.get_column_widths()

        if status is None:
            status = package.status

        # Determine whether the delivery time
        # should be visible at the requested time.
        if (
            package.delivery_time is not None
            and (
                query_time is None
                or query_time >= package.delivery_time
            )
        ):
            delivery_time = package.delivery_time.strftime(
                "%I:%M %p"
            )
        else:
            delivery_time = "N/A"

        if package.truck_id is None:
            truck_id = "N/A"
        else:
            truck_id = package.truck_id

        address = package.address
        city = package.city
        state = package.state
        zip_code = package.zip_code

        # Before 10:20 AM, Package 9 must show
        # its original incorrect address.
        if (
            package.package_id == 9
            and query_time is not None
        ):
            correction_time = datetime.strptime(
                "10:20 AM",
                "%I:%M %p"
            )

            if query_time < correction_time:
                address = "300 State St"
                city = "Salt Lake City"
                state = "UT"
                zip_code = "84103"

        print(
            f"{package.package_id:<{widths['id']}}  "
            f"{truck_id:<{widths['truck']}}  "
            f"{address:<{widths['address']}}  "
            f"{city:<{widths['city']}}  "
            f"{state:<{widths['state']}}  "
            f"{zip_code:<{widths['zip']}}  "
            f"{package.deadline:<{widths['deadline']}}  "
            f"{package.weight:<{widths['weight']}}  "
            f"{status.value:<{widths['status']}}  "
            f"{delivery_time:<{widths['delivery']}}"
        )

        # Print special notes below the package row
        # so long notes do not break table alignment.
        if package.special_notes.strip():
            print(
                f"    Special Note: "
                f"{package.special_notes}"
            )

    def lookup_package(self):
        """
        Looks up one package by package ID.
        """

        try:
            package_id = int(
                input(
                    "\nEnter package ID: "
                )
            )

            package = self.packages.lookup(
                package_id
            )

            if package is None:
                print(
                    "\nPackage not found."
                )
                return

            self.print_header()

            self.print_package(
                package
            )

        except ValueError:
            print(
                "\nPlease enter a valid package ID."
            )

    def view_status_by_time(self):
        """
        Displays all package statuses at a selected time.
        """

        time_string = input(
            "\nEnter time "
            "(example 8:35 AM or 08:35): "
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

            print()
            print("=" * 45)
            print(
                "Package Status at "
                f"{query_time.strftime('%I:%M %p')}"
            )
            print("=" * 45)

            self.print_header()

            all_packages = self.packages.get_all()

            all_packages.sort(
                key=lambda package: package.package_id
            )

            for package in all_packages:
                status = package.get_status_at(
                    query_time
                )

                self.print_package(
                    package,
                    status,
                    query_time
                )

        except ValueError:
            print(
                "\nPlease enter a valid time."
            )

    def view_all_packages(self):
        """
        Displays the final status of all packages.
        """

        print()
        print("=" * 45)
        print("Final Package Delivery Status")
        print("=" * 45)

        self.print_header()

        all_packages = self.packages.get_all()

        all_packages.sort(
            key=lambda package: package.package_id
        )

        for package in all_packages:
            self.print_package(
                package
            )

    def view_total_mileage(self):
        """
        Displays each truck's mileage and total mileage.
        """

        total_mileage = 0

        print()
        print("=" * 35)
        print("         Truck Mileage")
        print("=" * 35)

        for truck in self.trucks:
            total_mileage += truck.miles

            print(
                f"Truck {truck.truck_id}: "
                f"{truck.miles:.1f} miles"
            )

        print("-" * 35)

        print(
            f"Total Mileage: "
            f"{total_mileage:.1f} miles"
        )

        print("=" * 35)