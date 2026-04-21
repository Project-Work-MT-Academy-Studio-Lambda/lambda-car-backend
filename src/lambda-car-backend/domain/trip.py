from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timedelta

@dataclass
class Trip:
    id: UUID
    car_id: UUID
    user_id: UUID
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
    
    @property
    def is_active(self) -> bool:
        return datetime.now() < self.end_date if self.end_date else True