from domain.trip import Trip
from uuid import UUID
from datetime import datetime
from domain.enum.trip_status import TripStatus

def trip_to_item(trip: Trip) -> dict:
    return {
        'id': str(trip.id),
        'car_id': str(trip.car_id),
        'user_id': str(trip.user_id),
        'start_position': trip.start_position,
        'start_date': trip.start_date.isoformat(),
        'start_km': trip.start_km,
        'end_position': trip.end_position,
        'end_date': trip.end_date.isoformat() if trip.end_date else None,
        'end_km': trip.end_km,
        'status': trip.status.value
    }

def item_to_trip(item: dict) -> Trip:
    return Trip(
        id=UUID(item['id']),
        car_id=UUID(item['car_id']),
        user_id=UUID(item['user_id']),
        start_position=item['start_position'],
        start_date=datetime.fromisoformat(item['start_date']),
        start_km=item['start_km'],
        end_position=item.get('end_position'),
        end_date=datetime.fromisoformat(item['end_date']) if item.get('end_date') else None,
        end_km=item.get('end_km'),
        status=TripStatus(item.get("status", TripStatus.ACTIVE.value)),
    )

