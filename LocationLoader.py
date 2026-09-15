import csv

from Location import Location


class LocationLoader:
    """
    Loads delivery locations from the Locations.csv file.

    Each row is converted into a Location object and returned
    in a list ordered by location ID.
    """

    @staticmethod
    def load(file_path):
        """
        Loads location data from a CSV file.

        @param file_path: Path to the location CSV file.
        @return: List of Location objects.
        """

        locations = []

        # Open the CSV file and read each location row.
        with open(
            file_path,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                location = Location(
                    int(row["location_id"]),
                    row["address"].strip()
                )

                locations.append(location)

        # Return the complete list so the distance graph
        # can use matching numeric location IDs.
        return locations