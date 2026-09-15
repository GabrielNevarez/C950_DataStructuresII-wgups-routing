from enum import Enum

from PackageLoader import PackageLoader


class MenuOption(Enum):
    VIEW_PACKAGE_STATUS = 1
    VIEW_ALL_PACKAGES = 2
    VIEW_TOTAL_MILEAGE = 3
    EXIT = 4


class Menu:
    def __init__(self):
        self.packages = PackageLoader.load()

    def display(self):
        print("\nWGUPS Routing Program")
        print("1. View package status")
        print("2. View all packages")
        print("3. View total mileage")
        print("4. Exit")

    def get_option(self, choice):
        try:
            option = MenuOption(int(choice))

            if option == MenuOption.VIEW_PACKAGE_STATUS:
                self.view_package_status()

            elif option == MenuOption.VIEW_ALL_PACKAGES:
                self.view_all_packages()

            elif option == MenuOption.VIEW_TOTAL_MILEAGE:
                self.view_total_mileage()

            elif option == MenuOption.EXIT:
                print("Exiting program...")
                return False

        except (ValueError, TypeError):
            print("Please enter a numeric value between 1 and 4")

        return True

    def view_package_status(self):
        try:
            package_id = int(input("Enter package ID: "))
            package = self.packages.lookup(package_id)

            if package is None:
                print("Package not found.")
            else:
                print(package)

        except ValueError:
            print("Please enter a valid package ID.")

    def view_all_packages(self):
        print()
        print(
            f"{'ID':<4} "
            f"{'Truck':<7} "
            f"{'Address':<28} "
            f"{'City':<18} "
            f"{'State':<5} "
            f"{'Zip':<8} "
            f"{'Deadline':<12} "
            f"{'Weight':<8} "
            f"{'Status':<12} "
            f"{'Delivery Time':<15}"
        )

        print("-" * 135)

        for package in self.packages.get_all():
            print(package)

    def view_total_mileage(self):
        print("Total mileage not implemented yet.")