from uuid import UUID
from boto3.dynamodb.conditions import Key

from domain.car import Car
from repositories.car_repository import CarRepository
from infrastructure.dynamodb.mappers.car_mapper import car_to_item, item_to_car


class DynamoDbCarRepository(CarRepository):
    def __init__(self, car_table):
        self.car_table = car_table

    def get_by_id(self, car_id: UUID) -> Car | None:
        response = self.car_table.get_item(Key={"id": str(car_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_car(item)

    def get_by_plate(self, plate: str) -> Car | None:
        response = self.car_table.query(
            IndexName="plate-index",
            KeyConditionExpression=Key("plate").eq(plate),
        )
        items = response.get("Items", [])
        if not items:
            return None
        return item_to_car(items[0])

    def save(self, car: Car) -> None:
        self.car_table.put_item(Item=car_to_item(car))

    def delete(self, car_id: UUID) -> None:
        self.car_table.delete_item(Key={"id": str(car_id)})