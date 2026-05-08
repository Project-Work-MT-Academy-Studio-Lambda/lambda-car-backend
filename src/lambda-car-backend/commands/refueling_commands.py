from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from decimal import Decimal

@dataclass
class CreateRefuelingCommand:
    car_id: UUID
    card_number: str
    liter_price: Decimal
    liters: int
    receipt_filename: str
    receipt_content: bytes
    receipt_content_type: str
    date: datetime

@dataclass
class UpdateRefuelingCommand:
    refueling_id: UUID
    car_id: UUID
    card_number: str
    liter_price: Decimal
    liters: int
    date: datetime