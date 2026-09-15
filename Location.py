class Location:
    def __init__(self, location_id, address):
        self.location_id = location_id
        self.address = address

    def __str__(self):
        return f"{self.location_id}: {self.address}"