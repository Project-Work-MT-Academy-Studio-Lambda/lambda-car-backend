from dataclasses import dataclass
from uuid import UUID

@dataclass
class Car:
    id: UUID
    trip_id: UUID
    plate: str
    km: int
    fuel_level: int

    def __post_init__(self):
        if not self.plate:
            raise ValueError("Plate cannot be empty")
        if self.km < 0:
            raise ValueError("Km cannot be negative")
        if self.fuel_level < 0:
            raise ValueError("Fuel level cannot be negative")