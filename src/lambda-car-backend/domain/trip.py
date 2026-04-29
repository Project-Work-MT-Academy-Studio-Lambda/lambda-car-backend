from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timedelta
from constants import Constants
from .enum.trip_status import TripStatus

@dataclass
class Trip:
    id: UUID
    car_id: UUID
    user_id: UUID
    start_position: str
    start_date: datetime
    start_km: int
    status: TripStatus = TripStatus.ACTIVE
    end_position: str | None = None
    end_date: datetime | None = None
    end_km: int | None = None

    def __post_init__(self):
        now = datetime.now()
        TOLLERANCE = timedelta(minutes=5)
        if not self.start_position:
            raise ValueError(Constants.START_POSITION_CANNOT_BE_EMPTY)
        if self.start_date > now + TOLLERANCE:
            raise ValueError(Constants.START_DATE_CANNOT_BE_IN_THE_FUTURE)
        if self.start_km < 0:
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
    
    def close_trip(self, end_position: str, end_date: datetime, end_km: int):
        if not end_position:
            raise ValueError(Constants.END_POSITION_CANNOT_BE_EMPTY)
        now = datetime.now()
        TOLLERANCE = timedelta(minutes=5)
        if end_date > now + TOLLERANCE:
            raise ValueError(Constants.END_DATE_CANNOT_BE_IN_THE_FUTURE)
        if end_date < self.start_date:
            raise ValueError(Constants.END_DATE_CANNOT_BE_BEFORE_START_DATE)
        if end_km < 0:
            raise ValueError(Constants.END_KM_CANNOT_BE_NEGATIVE)
        if end_km < self.start_km:
            raise ValueError(Constants.END_KM_CANNOT_BE_LESS_THAN_START_KM)
        
        self.status = TripStatus.CLOSED
        self.end_position = end_position
        self.end_date = end_date
        self.end_km = end_km