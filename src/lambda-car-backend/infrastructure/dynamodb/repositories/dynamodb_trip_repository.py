from uuid import UUID
from boto3.dynamodb.conditions import Key

from domain.trip import Trip
from repositories.trip_repository import TripRepository
from infrastructure.dynamodb.mappers.trip_mapper import trip_to_item, item_to_trip


class DynamoDbTripRepository(TripRepository):
    def __init__(self, trip_table):
        self.trip_table = trip_table

    def get_by_id(self, trip_id: UUID) -> Trip | None:
        response = self.trip_table.get_item(Key={"id": str(trip_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_trip(item)

    def save(self, trip: Trip) -> None:
        self.trip_table.put_item(Item=trip_to_item(trip))

    def delete(self, trip_id: UUID) -> None:
        self.trip_table.delete_item(Key={"id": str(trip_id)})

    def list_by_user_id(self, user_id: UUID) -> list[Trip]:
        response = self.trip_table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(str(user_id)),
        )
        return [item_to_trip(item) for item in response.get("Items", [])]

    def list_by_car_id(self, car_id: UUID) -> list[Trip]:
        response = self.trip_table.query(
            IndexName="car_id-index",
            KeyConditionExpression=Key("car_id").eq(str(car_id)),
        )
        return [item_to_trip(item) for item in response.get("Items", [])]