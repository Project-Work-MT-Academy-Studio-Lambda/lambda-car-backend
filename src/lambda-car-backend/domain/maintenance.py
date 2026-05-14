from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timezone
from ..constants import Constants
from decimal import Decimal
from .enum.maintenance_type import MaintenanceType

@dataclass
class Maintenance:
    id: UUID
    car_id: UUID
    description: str
    date: datetime
    km_at_maintenance: int
    cost: Decimal
    type: MaintenanceType

    def __post_init__(self):
        now = datetime.now(timezone.utc)
        if not self.description:
            raise ValueError(Constants.DESCRIPTION_CANNOT_BE_EMPTY)
        if self.date > now:
            raise ValueError(Constants.DATE_CANNOT_BE_IN_THE_FUTURE)
        if self.km_at_maintenance < 0:
            raise ValueError(Constants.KM_AT_MAINTENANCE_CANNOT_BE_NEGATIVE)
        if self.cost < 0:
            raise ValueError(Constants.COST_CANNOT_BE_NEGATIVE)