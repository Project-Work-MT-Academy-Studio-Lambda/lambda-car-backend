from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ...commands.trip_commands import (
    OpenTripCommand,
    UpdateTripCommand,
    CloseTripCommand,
    DeleteTripCommand
)
from ...dependencies import get_trip_service, require_user
from ...schemas.trip_schemas import (
    OpenTripRequest,
    UpdateTripRequest,
    CloseTripRequest,
    TripResponse,
)
from ...services.trip_service import TripService

from ...logger import get_logger

from ...domain.user import CurrentUser

router = APIRouter(prefix="/trips", tags=["trips"])
logger = get_logger(__name__)



@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def open_trip(
    payload: OpenTripRequest,
    current_user: CurrentUser = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    logger.debug(f"User {current_user.id} is attempting to open a trip with car_id: {payload.car_id} and commit_id: {payload.commit_id}")
    try:
        cmd = OpenTripCommand(
            user_id=current_user.id,
            car_id=payload.car_id,
            start_position=payload.start_position,
            start_date=payload.start_date,
            start_km=payload.start_km,
        )
        logger.debug(f"OpenTripCommand created successfully {cmd}")
        trip = service.open_trip(cmd)
        return TripResponse.from_domain(trip)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[TripResponse])
def list_my_trips(
    current_user: CurrentUser = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    trips = service.get_trips_for_user(current_user.id)
    return [TripResponse.from_domain(trip) for trip in trips]


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: UUID,
    current_user: CurrentUser = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)
        logger.debug(f"User {current_user.id} is attempting to access trip {trip_id} with user_id {trip.user_id}")
        logger.debug(trip.user_id == current_user.id)
        if str(trip.user_id) != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access this trip",
            )

        return TripResponse.from_domain(trip)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: UUID,
    payload: UpdateTripRequest,
    current_user: CurrentUser = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if str(trip.user_id) != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update this trip",
            )

        cmd = UpdateTripCommand(
            trip_id=trip_id,
            user_id=current_user.id,
            car_id=payload.car_id,
            start_position=payload.start_position,
            start_date=payload.start_date,
            start_km=payload.start_km,
            end_position=payload.end_position,
            end_date=payload.end_date,
            end_km=payload.end_km,
        )

        updated_trip = service.update_trip(cmd)
        return TripResponse.from_domain(updated_trip)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{trip_id}/close", response_model=TripResponse)
def close_trip(
    trip_id: UUID,
    payload: CloseTripRequest,
    current_user: CurrentUser = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if str(trip.user_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot close this trip",
            )

        cmd = CloseTripCommand(
            user_id=current_user.id,
            trip_id=trip_id,
            end_position=payload.end_position,
            end_date=payload.end_date,
            end_km=payload.end_km,
        )

        closed_trip = service.close_trip(cmd)
        return TripResponse.from_domain(closed_trip)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: UUID,
    current_user: CurrentUser = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if str(trip.user_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot delete this trip",
            )
        cmd = DeleteTripCommand(
            trip_id=trip_id,
            user_id=current_user.id
        )
        service.delete_trip(cmd=cmd)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))