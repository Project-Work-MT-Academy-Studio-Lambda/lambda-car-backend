from dataclasses import dataclass
from uuid import UUID
from constants import Constants

@dataclass
class Refueling:
    id: UUID
    car_id: UUID
    liter_price: float
    liters: int
    receipt_photo: str
    cartd_number: str | None = None

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