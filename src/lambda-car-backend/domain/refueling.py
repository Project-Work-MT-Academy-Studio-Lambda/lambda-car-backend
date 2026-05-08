from dataclasses import dataclass
from uuid import UUID
from ..constants import Constants
from datetime import datetime
from decimal import Decimal

@dataclass
class Refueling:
    id: UUID
    date: datetime
    car_id: UUID
    liter_price: Decimal
    liters: Decimal
    receipt_photo: str
    card_number: str | None = None

    def __post_init__(self):
        if self.liter_price < 0:
            raise ValueError(Constants.LITER_PRICE_CANNOT_BE_NEGATIVE)
        if self.liters < 0:
            raise ValueError(Constants.LITERS_CANNOT_BE_NEGATIVE)
        if not self.receipt_photo:
            raise ValueError(Constants.RECEIPT_PHOTO_CANNOT_BE_EMPTY)
        if self.card_number is not None and not self.card_number.strip():
            raise ValueError(Constants.FUEL_CARD_CANNOT_BE_EMPTY)
    
    @property
    def total_cost(self) -> float:
        return self.liter_price * self.liters