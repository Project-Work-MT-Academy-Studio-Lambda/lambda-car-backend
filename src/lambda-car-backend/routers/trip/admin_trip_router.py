from fastapi import APIRouter, Depends, status

from ...dependencies import get_trip_service, require_admin
from ...domain.user import CurrentUser
from ...logger import get_logger
from ...schemas.trip_schemas import TripResponse
from ...services.trip_service import TripService


router = APIRouter(prefix="/admin/trips", tags=["admin-trips"])
logger = get_logger(__name__)


def _trip_response_with_car(service: TripService, trip) -> TripResponse:
    try:
        car = service.get_car_for_trip(trip.id)
    except ValueError:
        car = None
    return TripResponse.from_domain(trip, car=car)


@router.get("/", response_model=list[TripResponse], status_code=status.HTTP_200_OK)
def list_trips(
    current_user: CurrentUser = Depends(require_admin),
    service: TripService = Depends(get_trip_service),
):
    logger.debug(f"Admin {current_user.id} is listing all trips")
    trips = service.find_all_trips()
    logger.debug(f"Found {len(trips)} trips in the system")
    return [_trip_response_with_car(service, trip) for trip in trips]
