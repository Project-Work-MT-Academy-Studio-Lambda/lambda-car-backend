from dataclasses import dataclass
from uuid import UUID
from constants import Constants

@dataclass
class Mileage:
    id: UUID
    km_total: int
    km_servicing: int
    km_wheels: int

    def __post_init__(self):
        if self.km_total < 0:
            raise ValueError(Constants.KM_TOTAL_CANNOT_BE_NEGATIVE)
        if self.km_servicing < 0:
            raise ValueError(Constants.KM_SERVICING_CANNOT_BE_NEGATIVE)
        if self.km_wheels < 0:
            raise ValueError(Constants.KM_WHEELS_CANNOT_BE_NEGATIVE)