from enum import Enum

class TripStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"