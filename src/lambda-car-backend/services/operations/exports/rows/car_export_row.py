from dataclasses import dataclass


@dataclass(frozen=True)
class CarExportRow:
    plate: str
    model: str | None
    km_total: int
    km_servicing: int
    km_wheels: int
    fuel_type: str
    fuel_level: int | None
    fuel_card: str | None