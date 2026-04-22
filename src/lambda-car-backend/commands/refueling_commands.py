from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class CreateRefuelingCommand:
    trip_id: UUID
    cart_number: str
    liter_price: float
    liters: int
    receipt_photo: str
    date: datetime

@dataclass
class UpdateRefuelingCommand:
    refueling_id: UUID
    trip_id: UUID
    cart_number: str
    liter_price: float
    liters: int
    receipt_photo: str
    date: datetime