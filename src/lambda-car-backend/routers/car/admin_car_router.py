# routes/car/admin_car_router.py

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from commands.car_commands import CreateCarCommand, UpdateCarCommand
from dependencies import get_car_service, require_admin
from schemas.car_schemas import CreateCarRequest, UpdateCarRequest, CarResponse
from services.car_service import CarService


router = APIRouter(prefix="/admin/cars", tags=["admin-cars"])


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(
    payload: CreateCarRequest,
    admin_id: UUID = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    try:
        cmd = CreateCarCommand(
            plate=payload.plate,
            model=payload.model,
            km_total=payload.mileage.km_total,
            km_servicing=payload.mileage.km_servicing,
            km_wheels=payload.mileage.km_wheels,
            fuel_type=payload.fuel_info.type,
            fuel_level=payload.fuel_info.level,
            fuel_card=payload.fuel_info.card,
        )
        car = service.create_car(cmd)
        return CarResponse.from_domain(car)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{car_id}", response_model=CarResponse)
def get_car(
    car_id: UUID,
    admin_id: UUID = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    try:
        car = service.get_car(car_id)
        return CarResponse.from_domain(car)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{car_id}", response_model=CarResponse)
def update_car(
    car_id: UUID,
    payload: UpdateCarRequest,
    admin_id: UUID = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    try:
        cmd = UpdateCarCommand(
            car_id=car_id,
            plate=payload.plate,
            model=payload.model,
            km_total=payload.mileage.km_total,
            km_servicing=payload.mileage.km_servicing,
            km_wheels=payload.mileage.km_wheels,
            fuel_type=payload.fuel_info.type,
            fuel_level=payload.fuel_info.level,
            fuel_card=payload.fuel_info.card,
        )
        car = service.update_car(cmd)
        return CarResponse.from_domain(car)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: UUID,
    admin_id: UUID = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    try:
        service.delete_car(car_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))