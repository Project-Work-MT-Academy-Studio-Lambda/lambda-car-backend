# routes/trip/trip_router.py

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from commands.trip_commands import (
    OpenTripCommand,
    UpdateTripCommand,
    CloseTripCommand,
)
from dependencies import get_trip_service, require_user
from schemas.trip_schemas import (
    OpenTripRequest,
    UpdateTripRequest,
    CloseTripRequest,
    TripResponse,
)
from services.trip_service import TripService


router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def open_trip(
    payload: OpenTripRequest,
    current_user_id: UUID = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        cmd = OpenTripCommand(
            user_id=current_user_id,
            car_id=payload.car_id,
            start_position=payload.start_position,
            start_date=payload.start_date,
            start_km=payload.start_km,
        )

        trip = service.open_trip(cmd)
        return TripResponse.from_domain(trip)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[TripResponse])
def list_my_trips(
    current_user_id: UUID = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    trips = service.get_trips_for_user(current_user_id)
    return [TripResponse.from_domain(trip) for trip in trips]


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: UUID,
    current_user_id: UUID = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if trip.user_id != current_user_id:
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
    current_user_id: UUID = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if trip.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update this trip",
            )

        cmd = UpdateTripCommand(
            trip_id=trip_id,
            user_id=current_user_id,
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
    current_user_id: UUID = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if trip.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot close this trip",
            )

        cmd = CloseTripCommand(
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
    current_user_id: UUID = Depends(require_user),
    service: TripService = Depends(get_trip_service),
):
    try:
        trip = service.get_trip(trip_id)

        if trip.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot delete this trip",
            )

        service.delete_trip(trip_id)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))