from datetime import datetime, timedelta, timezone

import pytest


class TestTripDomain:
    def test_creates_active_trip_and_calculates_distance_duration(self, trip_factory):
        trip = trip_factory(
            end_position="Napoli",
            end_date=datetime(2024, 5, 10, 11, 0, tzinfo=timezone.utc),
            end_km=45225,
        )

        assert trip.distance == 225
        assert trip.duration == 180

    def test_rejects_invalid_open_trip_values(self, trip_factory):
        with pytest.raises(ValueError, match="Start position cannot be empty"):
            trip_factory(start_position="")

        with pytest.raises(ValueError, match="Start km cannot be negative"):
            trip_factory(start_km=-1)

    def test_close_trip_sets_closed_state(self, trip_factory):
        trip = trip_factory()
        end_date = trip.start_date + timedelta(hours=2)

        trip.close_trip("Napoli", end_date, 45225)

        assert trip.end_position == "Napoli"
        assert trip.end_km == 45225
        assert trip.distance == 225
