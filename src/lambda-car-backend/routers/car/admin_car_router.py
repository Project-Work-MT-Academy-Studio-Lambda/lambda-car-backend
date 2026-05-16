from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ...commands.car_commands import CreateCarCommand, UpdateCarCommand
from ...dependencies import get_car_service, require_admin
from ...schemas.car_schemas import CreateCarRequest, UpdateCarRequest, CarResponse
from ...services.car_service import CarService
from ...logger import get_logger

from ...domain.user import CurrentUser


router = APIRouter(prefix="/admin/cars", tags=["admin-cars"])
logger = get_logger(__name__)

@router.get("", response_model=list[CarResponse], status_code=status.HTTP_200_OK)
@router.get("/", response_model=list[CarResponse], status_code=status.HTTP_200_OK, include_in_schema=False)
def list_cars(
    current_user: CurrentUser = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    logger.debug(f"Admin {current_user.id} is listing all cars")
    cars = service.find_all_cars()
    logger.debug(f"Found {len(cars)} cars in the system")
    return [CarResponse.from_domain(car) for car in cars]

@router.get("/active", response_model=list[CarResponse], status_code=status.HTTP_200_OK)
def get_active_cars(
    current_user: CurrentUser = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    logger.debug(f"User {current_user.id} is attempting to get the active cars")
    try:
        cars = service.get_active_cars()
        logger.debug(f"Found {len(cars)} active cars")
        return [CarResponse.from_domain(car) for car in cars]
    except ValueError as e:
        logger.error(f"Error occurred while fetching active car: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(
    payload: CreateCarRequest,
    current_user: CurrentUser = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    logger.debug(f"Admin {current_user.id} is attempting to create a car with plate: {payload.plate}")
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
            status=payload.status,
        )
        logger.debug(f"CreateCarCommand created successfully for plate: {payload.plate}")
        car = service.create_car(cmd)
        logger.debug(f"Car created successfully with plate: {car.plate}")
        return CarResponse.from_domain(car)
    except ValueError as e:
        logger.error(f"Error creating car: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{car_id}", response_model=CarResponse)
def get_car(
    car_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
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
    current_user: CurrentUser = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    logger.debug(f"Admin {current_user.id} is attempting to update car with ID: {car_id}")
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
            status=payload.status,
        )
        car = service.update_car(cmd)
        logger.debug(f"Admin {current_user.id} successfully updated car with ID: {car_id}")
        return CarResponse.from_domain(car)
    except ValueError as e:
        logger.error(f"Error updating car: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
    service: CarService = Depends(get_car_service),
):
    try:
        service.delete_car(car_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
