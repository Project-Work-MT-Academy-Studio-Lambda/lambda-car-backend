from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies import get_car_service, require_user
from ...schemas.car_schemas import CarResponse
from ...services.car_service import CarService
from ...logger import get_logger

from ...domain.user import CurrentUser

router = APIRouter(prefix="/cars", tags=["cars"])
logger = get_logger(__name__)

@router.get("/active", response_model=CarResponse)
def get_active_car(
    current_user: CurrentUser = Depends(require_user),
    service: CarService = Depends(get_car_service),
):
    logger.debug(f"User {current_user.id} is attempting to get the active car")
    try:
        car = service.get_active_car()
        return CarResponse.from_domain(car)
    except ValueError as e:
        logger.error(f"Error occurred while fetching active car: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))