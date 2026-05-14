from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from tests.conftest import CAR_ID, MAINTENANCE_ID, app_module


class TestMaintenanceDomain:
    def test_creates_valid_maintenance(self, maintenance_type):
        Maintenance = app_module("domain.maintenance").Maintenance

        maintenance = Maintenance(
            id=MAINTENANCE_ID,
            car_id=CAR_ID,
            description="Controllo freni",
            date=datetime(2024, 5, 10, 9, 0, tzinfo=timezone.utc),
            km_at_maintenance=32000,
            cost=Decimal("92.00"),
            type=maintenance_type.BRAKES,
        )

        assert maintenance.id == MAINTENANCE_ID
        assert maintenance.car_id == CAR_ID
        assert maintenance.type == maintenance_type.BRAKES

    def test_rejects_invalid_values(self, maintenance_factory):
        with pytest.raises(ValueError, match="Description cannot be empty"):
            maintenance_factory(description="")

        with pytest.raises(ValueError, match="Date cannot be in the future"):
            maintenance_factory(date=datetime.now(timezone.utc) + timedelta(days=1))

        with pytest.raises(ValueError, match="Km at maintenance cannot be negative"):
            maintenance_factory(km_at_maintenance=-1)

        with pytest.raises(ValueError, match="Cost cannot be negative"):
            maintenance_factory(cost=Decimal("-1.00"))
