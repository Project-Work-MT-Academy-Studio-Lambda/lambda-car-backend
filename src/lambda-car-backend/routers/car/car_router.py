from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies import get_car_service, require_user
from ...schemas.car_schemas import CarResponse
from ...services.car_service import CarService
from ...logger import get_logger

from ...domain.user import CurrentUser

router = APIRouter(prefix="/cars", tags=["cars"])
logger = get_logger(__name__)

@router.get("/active", response_model=list[CarResponse], status_code=status.HTTP_200_OK)
def get_active_cars(
    current_user: CurrentUser = Depends(require_user),
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