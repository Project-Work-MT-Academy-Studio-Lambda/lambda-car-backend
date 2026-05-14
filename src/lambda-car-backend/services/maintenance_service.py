from uuid import UUID, uuid4
from decimal import Decimal

from ..commands.maintenance_commands import (
    CreateMaintenanceCommand,
    UpdateMaintenanceCommand,
)
from ..constants import Constants
from ..domain.maintenance import Maintenance
from ..repositories.car_repository import CarRepository
from ..repositories.maintenance_repository import MaintenanceRepository
from ..logger import get_logger


class MaintenanceService:
    def __init__(
        self,
        maintenance_repository: MaintenanceRepository,
        car_repository: CarRepository,
    ):
        self.maintenance_repository = maintenance_repository
        self.car_repository = car_repository
        self.logger = get_logger(__name__)

    def _get_car_or_raise(self, car_id: UUID) -> None:
        car = self.car_repository.get_by_id(car_id)
        if car is None:
            raise ValueError(Constants.CAR_NOT_FOUND)

    def _get_maintenance_or_raise(self, maintenance_id: UUID) -> Maintenance:
        maintenance = self.maintenance_repository.get_by_id(maintenance_id)
        if maintenance is None:
            raise ValueError(Constants.MAINTENANCE_NOT_FOUND)
        return maintenance

    def create_maintenance(self, cmd: CreateMaintenanceCommand) -> Maintenance:
        self._get_car_or_raise(cmd.car_id)

        maintenance = Maintenance(
            id=uuid4(),
            car_id=cmd.car_id,
            description=cmd.description,
            date=cmd.date,
            km_at_maintenance=cmd.km_at_maintenance,
            cost=Decimal(str(cmd.cost)),
            type=cmd.type,
        )

        self.maintenance_repository.save(maintenance)
        return maintenance

    def get_maintenance(self, maintenance_id: UUID) -> Maintenance:
        return self._get_maintenance_or_raise(maintenance_id)

    def get_maintenances_for_car(self, car_id: UUID) -> list[Maintenance]:
        self._get_car_or_raise(car_id)
        return self.maintenance_repository.find_by_car_id(car_id)

    def find_all_maintenances(self) -> list[Maintenance]:
        return self.maintenance_repository.find_all()

    def update_maintenance(self, cmd: UpdateMaintenanceCommand) -> Maintenance:
        maintenance = self._get_maintenance_or_raise(cmd.maintenance_id)
        self._get_car_or_raise(cmd.car_id)

        maintenance.car_id = cmd.car_id
        maintenance.description = cmd.description
        maintenance.date = cmd.date
        maintenance.km_at_maintenance = cmd.km_at_maintenance
        maintenance.cost = Decimal(str(cmd.cost))
        maintenance.type = cmd.type

        self.maintenance_repository.save(maintenance)
        return maintenance

    def delete_maintenance(self, maintenance_id: UUID) -> None:
        self._get_maintenance_or_raise(maintenance_id)
        self.maintenance_repository.delete(maintenance_id)
