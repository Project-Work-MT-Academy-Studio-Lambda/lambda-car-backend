from uuid import UUID, uuid4

from domain.refueling import Refueling
from repositories.refueling_repository import RefuelingRepository
from repositories.trip_repository import TripRepository
from constants import Constants

from commands.refueling_commands import (
    CreateRefuelingCommand,
    UpdateRefuelingCommand
)


class RefuelingService:
    def __init__(
        self,
        refueling_repository: RefuelingRepository,
        trip_repository: TripRepository,
    ):
        self.refueling_repository = refueling_repository
        self.trip_repository = trip_repository
    
    def _get_refueling_or_raise(self, refueling_id: UUID) -> Refueling:
        refueling = self.refueling_repository.get_by_id(refueling_id)
        if not refueling:
            raise ValueError(Constants.REFUELING_NOT_FOUND)
        return refueling

    def create_refueling(
        self,
        cmd: CreateRefuelingCommand
    ) -> Refueling:
        trip = self.trip_repository.get_by_id(cmd.trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        refueling = Refueling(
            id=uuid4(),
            trip_id=cmd.trip_id,
            liters=cmd.liters,
            price=cmd.liter_price,
            date=cmd.date,
        )

        self.refueling_repository.save(refueling)
        return refueling

    def get_refueling(self, refueling_id: UUID) -> Refueling:
        refueling = self._get_refueling_or_raise(refueling_id)
        return refueling

    def get_refuelings_for_trip(self, trip_id: UUID) -> list[Refueling]:
        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        return self.refueling_repository.list_by_trip_id(trip_id)

    def update_refueling(
        self,
        cmd: UpdateRefuelingCommand
    ) -> Refueling:
        refueling = self._get_refueling_or_raise(cmd.refueling_id)

        trip = self.trip_repository.get_by_id(cmd.trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        refueling.trip_id = cmd.trip_id
        refueling.liters = cmd.liters
        refueling.price = cmd.liter_price
        refueling.date = cmd.date

        self.refueling_repository.save(refueling)
        return refueling

    def delete_refueling(self, refueling_id: UUID) -> None:
        refueling = self._get_refueling_or_raise(refueling_id)
        self.refueling_repository.delete(refueling_id)