from dataclasses import dataclass
from uuid import UUID

@dataclass
class Refueling:
    id: UUID
    cart_number: str
    liter_price: float
    liters: int
    receipt_photo: str

    def __post_init__(self):
        if not self.cart_number:
            raise ValueError("Cart number cannot be empty")
        if self.liter_price < 0:
            raise ValueError("Liter price cannot be negative")
        if self.liters < 0:
            raise ValueError("Liters cannot be negative")
        if not self.receipt_photo:
            raise ValueError("Receipt photo cannot be empty")