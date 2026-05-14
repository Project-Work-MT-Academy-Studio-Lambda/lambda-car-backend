from tests.conftest import ADMIN_ID, CAR_ID, app_module


class FakeCarService:
    def __init__(self, car):
        self.car = car
        self.created_command = None
        self.updated_command = None
        self.deleted_id = None

    def find_all_cars(self):
        return [self.car]

    def get_active_cars(self):
        return [self.car]

    def get_car(self, car_id):
        return self.car

    def create_car(self, cmd):
        self.created_command = cmd
        return self.car

    def update_car(self, cmd):
        self.updated_command = cmd
        return self.car

    def delete_car(self, car_id):
        self.deleted_id = car_id


class TestCarRouter:
    def _client(self, api_client_factory, service):
        dependencies = app_module("dependencies")
        CurrentUser = app_module("domain.user").CurrentUser
        Role = app_module("domain.enum.role").Role
        return api_client_factory(
            {
                dependencies.require_admin: lambda: CurrentUser(id=ADMIN_ID, role=Role.ADMIN),
                dependencies.get_car_service: lambda: service,
            }
        )

    def test_admin_car_crud_routes(self, api_client_factory, car_factory):
        service = FakeCarService(car_factory())
        client = self._client(api_client_factory, service)

        assert client.get("/api/v1/lambdacar/admin/cars/").status_code == 200
        assert client.get("/api/v1/lambdacar/admin/cars/active").status_code == 200
        assert client.get(f"/api/v1/lambdacar/admin/cars/{CAR_ID}").status_code == 200

        payload = {
            "plate": "AB123CD",
            "model": "Fiat Panda",
            "mileage": {"km_total": 45000, "km_servicing": 50000, "km_wheels": 60000},
            "fuel_info": {"type": "DIESEL", "level": 70, "card": "CARD-001"},
        }
        assert client.post("/api/v1/lambdacar/admin/cars/", json=payload).status_code == 201
        assert service.created_command.plate == "AB123CD"

        assert client.put(f"/api/v1/lambdacar/admin/cars/{CAR_ID}", json=payload).status_code == 200
        assert service.updated_command.car_id == CAR_ID

        assert client.delete(f"/api/v1/lambdacar/admin/cars/{CAR_ID}").status_code == 204
        assert service.deleted_id == CAR_ID
