from uuid import UUID, uuid4

from ..domain.refueling import Refueling
from ..repositories.refueling_repository import RefuelingRepository
from ..repositories.car_repository import CarRepository
from ..constants import Constants

from ..commands.refueling_commands import (
    CreateRefuelingCommand,
    UpdateRefuelingCommand
)

from ..storage.receipt_photo_storage import ReceiptPhotoStorage

from ..logger import get_logger


class RefuelingService:
    def __init__(
        self,
        refueling_repository: RefuelingRepository,
        car_repository: CarRepository,
        receipt_photo_storage: ReceiptPhotoStorage
    ):
        self.refueling_repository = refueling_repository
        self.car_repository = car_repository
        self.receipt_photo_storage = receipt_photo_storage
        self.logger = get_logger(__name__)

    def _get_refueling_or_raise(self, refueling_id: UUID, user_id: UUID, user_role: str) -> Refueling:
        refueling = self.refueling_repository.get_by_id(refueling_id, user_id, user_role)
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
        self.logger.debug(f"Creating refueling for car_id: {cmd.car_id}, liters: {cmd.liters}, liter_price: {cmd.liter_price}, date: {cmd.date}")
        self.logger.debug(f"Received command price type: {type(cmd.liter_price)}, liters type: {type(cmd.liters)}")
        refueling_id = uuid4()

        receipt_photo = self.receipt_photo_storage.save_receipt_photo(
            refueling_id=refueling_id,
            filename=cmd.receipt_filename,
            content=cmd.receipt_content,
            content_type=cmd.receipt_content_type
        )

        refueling = Refueling(
            id=refueling_id,
            car_id=cmd.car_id,
            liters=cmd.liters,
            liter_price=cmd.liter_price,
            date=cmd.date,
            receipt_photo=receipt_photo,
            card_number=cmd.card_number
        )
        self.logger.debug(f"Created refueling: {refueling}")
        self.logger.debug(f"liters type: {type(cmd.liters)}, liter_price type: {type(cmd.liter_price)}")
        self.refueling_repository.save(refueling)
        return refueling

    def get_refueling(self, refueling_id: UUID, user_id: UUID, user_role: str) -> Refueling:
        refueling = self._get_refueling_or_raise(refueling_id, user_id, user_role)
        return refueling

    def get_refuelings_for_car(self, car_id: UUID, user_id: UUID, user_role: str) -> list[Refueling]:
        car = self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)

        return self.refueling_repository.list_by_car_id(car_id, user_id, user_role)

    def update_refueling(
        self,
        cmd: UpdateRefuelingCommand
    ) -> Refueling:
        
        refueling = self._get_refueling_or_raise(cmd.refueling_id, cmd.user_id, cmd.user_role)

        car = self.car_repository.get_by_id(cmd.car_id)
        if not car:
            raise ValueError(Constants.CAR_NOT_FOUND)

        refueling.liters = cmd.liters
        refueling.liter_price = cmd.liter_price
        refueling.date = cmd.date

        self.refueling_repository.save(refueling)
        return refueling

    def delete_refueling(self, refueling_id: UUID, user_id: UUID, user_role: str) -> None:
        refueling = self._get_refueling_or_raise(refueling_id, user_id, user_role)
        self.refueling_repository.delete(refueling_id)