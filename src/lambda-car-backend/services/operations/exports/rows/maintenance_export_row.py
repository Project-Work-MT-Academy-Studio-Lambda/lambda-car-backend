from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from .....domain.enum.maintenance_type import MaintenanceType

@dataclass(frozen=True)
class MaintenanceExportRow:
    car_plate:str
    description: str
    date: datetime
    km_at_maintenance: int
    cost: Decimal
    type: MaintenanceType