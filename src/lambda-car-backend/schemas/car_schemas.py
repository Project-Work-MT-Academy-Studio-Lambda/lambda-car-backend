from uuid import UUID
from pydantic import BaseModel, Field

from ..domain.car import Car

class MileageSchema(BaseModel):
    km_total: int = Field(..., ge=0)
    km_servicing: int = Field(..., ge=0)
    km_wheels: int = Field(..., ge=0)

class FuelInfoSchema(BaseModel):
    type: str = Field(..., min_length=1)
    level: int | None = Field(default=None, ge=0, le=100)
    card: str | None = None


class CreateCarRequest(BaseModel):
    plate: str = Field(..., min_length=1)
    model: str | None = None
    mileage: MileageSchema
    fuel_info: FuelInfoSchema


class UpdateCarRequest(BaseModel):
    plate: str = Field(..., min_length=1)
    model: str | None = None
    mileage: MileageSchema
    fuel_info: FuelInfoSchema


class CarResponse(BaseModel):
    id: UUID
    plate: str
    model: str | None
    mileage: MileageSchema
    fuel_info: FuelInfoSchema

    @classmethod
    def from_domain(cls, car: Car) -> "CarResponse":
        return cls(
            id=car.id,
            plate=car.plate,
            model=car.model,
            mileage=MileageSchema(
                km_total=car.mileage.km_total,
                km_servicing=car.mileage.km_servicing,
                km_wheels=car.mileage.km_wheels,
            ),
            fuel_info=FuelInfoSchema(
                type=car.fuel_info.type,
                level=car.fuel_info.level,
                card=car.fuel_info.card,
            ),
        )