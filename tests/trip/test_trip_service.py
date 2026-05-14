from datetime import datetime, timezone

from tests.conftest import CAR_ID, COMMIT_ID, TRIP_ID, USER_ID, app_module


class FakeTripRepository:
    def __init__(self, trip=None, active_trip=None):
        self.trip = trip
        self.active_trip = active_trip
        self.saved = None
        self.deleted_id = None

    def get_by_id(self, trip_id):
        if self.trip and self.trip.id == trip_id:
            return self.trip
        return None

    def save(self, trip):
        self.saved = trip
        self.trip = trip

    def get_active_trip_by_car_id(self, car_id):
        return self.active_trip

    def list_by_user_id(self, user_id):
        return [self.trip] if self.trip and self.trip.user_id == user_id else []

    def delete(self, trip_id):
        self.deleted_id = trip_id


class FakeRepository:
    def __init__(self, item=None):
        self.item = item
        self.saved = None

    def get_by_id(self, item_id):
        if self.item and self.item.id == item_id:
            return self.item
        return None

    def save(self, item):
        self.saved = item

    def close_commit_by_trip_id(self, trip_id):
        self.closed_trip_id = trip_id


class TestTripService:
    def test_open_trip_updates_commit_car_and_trip(self, car_factory, user_factory, commit_factory):
        service_module = app_module("services.trip_service")
        command_module = app_module("commands.trip_commands")
        service = service_module.TripService(
            trip_repository=FakeTripRepository(),
            user_repository=FakeRepository(user_factory()),
            car_repository=FakeRepository(car_factory()),
            commit_repository=FakeRepository(commit_factory()),
        )

        trip = service.open_trip(
            command_module.OpenTripCommand(
                user_id=USER_ID,
                car_id=CAR_ID,
                commit_id=COMMIT_ID,
                start_position="Roma",
                start_date=datetime.now(timezone.utc),
                start_km=45000,
            )
        )

        assert trip.car_id == CAR_ID
        assert trip.user_id == USER_ID
        assert trip.commit_id == COMMIT_ID

    def test_get_trips_for_user_returns_repository_items(self, trip_factory, user_factory, car_factory, commit_factory):
        service_module = app_module("services.trip_service")
        trip = trip_factory()
        service = service_module.TripService(
            trip_repository=FakeTripRepository(trip=trip),
            user_repository=FakeRepository(user_factory()),
            car_repository=FakeRepository(car_factory()),
            commit_repository=FakeRepository(commit_factory()),
        )

        assert service.get_trip(TRIP_ID) == trip
        assert service.get_trips_for_user(USER_ID) == [trip]

    def test_delete_trip_frees_trip_car(self, trip_factory, user_factory, car_factory, commit_factory):
        service_module = app_module("services.trip_service")
        command_module = app_module("commands.trip_commands")
        trip = trip_factory()
        car = car_factory()
        service = service_module.TripService(
            trip_repository=FakeTripRepository(trip=trip),
            user_repository=FakeRepository(user_factory()),
            car_repository=FakeRepository(car),
            commit_repository=FakeRepository(commit_factory()),
        )

        service.delete_trip(command_module.DeleteTripCommand(trip_id=TRIP_ID, user_id=USER_ID))

        assert service.car_repository.saved.id == CAR_ID
        assert service.trip_repository.deleted_id == TRIP_ID
