from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RefuelingExportRow:
    car_plate: str
    card_number: str
    liter_price: float
    liters: int
    total_price: float
    date: datetime
    receipt_photo: str