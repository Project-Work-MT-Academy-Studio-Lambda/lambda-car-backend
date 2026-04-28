from dataclasses import dataclass
from uuid import UUID

@dataclass
class CreateCarCommand:
    plate: str
    km_total: int
    km_servicing: int
    km_wheels: int

@dataclass
class UpdateCarCommand:
    car_id: UUID
    plate: str
    km_total: int
    km_servicing: int
    km_wheels: int