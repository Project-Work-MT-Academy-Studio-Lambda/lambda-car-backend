from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from domain.refueling import Refueling


class CreateRefuelingRequest(BaseModel):
    car_id: UUID
    liters: float = Field(..., gt=0)
    liter_price: float = Field(..., ge=0)
    date: datetime
    receipt_photo: str
    card_number: str | None = None
    


class UpdateRefuelingRequest(BaseModel):
    liters: float = Field(..., gt=0)
    liter_price: float = Field(..., ge=0)
    date: datetime
    receipt_photo: str
    card_number: str | None = None

class RefuelingResponse(BaseModel):
    id: UUID
    car_id: UUID
    liters: float
    liter_price: float
    date: datetime
    receipt_photo: str
    card_number: str | None = None

    @classmethod
    def from_domain(cls, refueling: Refueling) -> "RefuelingResponse":
        return cls(
            id=refueling.id,
            car_id=refueling.car_id,
            liters=refueling.liters,
            liter_price=refueling.liter_price,
            date=refueling.date,
            receipt_photo=refueling.receipt_photo,
            card_number=refueling.card_number,
        )