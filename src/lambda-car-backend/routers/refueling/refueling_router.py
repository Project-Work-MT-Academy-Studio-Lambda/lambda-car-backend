from uuid import UUID
from datetime import datetime

from fastapi import (
    APIRouter, 
    Depends,
    HTTPException, 
    status,
    Form,
    UploadFile,
    File
)

from ...commands.refueling_commands import (
    CreateRefuelingCommand,
    UpdateRefuelingCommand,
)
from ...dependencies import get_refueling_service, require_user
from ...schemas.refueling_schemas import (
    CreateRefuelingRequest,
    UpdateRefuelingRequest,
    RefuelingResponse,
)
from ...services.refueling_service import RefuelingService

from ...domain.user import CurrentUser

from decimal import Decimal

from ...logger import get_logger


router = APIRouter(prefix="/refuelings", tags=["refuelings"])

logger = get_logger(__name__)

@router.get("/car/{car_id}", response_model=list[RefuelingResponse], status_code=status.HTTP_200_OK)
def list_refuelings(
    car_id: UUID,
    current_user: CurrentUser = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    logger.debug(f"User {current_user.id} is listing all refuelings")
    try:
        refuelings = service.get_refuelings_for_car(car_id=car_id)
        logger.debug(f"Found {len(refuelings)} refuelings for car {car_id}")
        return [RefuelingResponse.from_domain(refueling) for refueling in refuelings]
    except ValueError as e:
        logger.error(f"Error occurred while fetching refuelings: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=RefuelingResponse, status_code=status.HTTP_201_CREATED)
async def create_refueling(
    car_id: UUID = Form(...),
    liters: Decimal = Form(...),
    liter_price: Decimal = Form(...),
    date: datetime = Form(...),
    receipt_photo: UploadFile = File(...),
    card_number: str | None = Form(None),
    current_user: CurrentUser = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        content = await receipt_photo.read()

        cmd = CreateRefuelingCommand(
            car_id=car_id,
            liters=liters,
            liter_price=liter_price,
            date=date,
            card_number=card_number,
            receipt_filename=receipt_photo.filename,
            receipt_content=content,
            receipt_content_type=receipt_photo.content_type,
            user_id=current_user.id,
            user_role=current_user.role,
        )

        refueling = service.create_refueling(
            cmd=cmd,
        )

        return RefuelingResponse.from_domain(refueling)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{refueling_id}", response_model=RefuelingResponse)
def get_refueling(
    refueling_id: UUID,
    current_user: CurrentUser = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        refueling = service.get_refueling(
            refueling_id=refueling_id,
            user_id=current_user.id,
            user_role=current_user.role,
        )

        logger.debug(f"User {current_user.id} is attempting to access refueling {refueling_id}")

        return RefuelingResponse.from_domain(refueling)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/car/{car_id}", response_model=list[RefuelingResponse])
def list_refuelings_for_car(
    car_id: UUID,
    current_user: CurrentUser = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        refuelings = service.get_refuelings_for_car(
            car_id=car_id,
            user_id=current_user.id,
            user_role=current_user.role,
        )

        return [RefuelingResponse.from_domain(refueling) for refueling in refuelings]

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{refueling_id}", response_model=RefuelingResponse)
def update_refueling(
    refueling_id: UUID,
    payload: UpdateRefuelingRequest,
    current_user: CurrentUser = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        cmd = UpdateRefuelingCommand(
            refueling_id=refueling_id,
            liters=payload.liters,
            liter_price=payload.liter_price,
            date=payload.date,
            card_number=payload.card_number,
            user_id=current_user.id,
            user_role=current_user.role,
            car_id=payload.car_id
        )

        refueling = service.update_refueling(
            cmd=cmd,
        )

        return RefuelingResponse.from_domain(refueling)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{refueling_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_refueling(
    refueling_id: UUID,
    current_user: CurrentUser = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        service.delete_refueling(
            refueling_id=refueling_id,
            user_id=current_user.id,
            user_role=current_user.role,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))