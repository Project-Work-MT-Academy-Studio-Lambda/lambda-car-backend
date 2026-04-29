from uuid import UUID, uuid4

from domain.refueling import Refueling
from repositories.refueling_repository import RefuelingRepository
from repositories.car_repository import CarRepository
from constants import Constants

from commands.refueling_commands import (
    CreateRefuelingCommand,
    UpdateRefuelingCommand
)


class RefuelingService:
    def __init__(
        self,
        refueling_repository: RefuelingRepository,
        car_repository: CarRepository,
    ):
        self.refueling_repository = refueling_repository
        self.car_repository = car_repository

    def _get_refueling_or_raise(self, refueling_id: UUID) -> Refueling:
        refueling = self.refueling_repository.get_by_id(refueling_id)
        if not refueling:
            raise ValueError(Constants.REFUELING_NOT_FOUND)
        return refueling

    def create_refueling(
        self,
        cmd: CreateRefuelingCommand
    ) -> Refueling:
        car = self.car_repository.get_by_id(cmd.car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)

        refueling = Refueling(
            id=uuid4(),
            car_id=cmd.car_id,
            liters=cmd.liters,
            price=cmd.liter_price,
            date=cmd.date,
        )

        self.refueling_repository.save(refueling)
        return refueling

    def get_refueling(self, refueling_id: UUID) -> Refueling:
        refueling = self._get_refueling_or_raise(refueling_id)
        return refueling

    def get_refuelings_for_car(self, car_id: UUID) -> list[Refueling]:
        car = self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)

        return self.refueling_repository.list_by_car_id(car_id)

    def update_refueling(
        self,
        cmd: UpdateRefuelingCommand
    ) -> Refueling:
        refueling = self._get_refueling_or_raise(cmd.refueling_id)

        car = self.car_repository.get_by_id(cmd.car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)

        refueling.car_id = cmd.car_id
        refueling.liters = cmd.liters
        refueling.price = cmd.liter_price
        refueling.date = cmd.date

        self.refueling_repository.save(refueling)
        return refueling

    def delete_refueling(self, refueling_id: UUID) -> None:
        refueling = self._get_refueling_or_raise(refueling_id)
        self.refueling_repository.delete(refueling_id)