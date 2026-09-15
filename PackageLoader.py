import csv
import re

from Package import Package
from Packages import Packages


class PackageLoader:
    """
    Loads package data from the package CSV file.

    PackageLoader converts each CSV row into a Package object,
    matches the package address to a location ID, formats delivery
    deadlines, and inserts the package into the custom hash table.
    """

    @staticmethod
    def load(package_file, locations):
        """
        Loads all packages from the package CSV file.

        @param package_file: Path to the package CSV file.
        @param locations: List of Location objects used to match
                          package addresses to location IDs.
        @return: Packages hash table containing all Package objects.
        """

        package_data = []

        # Open the package file and read each package row.
        with open(
            package_file,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                package_id = int(
                    row["Package\nID"]
                )

                address = row["Address"].strip()
                city = row["City "].strip()
                state = row["State"].strip()
                zip_code = row["Zip"].strip()

                # Convert Excel-style deadline values such as
                # 0.375 and 0.4375 into readable delivery times.
                deadline = PackageLoader.format_deadline(
                    row["Delivery\nDeadline"]
                )

                weight = int(
                    row["Weight\nKILO"]
                )

                # Special notes are stored exactly as provided.
                # Constraint logic is handled separately and
                # hard-coded in the routing/truck logic.
                special_notes = row[
                    "page 1 of 1PageSpecial Notes"
                ].strip()

                # Match the package address to the numeric
                # location ID used by the distance graph.
                location_id = (
                    PackageLoader.find_location_id(
                        address,
                        locations
                    )
                )

                if location_id is None:
                    raise ValueError(
                        f"Location not found for package "
                        f"{package_id}: {address}"
                    )

                package = Package(
                    package_id,
                    location_id,
                    address,
                    city,
                    state,
                    zip_code,
                    deadline,
                    weight,
                    special_notes
                )

                package_data.append(
                    package
                )

        # Create the custom hash table after all
        # package records have been loaded.
        packages = Packages(
            len(package_data) * 2
        )

        # Package ID is used as the hash table key.
        for package in package_data:
            packages.insert(
                package.package_id,
                package
            )

        return packages

    @staticmethod
    def format_deadline(deadline):
        """
        Converts a package deadline into a readable time.

        @param deadline: Deadline value from the CSV file.
        @return: Formatted deadline such as "9:00 AM",
                 "10:30 AM", or "EOD".
        """

        deadline = deadline.strip()

        if deadline == "EOD":
            return "EOD"

        try:
            # Excel stores times as fractions of a 24-hour day.
            excel_time = float(
                deadline
            )

            total_minutes = round(
                excel_time * 24 * 60
            )

            hours = (
                total_minutes // 60
            )

            minutes = (
                total_minutes % 60
            )

            period = "AM"

            if hours >= 12:
                period = "PM"

            display_hour = (
                hours % 12
            )

            if display_hour == 0:
                display_hour = 12

            return (
                f"{display_hour}:"
                f"{minutes:02d} "
                f"{period}"
            )

        except ValueError:
            # If the value is already readable text,
            # return it without modification.
            return deadline

    @staticmethod
    def normalize_address(address):
        """
        Normalizes an address before comparing package
        and location records.

        @param address: Address string to normalize.
        @return: Normalized lowercase address string.
        """

        address = address.lower().strip()

        # Normalize common street-direction differences
        # between the package and location source files.
        replacements = {
            " south ": " s ",
            " north ": " n ",
            " east ": " e ",
            " west ": " w ",
            " street ": " st ",
            " avenue ": " ave ",
            " boulevard ": " blvd ",
            " road ": " rd ",
            " drive ": " dr "
        }

        address = f" {address} "

        for old, new in replacements.items():
            address = address.replace(
                old,
                new
            )

        # Remove duplicate whitespace after replacements.
        address = re.sub(
            r"\s+",
            " ",
            address
        ).strip()

        return address

    @staticmethod
    def find_location_id(address, locations):
        """
        Finds the location ID that matches a package address.

        @param address: Package delivery address.
        @param locations: List of Location objects.
        @return: Matching location ID, or None if no match exists.
        """

        package_address = (
            PackageLoader.normalize_address(
                address
            )
        )

        for location in locations:
            location_address = (
                PackageLoader.normalize_address(
                    location.address
                )
            )

            if package_address == location_address:
                return location.location_id

        return None