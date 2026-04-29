from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class CreateRefuelingCommand:
    car_id: UUID
    card_number: str
    liter_price: float
    liters: int
    receipt_photo: str
    date: datetime

@dataclass
class UpdateRefuelingCommand:
    refueling_id: UUID
    car_id: UUID
    card_number: str
    liter_price: float
    liters: int
    receipt_photo: str
    date: datetime