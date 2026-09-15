from Package import Package
from Packages import Packages


class PackageLoader:

    @staticmethod
    def load():
        # Temporary manual data.
        # Later this list will come from the package file.

        package_data = [
            Package(
                1,
                "195 W Oakland Ave",
                "Salt Lake City",
                "UT",
                "84115",
                "10:30 AM",
                21
            ),

            Package(
                2,
                "2530 S 500 E",
                "Salt Lake City",
                "UT",
                "84106",
                "EOD",
                44
            )
        ]

        # Create the HashMap based on the number of packages.
        packages = Packages(len(package_data) * 2)

        for package in package_data:
            packages.insert(package)

        return packages