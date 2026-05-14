from tests.conftest import CAR_ID, REFUELING_ID, USER_ID, app_module


class FakeRefuelingService:
    def __init__(self, refueling):
        self.refueling = refueling
        self.created = None
        self.updated = None
        self.deleted_id = None

    def get_refuelings_for_car(self, car_id, *args, **kwargs):
        return [self.refueling]

    def get_refueling(self, refueling_id, user_id, user_role):
        return self.refueling

    def create_refueling(self, cmd):
        self.created = cmd
        return self.refueling

    def update_refueling(self, cmd):
        self.updated = cmd
        return self.refueling

    def delete_refueling(self, refueling_id, user_id, user_role):
        self.deleted_id = refueling_id


class TestRefuelingRouter:
    def _client(self, api_client_factory, service):
        dependencies = app_module("dependencies")
        CurrentUser = app_module("domain.user").CurrentUser
        Role = app_module("domain.enum.role").Role
        return api_client_factory(
            {
                dependencies.require_user: lambda: CurrentUser(id=USER_ID, role=Role.USER),
                dependencies.get_refueling_service: lambda: service,
            }
        )

    def test_refueling_routes(self, api_client_factory, refueling_factory):
        refueling = refueling_factory()
        service = FakeRefuelingService(refueling)
        client = self._client(api_client_factory, service)

        assert client.get(f"/api/v1/lambdacar/refuelings/car/{CAR_ID}").status_code == 200
        assert client.get(f"/api/v1/lambdacar/refuelings/{REFUELING_ID}").status_code == 200

        create_response = client.post(
            "/api/v1/lambdacar/refuelings/",
            data={
                "car_id": str(CAR_ID),
                "liters": "40.5",
                "liter_price": "1.82",
                "date": refueling.date.isoformat(),
                "card_number": "CARD-001",
            },
            files={"receipt_photo": ("receipt.jpg", b"content", "image/jpeg")},
        )
        assert create_response.status_code == 201
        assert service.created.car_id == CAR_ID

        update_response = client.put(
            f"/api/v1/lambdacar/refuelings/{REFUELING_ID}",
            json={
                "car_id": str(CAR_ID),
                "liters": "35.0",
                "liter_price": "1.80",
                "date": refueling.date.isoformat(),
                "receipt_photo": "receipts/refueling.jpg",
                "card_number": "CARD-001",
            },
        )
        assert update_response.status_code == 200
        assert service.updated.refueling_id == REFUELING_ID

        assert client.delete(f"/api/v1/lambdacar/refuelings/{REFUELING_ID}").status_code == 204
        assert service.deleted_id == REFUELING_ID
