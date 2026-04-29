from dataclasses import dataclass
from uuid import UUID

@dataclass
class CreateCarCommand:
    plate: str
    model: str
    km_total: int
    km_servicing: int
    km_wheels: int
    fuel_type: str
    fuel_level: int | None = None
    fuel_card: str | None = None

@dataclass
class UpdateCarCommand:
    car_id: UUID
    plate: str
    model: str
    km_total: int
    km_servicing: int
    km_wheels: int
    fuel_type: str
    fuel_level: int | None = None
    fuel_card: str | None = None