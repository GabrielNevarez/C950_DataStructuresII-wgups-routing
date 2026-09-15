from datetime import datetime
from enum import Enum


class PackageStatus(Enum):
    DELAYED = "Delayed"
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"


class Package:
    def __init__(
        self,
        package_id,
        location_id,
        address,
        city,
        state,
        zip_code,
        deadline,
        weight,
        special_notes=""
    ):
        self.package_id = package_id
        self.location_id = location_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes

        self.status = PackageStatus.AT_HUB
        self.truck_id = None

        self.departure_time = None
        self.delivery_time = None

    def get_status_at(self, query_time):
        if self.delivery_time is not None and query_time >= self.delivery_time:
            return PackageStatus.DELIVERED

        if self.departure_time is not None and query_time >= self.departure_time:
            return PackageStatus.EN_ROUTE

        return PackageStatus.AT_HUB