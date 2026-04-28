from uuid import UUID
from pydantic import BaseModel
from domain.car import Car


class CreateCarRequest(BaseModel):
    plate: str
    model: str | None = None
    km_total: int
    km_servicing: int
    km_wheels: int


class UpdateCarRequest(BaseModel):
    plate: str
    model: str | None = None
    km_total: int | None = None
    km_servicing: int | None = None
    km_wheels: int | None = None


class CarResponse(BaseModel):
    id: UUID
    plate: str
    model: str | None = None
    km_total: int | None = None
    km_servicing: int | None = None
    km_wheels: int | None = None

    @classmethod
    def from_domain(cls, car: Car) -> "CarResponse":
        return cls(
            id=car.id,
            plate=car.plate,
            model=car.model,
            km_total=car.km_total,
            km_servicing=car.km_servicing,
            km_wheels=car.km_wheels,
        )