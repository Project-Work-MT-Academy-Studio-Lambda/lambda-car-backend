import pytest

from tests.conftest import CAR_ID, app_module


class FakeCarRepository:
    def __init__(self, car=None, existing_plate=None):
        self.car = car
        self.existing_plate = existing_plate
        self.saved = None
        self.deleted_id = None

    def get_by_plate(self, plate):
        if self.existing_plate == plate:
            return self.car
        return None

    def save(self, car):
        self.saved = car
        self.car = car

    def get_by_id(self, car_id):
        if self.car and self.car.id == car_id:
            return self.car
        return None

    def delete(self, car_id):
        self.deleted_id = car_id

    def find_free_cars(self):
        return [self.car] if self.car else []

    def find_all(self):
        return [self.car] if self.car else []


class TestCarService:
    def test_create_car_saves_new_car(self):
        service_module = app_module("services.car_service")
        command_module = app_module("commands.car_commands")
        repository = FakeCarRepository()
        service = service_module.CarService(repository)

        car = service.create_car(
            command_module.CreateCarCommand(
                plate="AB123CD",
                model="Fiat Panda",
                km_total=45000,
                km_servicing=50000,
                km_wheels=60000,
                fuel_type="DIESEL",
                fuel_level=70,
                fuel_card="CARD-001",
            )
        )

        assert car.plate == "AB123CD"
        assert repository.saved == car

    def test_create_car_rejects_duplicate_plate(self, car_factory):
        service_module = app_module("services.car_service")
        command_module = app_module("commands.car_commands")
        service = service_module.CarService(FakeCarRepository(car=car_factory(), existing_plate="AB123CD"))

        with pytest.raises(ValueError, match="Car with the same plate already exists"):
            service.create_car(
                command_module.CreateCarCommand(
                    plate="AB123CD",
                    model="Fiat Panda",
                    km_total=1,
                    km_servicing=2,
                    km_wheels=3,
                    fuel_type="DIESEL",
                )
            )

    def test_get_update_delete_and_list(self, car_factory):
        service_module = app_module("services.car_service")
        command_module = app_module("commands.car_commands")
        repository = FakeCarRepository(car=car_factory())
        service = service_module.CarService(repository)

        assert service.get_car(CAR_ID).id == CAR_ID
        assert service.find_all_cars() == [repository.car]
        assert service.get_active_cars() == [repository.car]

        updated = service.update_car(
            command_module.UpdateCarCommand(
                car_id=CAR_ID,
                plate="CD456EF",
                model="Toyota Yaris",
                km_total=23000,
                km_servicing=30000,
                km_wheels=40000,
                fuel_type="GASOLINE",
                fuel_level=45,
                fuel_card="CARD-002",
            )
        )
        assert updated.plate == "CD456EF"
        assert repository.saved == updated

        service.delete_car(CAR_ID)
        assert repository.deleted_id == CAR_ID
