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

from decimal import Decimal


router = APIRouter(prefix="/refuelings", tags=["refuelings"])


@router.post("/", response_model=RefuelingResponse, status_code=status.HTTP_201_CREATED)
async def create_refueling(
    car_id: UUID = Form(...),
    liters: Decimal = Form(...),
    liter_price: Decimal = Form(...),
    date: datetime = Form(...),
    receipt_photo: UploadFile = File(...),
    card_number: str | None = Form(None),
    current_user_id: UUID = Depends(require_user),
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
            receipt_content_type=receipt_photo.content_type
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
    current_user_id: UUID = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        refueling = service.get_refueling(
            refueling_id=refueling_id,
            user_id=current_user_id,
        )

        return RefuelingResponse.from_domain(refueling)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/car/{car_id}", response_model=list[RefuelingResponse])
def list_refuelings_for_car(
    car_id: UUID,
    current_user_id: UUID = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        refuelings = service.get_refuelings_for_car(
            car_id=car_id,
            user_id=current_user_id,
        )

        return [RefuelingResponse.from_domain(refueling) for refueling in refuelings]

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{refueling_id}", response_model=RefuelingResponse)
def update_refueling(
    refueling_id: UUID,
    payload: UpdateRefuelingRequest,
    current_user_id: UUID = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        cmd = UpdateRefuelingCommand(
            refueling_id=refueling_id,
            liters=payload.liters,
            price=payload.price,
            date=payload.date,
        )

        refueling = service.update_refueling(
            cmd=cmd,
            user_id=current_user_id,
        )

        return RefuelingResponse.from_domain(refueling)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{refueling_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_refueling(
    refueling_id: UUID,
    current_user_id: UUID = Depends(require_user),
    service: RefuelingService = Depends(get_refueling_service),
):
    try:
        service.delete_refueling(
            refueling_id=refueling_id,
            user_id=current_user_id,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))