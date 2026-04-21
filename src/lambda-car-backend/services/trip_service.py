from uuid import UUID, uuid4
from datetime import datetime

from domain.trip import Trip
from domain.car import Car
from domain.refueling import Refueling
from domain.commit import Commit

from repositories.car_repository import CarRepository
from repositories.commit_repository import CommitRepository
from repositories.trip_repository import TripRepository
from repositories.user_repository import UserRepository

from constants import Constants

class TripService:
    def __init__(
        self,
        trip_repository: TripRepository,
        user_repository: UserRepository,
        car_repository: CarRepository,
        commit_repository: CommitRepository,
    ):
        self.trip_repository = trip_repository
        self.user_repository = user_repository
        self.car_repository = car_repository
        self.commit_repository = commit_repository
            
    def create_trip(self, 
                    user_id: UUID,
                    car_id: UUID,
                    start_position: str,
                    end_position: str,
                    start_date: datetime,
                    end_date: datetime,
                    start_km: int,
                    end_km: int
    ) -> Trip:
        car = self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(Constants.USER_NOT_FOUND)
        trip = Trip(
            id=uuid4(),
            car_id=car_id,
            user_id=user_id,
            start_position=start_position,
            end_position=end_position,
            start_date=start_date,
            end_date=end_date,
            start_km=start_km,
            end_km=end_km
        )
        self.trip_repository.save(trip)
        return trip
    
    def get_trip(self, trip_id: UUID) -> Trip:
        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)
        return trip
    
    def get_trips_for_user(self, user_id: UUID) -> list[Trip]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(Constants.USER_NOT_FOUND)
        return self.trip_repository.list_by_user_id(user_id)
    
    def get_trips_for_car(self, car_id: UUID) -> list[Trip]:
        car = self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)
        return self.trip_repository.list_by_car_id(car_id)
    
    def get_trips_for_commit(self, commit_id: UUID) -> list[Trip]:
        commit = self.commit_repository.get_by_id(commit_id)
        if not commit:
            raise ValueError(Constants.COMMIT_NOT_FOUND)
        return self.trip_repository.list_by_commit_id(commit_id)
    
    def update_trip(
            self,
            trip_id: UUID,
            user_id: UUID,
            car_id: UUID,
            start_position: str,
            end_position: str,
            start_date: datetime,
            end_date: datetime,
            start_km: int,
            end_km: int
    ) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.user_id != user_id:
            raise ValueError(Constants.USER_NOT_OWNER)
        car = self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)
        trip.car_id = car_id
        trip.start_position = start_position
        trip.end_position = end_position
        trip.start_date = start_date
        trip.end_date = end_date
        trip.start_km = start_km
        trip.end_km = end_km
        self.trip_repository.save(trip)
        return trip
    
    def delete_trip(self, trip_id: UUID, user_id: UUID) -> None:
        trip = self.get_trip(trip_id)
        if trip.user_id != user_id:
            raise ValueError(Constants.USER_NOT_OWNER)
        self.trip_repository.delete(trip_id)
    
    def get_car_for_trip(self, trip_id: UUID) -> Car:
        trip = self.get_trip(trip_id)
        car = self.car_repository.get_by_id(trip.car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)
        return car
    
    def get_commit_for_trip(self, trip_id: UUID) -> Commit | None:
        trip = self.get_trip(trip_id)
        if not trip.commit_id:
            return None
        commit = self.commit_repository.get_by_id(trip.commit_id)
        if not commit:
            raise ValueError(Constants.COMMIT_NOT_FOUND)
        return commit
    
    def get_refuelings_for_trip(self, trip_id: UUID) -> list[Refueling]:
        trip = self.get_trip(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)
        return self.refueling_repository.list_by_trip_id(trip_id)