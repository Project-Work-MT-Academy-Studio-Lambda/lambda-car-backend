from dataclasses import dataclass
from uuid import UUID
from constants import Constants
from domain.enum.refueling_type import RefuelingType

@dataclass
class FuelInfo:
    id: UUID
    level: int | None = None
    type: RefuelingType
    card: str | None = None

    def __post_init__(self):
        if self.level is not None and self.level < 0:
            raise ValueError(Constants.FUEL_LEVEL_CANNOT_BE_NEGATIVE)
        if self.card is not None and not self.card.strip():
            raise ValueError(Constants.FUEL_CARD_CANNOT_BE_EMPTY)
