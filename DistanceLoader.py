import csv

from DistanceGraph import DistanceGraph


class DistanceLoader:
    """
    Loads distance data from the Distances.csv file.

    Each CSV row contains two location IDs and the mileage
    between them. The values are stored in the DistanceGraph.
    """

    @staticmethod
    def load(file_path, locations):
        """
        Loads distance data into a DistanceGraph.

        @param file_path: Path to the distance CSV file.
        @param locations: List of Location objects used to size
                          and initialize the distance graph.
        @return: Fully populated DistanceGraph object.
        """

        graph = DistanceGraph(
            locations
        )

        # Open the CSV file and load each
        # location-to-location distance.
        with open(
            file_path,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(
                file
            )

            for row in reader:
                location1_id = int(
                    row["location1_id"]
                )

                location2_id = int(
                    row["location2_id"]
                )

                distance = float(
                    row["distance"]
                )

                # DistanceGraph stores the value
                # in both directions because the
                # WGUPS distance table is symmetric.
                graph.set_distance(
                    location1_id,
                    location2_id,
                    distance
                )

        return graph