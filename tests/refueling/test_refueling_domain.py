from decimal import Decimal

import pytest


class TestRefuelingDomain:
    def test_creates_valid_refueling_and_total_cost(self, refueling_factory):
        refueling = refueling_factory(liter_price=Decimal("2.00"), liters=Decimal("10"))

        assert refueling.total_cost == Decimal("20.00")

    def test_rejects_invalid_values(self, refueling_factory):
        with pytest.raises(ValueError, match="Liter price cannot be negative"):
            refueling_factory(liter_price=Decimal("-1"))

        with pytest.raises(ValueError, match="Liters cannot be negative"):
            refueling_factory(liters=Decimal("-1"))

        with pytest.raises(ValueError, match="Receipt photo cannot be empty"):
            refueling_factory(receipt_photo="")

        with pytest.raises(ValueError, match="Fuel card cannot be empty"):
            refueling_factory(card_number=" ")
