from tests.conftest import CAR_ID, REFUELING_ID, USER_ID, app_module


class FakeCarRepository:
    def __init__(self, car):
        self.car = car

    def get_by_id(self, car_id):
        if self.car and self.car.id == car_id:
            return self.car
        return None


class FakeRefuelingRepository:
    def __init__(self, refueling=None):
        self.refueling = refueling
        self.saved = None
        self.deleted_id = None

    def get_by_id(self, refueling_id, user_id=None, user_role=None):
        if self.refueling and self.refueling.id == refueling_id:
            return self.refueling
        return None

    def save(self, refueling):
        self.saved = refueling
        self.refueling = refueling

    def list_by_car_id(self, car_id):
        return [self.refueling] if self.refueling and self.refueling.car_id == car_id else []

    def delete(self, refueling_id):
        self.deleted_id = refueling_id


class FakeReceiptStorage:
    def save_receipt_photo(self, refueling_id, filename, content, content_type):
        self.saved = (refueling_id, filename, content, content_type)
        return f"receipts/{refueling_id}.jpg"


class TestRefuelingService:
    def test_create_refueling_saves_receipt_and_refueling(self, car_factory, refueling_factory):
        service_module = app_module("services.refueling_service")
        command_module = app_module("commands.refueling_commands")
        repository = FakeRefuelingRepository()
        storage = FakeReceiptStorage()
        refueling = refueling_factory()
        service = service_module.RefuelingService(repository, FakeCarRepository(car_factory()), storage)

        created = service.create_refueling(
            command_module.CreateRefuelingCommand(
                car_id=CAR_ID,
                liters=refueling.liters,
                liter_price=refueling.liter_price,
                date=refueling.date,
                card_number=refueling.card_number,
                receipt_filename="receipt.jpg",
                receipt_content=b"content",
                receipt_content_type="image/jpeg",
                user_id=USER_ID,
                user_role="USER",
            )
        )

        assert created.car_id == CAR_ID
        assert created.receipt_photo.startswith("receipts/")
        assert repository.saved == created

    def test_get_list_update_and_delete(self, car_factory, refueling_factory):
        service_module = app_module("services.refueling_service")
        command_module = app_module("commands.refueling_commands")
        repository = FakeRefuelingRepository(refueling_factory())
        service = service_module.RefuelingService(repository, FakeCarRepository(car_factory()), FakeReceiptStorage())

        assert service.get_refueling(REFUELING_ID, USER_ID, "USER") == repository.refueling
        assert service.get_refuelings_for_car(CAR_ID) == [repository.refueling]

        updated = service.update_refueling(
            command_module.UpdateRefuelingCommand(
                refueling_id=REFUELING_ID,
                car_id=CAR_ID,
                liters=10,
                liter_price=repository.refueling.liter_price,
                date=repository.refueling.date,
                card_number="CARD-001",
                user_id=USER_ID,
                user_role="USER",
            )
        )
        assert updated.liters == 10
        assert repository.saved == updated

        service.delete_refueling(REFUELING_ID, USER_ID, "USER")
        assert repository.deleted_id == REFUELING_ID
