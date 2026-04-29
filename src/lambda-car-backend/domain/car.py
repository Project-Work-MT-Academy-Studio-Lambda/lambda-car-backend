from dataclasses import dataclass
from uuid import UUID
import re
from constants import Constants
from domain.enum.refueling_type import RefuelingType

@dataclass
class Car:
    id: UUID
    fuel_info: 'FuelInfo'
    mileage: 'Mileage'
    plate: str
    model: str
    co2_per_km: float | None = None


    def __post_init__(self):
        if not self.plate:
            raise ValueError(Constants.PLATE_CANNOT_BE_EMPTY)
        plate_clean = self.plate.replace(" ", "").upper()

        if len(plate_clean) != 7:
            raise ValueError(Constants.PLATE_MUST_BE_7_CHARACTERS.format(length=len(plate_clean)))
        
        pattern = r"^[A-Z]{2}[0-9]{3}[A-Z]{2}$"
        if not re.match(pattern, plate_clean):
            raise ValueError(Constants.INVALID_PLATE_FORMAT.format(plate=self.plate))
        if self.mileage.km_total < 0:
            raise ValueError(Constants.KM_CANNOT_BE_NEGATIVE)
        if self.fuel_info.level < 0:
            raise ValueError(Constants.FUEL_LEVEL_CANNOT_BE_NEGATIVE)

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

@dataclass
class FuelInfo:
    id: UUID
    type: RefuelingType
    level: int | None = None
    card: str | None = None

    def __post_init__(self):
        if self.level is not None and self.level < 0:
            raise ValueError(Constants.FUEL_LEVEL_CANNOT_BE_NEGATIVE)
        if self.card is not None and not self.card.strip():
            raise ValueError(Constants.FUEL_CARD_CANNOT_BE_EMPTY)