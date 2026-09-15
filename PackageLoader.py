from Package import Package
from Packages import Packages


class PackageLoader:

    @staticmethod
    def load():
        package_data = [
            Package(
                1,
                1,
                "1060 Dalton Ave S",
                "Salt Lake City",
                "UT",
                "84104",
                "10:30 AM",
                21
            ),

            Package(
                2,
                2,
                "1330 2100 S",
                "Salt Lake City",
                "UT",
                "84106",
                "EOD",
                44
            ),

            Package(
                3,
                3,
                "1488 4800 S",
                "Salt Lake City",
                "UT",
                "84123",
                "9:00 AM",
                10
            ),

            Package(
                4,
                4,
                "177 W Price Ave",
                "Salt Lake City",
                "UT",
                "84115",
                "EOD",
                5
            ),

            Package(
                5,
                5,
                "2010 W 500 S",
                "Salt Lake City",
                "UT",
                "84104",
                "10:30 AM",
                15
            ),

            Package(
                6,
                6,
                "2300 Parkway Blvd",
                "West Valley City",
                "UT",
                "84119",
                "EOD",
                8
            )
        ]

        packages = Packages(len(package_data) * 2)

        for package in package_data:
            packages.insert(package.package_id, package)

        return packages