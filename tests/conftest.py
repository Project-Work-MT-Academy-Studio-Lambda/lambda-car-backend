import importlib
import os
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

import pytest


os.environ.setdefault("AWS_ACCESS_KEY_ID", "fake")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "fakepassword")
os.environ.setdefault("AWS_REGION", "eu-west-1")
os.environ.setdefault("DYNAMODB_ENDPOINT_URL", "http://localhost:8001")
os.environ.setdefault("S3_ENDPOINT_URL", "http://localhost:9000")
os.environ.setdefault("JWT_SECRET", "dev-secret")


def app_module(module_path: str):
    return importlib.import_module(f"lambda-car-backend.{module_path}")


CAR_ID = UUID("33333333-3333-3333-3333-333333333333")
CAR_2_ID = UUID("44444444-4444-4444-4444-444444444444")
ADMIN_ID = UUID("11111111-1111-1111-1111-111111111111")
USER_ID = UUID("22222222-2222-2222-2222-222222222222")
COMMIT_ID = UUID("77777777-7777-7777-7777-777777777777")
TRIP_ID = UUID("55555555-5555-5555-5555-555555555555")
REFUELING_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
MAINTENANCE_ID = UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")


@pytest.fixture
def maintenance_type():
    return app_module("domain.enum.maintenance_type").MaintenanceType


@pytest.fixture
def maintenance_factory(maintenance_type):
    Maintenance = app_module("domain.maintenance").Maintenance

    def factory(
        maintenance_id=MAINTENANCE_ID,
        car_id=CAR_ID,
        description="Tagliando olio e filtri",
        date=datetime(2024, 5, 10, 9, 0, tzinfo=timezone.utc),
        km_at_maintenance=45000,
        cost=Decimal("185.50"),
        type=maintenance_type.ROUTINE_SERVICE,
    ):
        return Maintenance(
            id=maintenance_id,
            car_id=car_id,
            description=description,
            date=date,
            km_at_maintenance=km_at_maintenance,
            cost=cost,
            type=type,
        )

    return factory


@pytest.fixture
def car_factory():
    car_module = app_module("domain.car")
    RefuelingType = app_module("domain.enum.refueling_type").RefuelingType
    CarStatus = app_module("domain.enum.car_status").CarStatus

    def factory(
        car_id=CAR_ID,
        plate="AB123CD",
        model="Fiat Panda",
        km_total=45000,
        km_servicing=50000,
        km_wheels=60000,
        fuel_type=RefuelingType.DIESEL,
        fuel_level=70,
        fuel_card="CARD-001",
        status=CarStatus.FREE,
        co2_per_km=95.5,
    ):
        return car_module.Car(
            id=car_id,
            plate=plate,
            model=model,
            mileage=car_module.Mileage(
                km_total=km_total,
                km_servicing=km_servicing,
                km_wheels=km_wheels,
            ),
            fuel_info=car_module.FuelInfo(
                type=fuel_type,
                level=fuel_level,
                card=fuel_card,
            ),
            status=status,
            co2_per_km=co2_per_km,
        )

    return factory


@pytest.fixture
def user_factory():
    User = app_module("domain.user").User
    Role = app_module("domain.enum.role").Role

    def factory(
        user_id=USER_ID,
        name="Mario Rossi",
        email="user@test.com",
        hashed_password="hashed-password",
        role=Role.USER,
    ):
        return User(
            id=user_id,
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )

    return factory


@pytest.fixture
def commit_factory():
    Commit = app_module("domain.commit").Commit
    CommitStatus = app_module("domain.enum.commit_status").CommitStatus

    def factory(
        commit_id=COMMIT_ID,
        code="COMM-001",
        description="Intervento cliente Napoli",
        status=CommitStatus.BACKLOG,
        trip_id=None,
    ):
        return Commit(
            id=commit_id,
            code=code,
            description=description,
            status=status,
            trip_id=trip_id,
        )

    return factory


@pytest.fixture
def trip_factory():
    Trip = app_module("domain.trip").Trip
    TripStatus = app_module("domain.enum.trip_status").TripStatus

    def factory(
        trip_id=TRIP_ID,
        car_id=CAR_ID,
        user_id=USER_ID,
        commit_id=COMMIT_ID,
        start_position="Roma",
        start_date=datetime(2024, 5, 10, 8, 0, tzinfo=timezone.utc),
        start_km=45000,
        status=TripStatus.ACTIVE,
        end_position=None,
        end_date=None,
        end_km=None,
    ):
        return Trip(
            id=trip_id,
            car_id=car_id,
            user_id=user_id,
            commit_id=commit_id,
            start_position=start_position,
            start_date=start_date,
            start_km=start_km,
            status=status,
            end_position=end_position,
            end_date=end_date,
            end_km=end_km,
        )

    return factory


@pytest.fixture
def refueling_factory():
    Refueling = app_module("domain.refueling").Refueling

    def factory(
        refueling_id=REFUELING_ID,
        car_id=CAR_ID,
        date=datetime(2024, 5, 10, 7, 30, tzinfo=timezone.utc),
        liter_price=Decimal("1.82"),
        liters=Decimal("40.5"),
        receipt_photo="receipts/refueling.jpg",
        card_number="CARD-001",
    ):
        return Refueling(
            id=refueling_id,
            car_id=car_id,
            date=date,
            liter_price=liter_price,
            liters=liters,
            receipt_photo=receipt_photo,
            card_number=card_number,
        )

    return factory


@pytest.fixture
def api_client_factory():
    def factory(overrides):
        app = app_module("app").app
        app.dependency_overrides.clear()
        app.dependency_overrides.update(overrides)
        from fastapi.testclient import TestClient

        return TestClient(app)

    yield factory
    app_module("app").app.dependency_overrides.clear()
