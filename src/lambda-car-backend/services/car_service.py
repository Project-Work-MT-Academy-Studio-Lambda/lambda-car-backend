from uuid import UUID, uuid4
from commands.car_commands import CreateCarCommand, UpdateCarCommand
from constants import Constants
from domain.car import Car, Mileage, FuelInfo
from repositories.car_repository import CarRepository


class CarService:
    def __init__(self, car_repository: CarRepository):
        self.car_repository = car_repository

    def create_car(self, cmd: CreateCarCommand) -> Car:
        existing_car = self.car_repository.get_by_plate(cmd.plate)
        if existing_car is not None:
            raise ValueError(Constants.CAR_ALREADY_EXISTS)

        car = Car(
            id=uuid4(),
            plate=cmd.plate,
            model=cmd.model,
            mileage=Mileage(
                km_total=cmd.km_total,
                km_servicing=cmd.km_servicing,
                km_wheels=cmd.km_wheels,
            ),
            fuel_info=FuelInfo(
                fuel_type=cmd.fuel_type,
                fuel_level=cmd.fuel_level,
                fuel_card=cmd.fuel_card,
            ),
        )

        self.car_repository.save(car)
        return car

    def get_car(self, car_id: UUID) -> Car:
        car = self.car_repository.get_by_id(car_id)
        if car is None:
            raise ValueError(Constants.CAR_NOT_FOUND)
        return car

    def update_car(self, cmd: UpdateCarCommand) -> Car:
        car = self.get_car(cmd.car_id)

        existing_car = self.car_repository.get_by_plate(cmd.plate)
        if existing_car is not None and existing_car.id != cmd.car_id:
            raise ValueError(Constants.CAR_ALREADY_EXISTS)

        car.plate = cmd.plate
        car.model = cmd.model
        car.mileage = Mileage(
            km_total=cmd.km_total,
            km_servicing=cmd.km_servicing,
            km_wheels=cmd.km_wheels,
        )
        car.fuel_info = FuelInfo(
            fuel_type=cmd.fuel_type,
            fuel_level=cmd.fuel_level,
            fuel_card=cmd.fuel_card,
        )

        self.car_repository.save(car)
        return car

    def delete_car(self, car_id: UUID) -> None:
        self.get_car(car_id)
        self.car_repository.delete(car_id)