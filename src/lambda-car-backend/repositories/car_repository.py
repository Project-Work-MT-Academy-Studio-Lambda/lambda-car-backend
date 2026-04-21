from typing import Protocol
from uuid import UUID
from domain.car import Car

class CarRepository(Protocol):
    def get_by_id(self, car_id: UUID) -> Car | None:
        ...

    def save(self, car: Car) -> None:
        ...

    def delete(self, car_id: UUID) -> None:
        ...
    
    def get_by_plate(self, plate: str) -> Car | None:
        ...