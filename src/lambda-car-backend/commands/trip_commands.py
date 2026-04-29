from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class OpenTripCommand:
    user_id: UUID
    car_id: UUID
    commit_id: UUID
    start_position: str
    start_date: datetime
    start_km: int

@dataclass
class CloseTripCommand:
    trip_id: UUID
    end_position: str
    end_date: datetime
    end_km: int

@dataclass
class UpdateTripCommand:
    trip_id: UUID
    user_id: UUID
    car_id: UUID
    start_position: str
    end_position: str
    start_date: datetime
    end_date: datetime
    start_km: int
    end_km: int