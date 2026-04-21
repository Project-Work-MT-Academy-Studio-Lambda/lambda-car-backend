from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timedelta
from constants import Constants

@dataclass
class Trip:
    id: UUID
    car_id: UUID
    user_id: UUID
    start_position: str
    end_position: str | None = None
    start_date: datetime
    end_date: datetime | None = None
    start_km: int
    end_km: int | None = None

    def __post_init__(self):
        now = datetime.now()
        TOLLERANCE = timedelta(minutes=5)
        if not self.start_position:
            raise ValueError(Constants.START_POSITION_CANNOT_BE_EMPTY)
        if not self.end_position:
            raise ValueError(Constants.END_POSITION_CANNOT_BE_EMPTY)
        if self.start_date and self.start_date > now + TOLLERANCE:
            raise ValueError(Constants.START_DATE_CANNOT_BE_IN_THE_FUTURE)
        if self.end_date and self.start_date and self.end_date > self.start_date + TOLLERANCE:
            raise ValueError(Constants.END_DATE_CANNOT_BE_IN_THE_FUTURE)
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError(Constants.END_DATE_CANNOT_BE_BEFORE_START_DATE)
        if self.start_km and self.start_km < 0:
            raise ValueError(Constants.START_KM_CANNOT_BE_NEGATIVE)

    @property
    def distance(self) -> int | None:
        if self.start_km is None or self.end_km is None:
            return None
        return self.end_km - self.start_km
    
    @property
    def duration(self) -> int | None:
        if self.start_date is None or self.end_date is None:
            return None
        return int((self.end_date - self.start_date).total_seconds() / 60)
    
    @property
    def is_active(self) -> bool:
        if self.end_date is None:
            return True
        return datetime.now() < self.end_date if self.end_date else True