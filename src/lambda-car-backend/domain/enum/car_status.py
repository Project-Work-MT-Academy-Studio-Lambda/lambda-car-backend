from enum import Enum

class CarStatus(str, Enum):
    FREE = "FREE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"