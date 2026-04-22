from domain.trip import Trip
from uuid import UUID

def trip_to_dynamodb_item(trip: Trip) -> dict:
    return {
        'id': str(trip.id),
        'car_id': str(trip.car_id),
        'user_id': str(trip.user_id),
        'start_position': trip.start_position,
        'start_date': trip.start_date,
        'start_km': trip.start_km,
        'end_position': trip.end_position,
        'end_date': trip.end_date,
        'end_km': trip.end_km
    }

def dynamodb_item_to_trip(item: dict) -> Trip:
    return Trip(
        id=UUID(item['id']),
        car_id=UUID(item['car_id']),
        user_id=UUID(item['user_id']),
        start_position=item['start_position'],
        start_date=item['start_date'],
        start_km=item['start_km'],
        end_position=item.get('end_position'),
        end_date=item.get('end_date'),
        end_km=item.get('end_km')
    )

