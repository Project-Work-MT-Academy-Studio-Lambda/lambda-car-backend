from tests.conftest import ADMIN_ID, CAR_ID, MAINTENANCE_ID, app_module


class FakeMaintenanceService:
    def __init__(self, maintenance):
        self.maintenance = maintenance
        self.created_command = None
        self.updated_command = None
        self.deleted_id = None

    def find_all_maintenances(self):
        return [self.maintenance]

    def get_maintenances_for_car(self, car_id):
        return [self.maintenance]

    def get_maintenance(self, maintenance_id):
        if maintenance_id != self.maintenance.id:
            raise ValueError("Maintenance not found")
        return self.maintenance

    def create_maintenance(self, cmd):
        self.created_command = cmd
        return self.maintenance

    def update_maintenance(self, cmd):
        self.updated_command = cmd
        return self.maintenance

    def delete_maintenance(self, maintenance_id):
        self.deleted_id = maintenance_id


class TestMaintenanceRouter:
    def _client(self, api_client_factory, service):
        dependencies = app_module("dependencies")
        CurrentUser = app_module("domain.user").CurrentUser
        Role = app_module("domain.enum.role").Role

        return api_client_factory(
            {
                dependencies.require_admin: lambda: CurrentUser(id=ADMIN_ID, role=Role.ADMIN),
                dependencies.get_maintenance_service: lambda: service,
            }
        )

    def test_list_get_create_update_and_delete(self, api_client_factory, maintenance_factory):
        maintenance = maintenance_factory()
        service = FakeMaintenanceService(maintenance)
        client = self._client(api_client_factory, service)

        list_response = client.get("/api/v1/lambdacar/admin/maintenances/")
        assert list_response.status_code == 200
        assert list_response.json()[0]["id"] == str(MAINTENANCE_ID)

        car_response = client.get(f"/api/v1/lambdacar/admin/maintenances/car/{CAR_ID}")
        assert car_response.status_code == 200
        assert car_response.json()[0]["car_id"] == str(CAR_ID)

        get_response = client.get(f"/api/v1/lambdacar/admin/maintenances/{MAINTENANCE_ID}")
        assert get_response.status_code == 200

        payload = {
            "car_id": str(maintenance.car_id),
            "date": maintenance.date.isoformat(),
            "km_at_maintenance": maintenance.km_at_maintenance,
            "cost": float(maintenance.cost),
            "description": maintenance.description,
            "type": maintenance.type.value,
        }

        create_response = client.post("/api/v1/lambdacar/admin/maintenances/", json=payload)
        assert create_response.status_code == 201
        assert service.created_command.car_id == CAR_ID

        update_response = client.put(
            f"/api/v1/lambdacar/admin/maintenances/{MAINTENANCE_ID}",
            json={**payload, "description": "Controllo impianto elettrico"},
        )
        assert update_response.status_code == 200
        assert service.updated_command.description == "Controllo impianto elettrico"

        delete_response = client.delete(f"/api/v1/lambdacar/admin/maintenances/{MAINTENANCE_ID}")
        assert delete_response.status_code == 204
        assert service.deleted_id == MAINTENANCE_ID

    def test_get_returns_404_when_missing(self, api_client_factory, maintenance_factory):
        service = FakeMaintenanceService(maintenance_factory())
        client = self._client(api_client_factory, service)

        response = client.get("/api/v1/lambdacar/admin/maintenances/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

        assert response.status_code == 404
        assert response.json()["detail"] == "Maintenance not found"
