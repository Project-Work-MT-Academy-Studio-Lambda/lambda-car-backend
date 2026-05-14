from uuid import UUID
from datetime import datetime
from decimal import Decimal
from ....domain.maintenance import Maintenance
from ....domain.enum.maintenance_type import MaintenanceType

def maintenance_to_item(maintenance: Maintenance) -> dict:
    return {
        "id": str(maintenance.id),
        "car_id": str(maintenance.car_id),
        "date": maintenance.date.isoformat(),
        "km_at_maintenance": maintenance.km_at_maintenance,
        "cost": float(maintenance.cost),
        "description": maintenance.description,
        "type": maintenance.type.value,
    }

def item_to_maintenance(item: dict) -> Maintenance:
    return Maintenance(
        id=UUID(item["id"]),
        car_id=UUID(item["car_id"]),
        date=datetime.fromisoformat(item["date"]),
        km_at_maintenance=item["km_at_maintenance"],
        cost=Decimal(str(item["cost"])),
        description=item["description"],
        type=MaintenanceType(item["type"]),
    )