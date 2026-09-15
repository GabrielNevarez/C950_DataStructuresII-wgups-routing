from Truck import Truck


class TruckLoader:
    """
    Creates the three WGUPS trucks and assigns packages to them.

    Package assignments are hard-coded to satisfy the known delivery
    constraints from the package file, including truck restrictions,
    delayed packages, grouped packages, and Package 9 handling.
    """

    @staticmethod
    def load(packages):
        """
        Creates the trucks and loads their assigned packages.

        @param packages: Packages hash table containing all Package objects.
        @return: List containing Truck 1, Truck 2, and Truck 3.
        """

        # Truck 1 leaves the hub at 8:00 AM.
        truck1 = Truck(
            1,
            "8:00 AM"
        )

        # Truck 2 leaves at 9:05 AM so delayed packages
        # are available before departure.
        truck2 = Truck(
            2,
            "9:05 AM"
        )

        # Truck 3 waits until a driver is available and
        # Package 9's corrected address is known.
        truck3 = Truck(
            3,
            None
        )

        # Truck 1 package assignments.
        # Packages 13, 14, 15, 16, 19, and 20
        # are kept on the same truck as required.
        truck1_packages = [
            1,
            2,
            4,
            7,
            13,
            14,
            15,
            16,
            19,
            20,
            29,
            30,
            31,
            34,
            37,
            40
        ]

        # Truck 2 package assignments.
        # Packages 3, 18, 36, and 38 are restricted
        # to Truck 2.
        #
        # Packages 6, 25, 28, and 32 are delayed
        # and are not available until 9:05 AM.
        truck2_packages = [
            3,
            5,
            6,
            8,
            10,
            11,
            12,
            17,
            18,
            23,
            24,
            25,
            28,
            32,
            36,
            38
        ]

        # Truck 3 package assignments.
        # Package 9 is included here so this truck can
        # wait until the corrected address is known at 10:20 AM.
        truck3_packages = [
            9,
            21,
            22,
            26,
            27,
            33,
            35,
            39
        ]

        # Load Truck 1.
        for package_id in truck1_packages:
            package = packages.lookup(
                package_id
            )

            truck1.add_package(
                package
            )

        # Load Truck 2.
        for package_id in truck2_packages:
            package = packages.lookup(
                package_id
            )

            truck2.add_package(
                package
            )

        # Load Truck 3.
        for package_id in truck3_packages:
            package = packages.lookup(
                package_id
            )

            truck3.add_package(
                package
            )

        return [
            truck1,
            truck2,
            truck3
        ]