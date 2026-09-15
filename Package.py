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
        address,
        city,
        state,
        zip_code,
        deadline,
        weight,
        special_notes=""
    ):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes

        self.status = PackageStatus.AT_HUB
        self.delivery_time = None
        self.truck_id = None