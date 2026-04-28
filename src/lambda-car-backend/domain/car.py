from dataclasses import dataclass
from uuid import UUID
import re
from constants import Constants

@dataclass
class Car:
    id: UUID
    fuel_info_id: UUID
    mileage_id: UUID
    plate: str
    model: str
    c02_per_km: float | None = None

    def __post_init__(self):
        if not self.plate:
            raise ValueError(Constants.PLATE_CANNOT_BE_EMPTY)
        plate_clean = self.plate.replace(" ", "").upper()

        if len(plate_clean) != 7:
            raise ValueError(Constants.PLATE_MUST_BE_7_CHARACTERS.format(length=len(plate_clean)))
        
        pattern = r"^[A-Z]{2}[0-9]{3}[A-Z]{2}$"
        if not re.match(pattern, plate_clean):
            raise ValueError(Constants.INVALID_PLATE_FORMAT.format(plate=self.plate))
        if self.km < 0:
            raise ValueError(Constants.KM_CANNOT_BE_NEGATIVE)
        if self.fuel_level < 0:
            raise ValueError(Constants.FUEL_LEVEL_CANNOT_BE_NEGATIVE)
