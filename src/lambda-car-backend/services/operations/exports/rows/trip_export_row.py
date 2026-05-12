from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TripExportRow:
    user_email: str
    car_plate: str
    commits: str
    start_position: str
    end_position: str | None
    start_date: datetime
    end_date: datetime | None
    start_km: int
    end_km: int | None
    distance: int | None
    duration_minutes: int | None
    status: str