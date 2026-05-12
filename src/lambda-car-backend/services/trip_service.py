from uuid import UUID, uuid4

from ..domain.trip import Trip
from ..domain.car import Car
from ..domain.refueling import Refueling
from ..domain.commit import Commit

from ..repositories.car_repository import CarRepository
from ..repositories.commit_repository import CommitRepository
from ..repositories.trip_repository import TripRepository
from ..repositories.user_repository import UserRepository

from ..constants import Constants
from ..domain.enum.commit_status import CommitStatus
from ..domain.enum.trip_status import TripStatus
from ..domain.enum.car_status import CarStatus

from ..commands.trip_commands import (
    OpenTripCommand,
    CloseTripCommand,
    UpdateTripCommand,
    DeleteTripCommand,
    GetCommitTripCommand,
)

from ..domain.enum.car_status import CarStatus

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
    
    def _get_trip_or_raise(self, trip_id: UUID) -> Trip:
        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)
        return trip
    
    def _get_car_or_raise(self, car_id: UUID) -> Car:
        car = self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)
        return car
    
    def _get_user_or_raise(self, user_id: UUID):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(Constants.USER_NOT_FOUND)
        return user
    
    def _get_commit_or_raise(self, commit_id: UUID) -> Commit:
        commit = self.commit_repository.get_by_id(commit_id)
        if not commit:
            raise ValueError(Constants.COMMIT_NOT_FOUND)
        return commit
    
    def _check_user_owns_trip_or_raise(self, trip: Trip, user_id: UUID):
        if str(trip.user_id) != str(user_id):
            raise ValueError(Constants.USER_NOT_OWNER)
    
    def _is_active_trip(self, car_id: UUID) -> Trip | None:
        active_trip = self.trip_repository.get_active_trip_by_car_id(car_id)
        if active_trip:
            return True
        return False
    
    def _check_active_trip_or_raise(self, car_id: UUID):
        if self._is_active_trip(car_id):
            raise ValueError(Constants.ACTIVE_TRIP_EXISTS)
    
    def _check_not_active_trip_or_raise(self, car_id: UUID):
        if not self._is_active_trip(car_id):
            raise ValueError(Constants.NO_ACTIVE_TRIP)

    def open_trip(self,cmd: OpenTripCommand ) -> Trip:
        car = self._get_car_or_raise(cmd.car_id)
        user = self._get_user_or_raise(cmd.user_id)
        self._check_active_trip_or_raise(cmd.car_id)
        commit = self._get_commit_or_raise(cmd.commit_id)
        trip = Trip(
            id=uuid4(),
            car_id=cmd.car_id,
            user_id=cmd.user_id,
            start_position=cmd.start_position,
            start_date=cmd.start_date,
            start_km=cmd.start_km
        )
        commit.trip_id = trip.id
        commit.status = CommitStatus.IN_PROGRESS
        car.status = CarStatus.IN_USE
        self.car_repository.save(car)
        self.trip_repository.save(trip)
        return trip
    
    def close_trip(self, cmd: CloseTripCommand) -> Trip:
        user = self._get_user_or_raise(cmd.user_id)
        trip = self._get_trip_or_raise(cmd.trip_id)
        self._check_user_owns_trip_or_raise(trip=trip, user_id=cmd.user_id)
        self._check_not_active_trip_or_raise(trip.car_id)
        car = self._get_car_or_raise(trip.car_id)
        trip.close_trip(cmd.end_position, cmd.end_date, cmd.end_km)
        car.status = CarStatus.FREE
        self.car_repository.save(car)
        self.trip_repository.save(trip)
        return trip
    
    def get_trip(self, trip_id: UUID) -> Trip:
        trip = self._get_trip_or_raise(trip_id)
        return trip
    
    def update_trip(
            self,
            cmd: UpdateTripCommand
    ) -> Trip:
        trip = self.get_trip(cmd.trip_id)
        if str(trip.user_id) != cmd.user_id:
            raise ValueError(Constants.USER_NOT_OWNER)
        car = self._get_car_or_raise(trip.car_id)
        if trip.car_id != cmd.car_id:
            self._check_active_trip_or_raise(cmd.car_id)
            car.status = CarStatus.FREE
            self.car_repository.save(car)
            car = self._get_car_or_raise(cmd.car_id)
            car.status = CarStatus.IN_USE
            self.car_repository.save(car)
        trip.car_id = cmd.car_id
        trip.start_position = cmd.start_position
        trip.end_position = cmd.end_position
        trip.start_date = cmd.start_date
        trip.end_date = cmd.end_date
        trip.start_km = cmd.start_km
        trip.end_km = cmd.end_km
        self.trip_repository.save(trip)
        return trip
    
    def delete_trip(self, cmd: DeleteTripCommand) -> None:
        user = self._get_user_or_raise(cmd.user_id)
        car = self._get_car_or_raise(cmd.user_id)
        trip = self.get_trip(cmd.trip_id)
        self._check_user_owns_trip_or_raise(trip=trip, user_id=cmd.user_id)
        car.status = CarStatus.FREE
        self.car_repository.save(car)
        self.trip_repository.delete(cmd.trip_id)
    
    def get_car_for_trip(self, trip_id: UUID) -> Car:
        trip = self._get_trip_or_raise(trip_id)
        car = self.car_repository.get_by_id(trip.car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)
        return car
    
    def get_commit_for_trip(self, cmd: GetCommitTripCommand) -> Commit | None:
        user = self._get_user_or_raise(cmd.user_id)
        trip = self._get_trip_or_raise(cmd.trip_id)
        self._check_user_owns_trip_or_raise(trip=trip, user_id=cmd.user_id)
        if not trip.commit_id:
            return None
        commit = self._get_commit_or_raise(trip.commit_id)
        return commit
    
    def get_trips_for_user(self, user_id: UUID) -> list[Trip]:
        user = self._get_user_or_raise(user_id)
        return self.trip_repository.list_by_user_id(user_id)