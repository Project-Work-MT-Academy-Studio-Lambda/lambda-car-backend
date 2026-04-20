from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timedelta

@dataclass
class User:
    id: UUID
    name: str
    email: str
    hashed_password: str

@dataclass
class Trip:
    id: UUID
    user: User
    car: 'Car'
    commit: 'Commit'
    refueling: 'Refueling' | None
    start_position: str | None
    end_position: str | None
    start_date: datetime | None
    end_date: datetime | None
    start_km: int | None
    end_km: int | None

    def __post_init__(self):
        if not self.start_position:
            raise ValueError("Start position cannot be empty")
        if not self.end_position:
            raise ValueError("End position cannot be empty")
        if self.start_date and abs(datetime.now() - self.start_date) <= timedelta(minutes=5):
            raise ValueError("Start date cannot be in the future")
        if self.end_date and abs(datetime.now() - self.end_date) <= timedelta(minutes=5):
            raise ValueError("End date cannot be in the future")
        if self.start_km and self.start_km < 0:
            raise ValueError("Start km cannot be negative")

    @property
    def distance(self) -> int:
        return self.end_km - self.start_km
    
    @property
    def duration(self) -> int:
        return int((self.end_date - self.start_date).total_seconds() / 60)

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

@dataclass
class Car:
    plate: str
    km: int
    fuel_level: int

    def __post_init__(self):
        if not self.plate:
            raise ValueError("Plate cannot be empty")
        if self.km < 0:
            raise ValueError("Km cannot be negative")
        if self.fuel_level < 0:
            raise ValueError("Fuel level cannot be negative")

@dataclass
class Commit:
    id: UUID
    code: str
    description: str

    def __post_init__(self):
        if not self.code:
            raise ValueError("Code cannot be empty")
        if not self.description:
            raise ValueError("Description cannot be empty")