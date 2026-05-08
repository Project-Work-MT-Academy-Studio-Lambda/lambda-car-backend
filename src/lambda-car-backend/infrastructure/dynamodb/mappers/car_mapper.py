from uuid import UUID

from ....domain.car import Car, Mileage, FuelInfo
from ....domain.enum.car_status import CarStatus


def car_to_item(car: Car) -> dict:
    return {
        "id": str(car.id),
        "plate": car.plate,
        "model": car.model,
        "status": car.status,
        "mileage": {
            "km_total": car.mileage.km_total,
            "km_servicing": car.mileage.km_servicing,
            "km_wheels": car.mileage.km_wheels,
        },
        "fuel_info": {
            "type": car.fuel_info.type,
            "level": car.fuel_info.level,
            "card": car.fuel_info.card,
        },
    }


def item_to_car(item: dict) -> Car:
    mileage_item = item["mileage"]
    fuel_item = item["fuel_info"]

    return Car(
        id=UUID(item["id"]),
        plate=item["plate"],
        model=item.get("model"),
        status=CarStatus(item["status"]),
        mileage=Mileage(
            km_total=mileage_item["km_total"],
            km_servicing=mileage_item["km_servicing"],
            km_wheels=mileage_item["km_wheels"],
        ),
        fuel_info=FuelInfo(
            type=fuel_item["type"],
            level=fuel_item.get("level"),
            card=fuel_item.get("card"),
        ),
    )