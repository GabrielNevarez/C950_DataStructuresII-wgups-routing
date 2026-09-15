from Location import Location


class LocationLoader:

    @staticmethod
    def load():
        locations = [
            Location(0, "HUB"),
            Location(1, "1060 Dalton Ave S"),
            Location(2, "1330 2100 S"),
            Location(3, "1488 4800 S"),
            Location(4, "177 W Price Ave"),
            Location(5, "2010 W 500 S"),
            Location(6, "2300 Parkway Blvd")
        ]

        return locations