import pytest

from tests.conftest import app_module


class TestCarDomain:
    def test_creates_valid_car(self, car_factory):
        car = car_factory()

        assert car.plate == "AB123CD"
        assert car.mileage.km_total == 45000
        assert car.fuel_info.card == "CARD-001"

    def test_rejects_invalid_plate_and_negative_values(self, car_factory):
        with pytest.raises(ValueError, match="Plate must be 7 characters"):
            car_factory(plate="ABC")

        with pytest.raises(ValueError, match="Invalid plate format"):
            car_factory(plate="123ABCD")

        with pytest.raises(ValueError, match="Total km cannot be negative"):
            car_factory(km_total=-1)

        with pytest.raises(ValueError, match="Fuel level cannot be negative"):
            car_factory(fuel_level=-1)

    def test_rejects_empty_fuel_card(self):
        FuelInfo = app_module("domain.car").FuelInfo
        RefuelingType = app_module("domain.enum.refueling_type").RefuelingType

        with pytest.raises(ValueError, match="Fuel card cannot be empty"):
            FuelInfo(type=RefuelingType.DIESEL, level=10, card=" ")
