from uuid import UUID
from boto3.dynamodb.conditions import Key
from ....repositories.maintenance_repository import MaintenanceRepository
from ....domain.maintenance import Maintenance
from ....infrastructure.dynamodb.mappers.maintenance_mapper import maintenance_to_item, item_to_maintenance

class DynamoDbMaintenanceRepository(MaintenanceRepository):
    def __init__(self, maintenance_table):
        self.maintenance_table = maintenance_table

    def get_by_id(self, maintenance_id: UUID) -> Maintenance | None:
        response = self.maintenance_table.get_item(Key={"id": str(maintenance_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_maintenance(item)

    def save(self, maintenance: Maintenance) -> None:
        self.maintenance_table.put_item(Item=maintenance_to_item(maintenance))

    def delete(self, maintenance_id: UUID) -> None:
        self.maintenance_table.delete_item(Key={"id": str(maintenance_id)})
    
    def find_by_car_id(self, car_id: UUID) -> list[Maintenance]:
        response = self.maintenance_table.query(
            IndexName="car_id-index",
            KeyConditionExpression=Key("car_id").eq(str(car_id)),
        )
        return [item_to_maintenance(item) for item in response.get("Items", [])]
    
    def find_all(self) -> list[Maintenance]:
        response = self.maintenance_table.scan()
        return [item_to_maintenance(item) for item in response.get("Items", [])]