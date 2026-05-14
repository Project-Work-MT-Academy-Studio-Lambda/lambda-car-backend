from tests.conftest import CAR_ID, COMMIT_ID, TRIP_ID, USER_ID, app_module


class FakeTripService:
    def __init__(self, trip):
        self.trip = trip
        self.opened = None
        self.updated = None
        self.closed = None
        self.deleted = None

    def open_trip(self, cmd):
        self.opened = cmd
        return self.trip

    def get_trips_for_user(self, user_id):
        return [self.trip]

    def get_trip(self, trip_id):
        return self.trip

    def update_trip(self, cmd):
        self.updated = cmd
        return self.trip

    def close_trip(self, cmd):
        self.closed = cmd
        return self.trip

    def delete_trip(self, cmd):
        self.deleted = cmd


class TestTripRouter:
    def _client(self, api_client_factory, service):
        dependencies = app_module("dependencies")
        CurrentUser = app_module("domain.user").CurrentUser
        Role = app_module("domain.enum.role").Role
        return api_client_factory(
            {
                dependencies.require_user: lambda: CurrentUser(id=str(USER_ID), role=Role.USER),
                dependencies.get_trip_service: lambda: service,
            }
        )

    def test_trip_routes(self, api_client_factory, trip_factory):
        trip = trip_factory()
        service = FakeTripService(trip)
        client = self._client(api_client_factory, service)

        payload = {
            "car_id": str(CAR_ID),
            "commit_id": str(COMMIT_ID),
            "start_position": "Roma",
            "start_date": trip.start_date.isoformat(),
            "start_km": 45000,
        }
        open_response = client.post("/api/v1/lambdacar/trips/", json=payload)
        assert open_response.status_code == 201
        assert open_response.json()["commit_id"] == str(trip.commit_id)
        assert service.opened.car_id == CAR_ID

        list_response = client.get("/api/v1/lambdacar/trips/")
        assert list_response.status_code == 200
        assert list_response.json()[0]["commit_id"] == str(trip.commit_id)
        assert client.get(f"/api/v1/lambdacar/trips/{TRIP_ID}").status_code == 200

        update_payload = {
            "car_id": str(CAR_ID),
            "start_position": "Roma",
            "start_date": trip.start_date.isoformat(),
            "start_km": 45000,
            "end_position": None,
            "end_date": None,
            "end_km": None,
        }
        assert client.put(f"/api/v1/lambdacar/trips/{TRIP_ID}", json=update_payload).status_code == 200
        assert service.updated.trip_id == TRIP_ID

        close_payload = {
            "end_position": "Napoli",
            "end_date": trip.start_date.isoformat(),
            "end_km": 45225,
        }
        assert client.patch(f"/api/v1/lambdacar/trips/{TRIP_ID}/close", json=close_payload).status_code == 200
        assert service.closed.trip_id == TRIP_ID

        assert client.delete(f"/api/v1/lambdacar/trips/{TRIP_ID}").status_code == 204
        assert service.deleted.trip_id == TRIP_ID
