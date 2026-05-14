from uuid import uuid4

import pytest

from tests.conftest import CAR_ID, MAINTENANCE_ID, app_module


class FakeCarRepository:
    def __init__(self, existing_car=True):
        self.existing_car = existing_car
        self.requested_car_ids = []

    def get_by_id(self, car_id):
        self.requested_car_ids.append(car_id)
        if not self.existing_car:
            return None
        return object()


class FakeMaintenanceRepository:
    def __init__(self, maintenance=None, maintenances=None):
        self.maintenance = maintenance
        self.maintenances = maintenances or []
        self.saved = None
        self.deleted_id = None

    def get_by_id(self, maintenance_id):
        if self.maintenance and self.maintenance.id == maintenance_id:
            return self.maintenance
        return None

    def save(self, maintenance):
        self.saved = maintenance

    def delete(self, maintenance_id):
        self.deleted_id = maintenance_id

    def find_by_car_id(self, car_id):
        return [maintenance for maintenance in self.maintenances if maintenance.car_id == car_id]

    def find_all(self):
        return self.maintenances


class TestMaintenanceService:
    def test_create_validates_car_and_saves(self, maintenance_factory):
        service_module = app_module("services.maintenance_service")
        command_module = app_module("commands.maintenance_commands")
        maintenance = maintenance_factory()
        maintenance_repository = FakeMaintenanceRepository()
        car_repository = FakeCarRepository()
        service = service_module.MaintenanceService(maintenance_repository, car_repository)

        result = service.create_maintenance(
            command_module.CreateMaintenanceCommand(
                car_id=maintenance.car_id,
                description=maintenance.description,
                date=maintenance.date,
                km_at_maintenance=maintenance.km_at_maintenance,
                cost=float(maintenance.cost),
                type=maintenance.type,
            )
        )

        assert result.car_id == maintenance.car_id
        assert result.description == maintenance.description
        assert maintenance_repository.saved == result
        assert car_repository.requested_car_ids == [maintenance.car_id]

    def test_create_raises_when_car_is_missing(self, maintenance_factory):
        service_module = app_module("services.maintenance_service")
        command_module = app_module("commands.maintenance_commands")
        maintenance = maintenance_factory()
        service = service_module.MaintenanceService(
            FakeMaintenanceRepository(),
            FakeCarRepository(existing_car=False),
        )

        with pytest.raises(ValueError, match="Car not found"):
            service.create_maintenance(
                command_module.CreateMaintenanceCommand(
                    car_id=maintenance.car_id,
                    description=maintenance.description,
                    date=maintenance.date,
                    km_at_maintenance=maintenance.km_at_maintenance,
                    cost=float(maintenance.cost),
                    type=maintenance.type,
                )
            )

    def test_get_find_update_and_delete(self, maintenance_factory, maintenance_type):
        service_module = app_module("services.maintenance_service")
        command_module = app_module("commands.maintenance_commands")
        maintenance = maintenance_factory()
        repository = FakeMaintenanceRepository(maintenance=maintenance, maintenances=[maintenance])
        service = service_module.MaintenanceService(repository, FakeCarRepository())

        assert service.get_maintenance(MAINTENANCE_ID) == maintenance
        assert service.find_all_maintenances() == [maintenance]
        assert service.get_maintenances_for_car(CAR_ID) == [maintenance]

        updated = service.update_maintenance(
            command_module.UpdateMaintenanceCommand(
                maintenance_id=MAINTENANCE_ID,
                car_id=CAR_ID,
                description="Controllo impianto elettrico",
                date=maintenance.date,
                km_at_maintenance=46000,
                cost=145.0,
                type=maintenance_type.ELECTRICAL,
            )
        )

        assert updated.description == "Controllo impianto elettrico"
        assert repository.saved == updated

        service.delete_maintenance(MAINTENANCE_ID)
        assert repository.deleted_id == MAINTENANCE_ID

    def test_get_raises_when_missing(self):
        service_module = app_module("services.maintenance_service")
        service = service_module.MaintenanceService(FakeMaintenanceRepository(), FakeCarRepository())

        with pytest.raises(ValueError, match="Maintenance not found"):
            service.get_maintenance(uuid4())
