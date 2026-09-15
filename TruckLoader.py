from Truck import Truck


class TruckLoader:

    @staticmethod
    def load(packages):
        truck1 = Truck(1, "8:00 AM")
        truck2 = Truck(2, "8:00 AM")
        truck3 = Truck(3, None)

        truck1.add_package(packages.lookup(1))
        truck1.add_package(packages.lookup(2))

        truck2.add_package(packages.lookup(3))
        truck2.add_package(packages.lookup(4))

        truck3.add_package(packages.lookup(5))
        truck3.add_package(packages.lookup(6))

        return [truck1, truck2, truck3]