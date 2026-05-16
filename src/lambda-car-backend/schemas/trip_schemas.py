from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from ..domain.car import Car
from ..domain.trip import Trip
from ..domain.enum.trip_status import TripStatus

class OpenTripRequest(BaseModel):
    car_id: UUID
    commit_id: UUID
    start_position: str
    start_date: datetime
    start_km: int


class UpdateTripRequest(BaseModel):
    car_id: UUID
    start_position: str
    start_date: datetime
    start_km: int
    end_position: str | None = None
    end_date: datetime | None = None
    end_km: int | None = None


class CloseTripRequest(BaseModel):
    end_position: str
    end_date: datetime
    end_km: int


class TripCarResponse(BaseModel):
    id: UUID
    plate: str
    model: str | None = None
    status: str | None = None

    @classmethod
    def from_domain(cls, car: Car) -> "TripCarResponse":
        return cls(
            id=car.id,
            plate=car.plate,
            model=car.model,
            status=car.status.value if hasattr(car.status, "value") else car.status,
        )


class TripResponse(BaseModel):
    id: UUID
    car_id: UUID
    car: TripCarResponse | None = None
    commit_id: UUID | None = None
    user_id: UUID
    start_position: str
    start_date: datetime
    start_km: int
    status: TripStatus
    end_position: str | None = None
    end_date: datetime | None = None
    end_km: int | None = None
    distance: int | None = None
    duration: int | None = None

    @classmethod
    def from_domain(cls, trip: Trip, car: Car | None = None) -> "TripResponse":
        return cls(
            id=trip.id,
            car_id=trip.car_id,
            car=TripCarResponse.from_domain(car) if car else None,
            commit_id=trip.commit_id,
            user_id=trip.user_id,
            start_position=trip.start_position,
            start_date=trip.start_date,
            start_km=trip.start_km,
            end_position=trip.end_position,
            end_date=trip.end_date,
            end_km=trip.end_km,
            distance=trip.distance,
            duration=trip.duration,
            status=trip.status
        )
