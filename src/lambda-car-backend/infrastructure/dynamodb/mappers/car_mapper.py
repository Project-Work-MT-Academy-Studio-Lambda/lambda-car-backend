from uuid import UUID

from domain.car import Car, Mileage, FuelInfo


def car_to_item(car: Car) -> dict:
    return {
        "id": str(car.id),
        "plate": car.plate,
        "model": car.model,
        "mileage": {
            "km_total": car.mileage.km_total,
            "km_servicing": car.mileage.km_servicing,
            "km_wheels": car.mileage.km_wheels,
        },
        "fuel_info": {
            "type": car.fuel_info.fuel_type,
            "level": car.fuel_info.fuel_level,
            "card": car.fuel_info.fuel_card,
        },
    }


def item_to_car(item: dict) -> Car:
    mileage_item = item["mileage"]
    fuel_item = item["fuel_info"]

    return Car(
        id=UUID(item["id"]),
        plate=item["plate"],
        model=item.get("model"),
        mileage=Mileage(
            km_total=mileage_item["km_total"],
            km_servicing=mileage_item["km_servicing"],
            km_wheels=mileage_item["km_wheels"],
        ),
        fuel_info=FuelInfo(
            fuel_type=fuel_item["type"],
            fuel_level=fuel_item.get("level"),
            fuel_card=fuel_item.get("card"),
        ),
    )