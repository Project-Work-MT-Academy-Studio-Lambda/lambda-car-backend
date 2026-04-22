from domain.car import Car 
from uuid import UUID

def car_to_dynamodb_item(car: Car) -> dict:
    return {
        'id': str(car.id),
        'trip_id': str(car.trip_id),
        'plate': car.plate,
        'km': car.km,
        'fuel_level': car.fuel_level
    }

def dynamodb_item_to_car(item: dict) -> Car:
    return Car(
        id=UUID(item['id']),
        trip_id=UUID(item['trip_id']),
        plate=item['plate'],
        km=item['km'],
        fuel_level=item['fuel_level']
    )