from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ...logger import get_logger
from ...dependencies import require_admin, get_maintenance_service
from ...services.maintenance_service import MaintenanceService
from ...schemas.maintenance_schemas import (
    MaintenanceResponse,
    CreateMaintenanceRequest,
    UpdateMaintenanceRequest,
)
from ...commands.maintenance_commands import (
    CreateMaintenanceCommand,
    UpdateMaintenanceCommand,
)
from ...domain.user import CurrentUser
from ...domain.errors import ApplicationError

router = APIRouter(prefix="/admin/maintenances", tags=["admin-maintenances"])
logger = get_logger(__name__)

@router.get("/", response_model=list[MaintenanceResponse], status_code=status.HTTP_200_OK)
def list_maintenances(
    current_user: CurrentUser = Depends(require_admin),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    logger.debug(f"Admin {current_user.id} is listing all maintenances")
    maintenances = service.find_all_maintenances()
    logger.debug(f"Found {len(maintenances)} maintenances in the system")
    return [MaintenanceResponse.from_domain(maintenance) for maintenance in maintenances]


@router.get("/car/{car_id}", response_model=list[MaintenanceResponse], status_code=status.HTTP_200_OK)
def list_maintenances_for_car(
    car_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    logger.debug(f"Admin {current_user.id} is listing maintenances for car with ID: {car_id}")
    try:
        maintenances = service.get_maintenances_for_car(car_id)
        logger.debug(f"Found {len(maintenances)} maintenances for car with ID: {car_id}")
        return [MaintenanceResponse.from_domain(maintenance) for maintenance in maintenances]
    except ValueError as e:
        logger.error(f"Error occurred while fetching maintenances for car {car_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    payload: CreateMaintenanceRequest,
    current_user: CurrentUser = Depends(require_admin),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    logger.debug(f"Admin {current_user.id} is attempting to create a maintenance for car with ID: {payload.car_id}")
    try:
        cmd = CreateMaintenanceCommand(
            car_id=payload.car_id,
            description=payload.description,
            date=payload.date,
            km_at_maintenance=payload.km_at_maintenance,
            cost=payload.cost,
            type=payload.type,
        )
        maintenance = service.create_maintenance(cmd)
        logger.debug(f"Admin {current_user.id} successfully created maintenance with ID: {maintenance.id}")
        return MaintenanceResponse.from_domain(maintenance)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except ValueError as e:
        logger.error(f"Error creating maintenance: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(
    maintenance_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    logger.debug(f"Admin {current_user.id} is attempting to retrieve maintenance with ID: {maintenance_id}")
    try:
        maintenance = service.get_maintenance(maintenance_id)
        logger.debug(f"Admin {current_user.id} successfully retrieved maintenance with ID: {maintenance_id}")
        return MaintenanceResponse.from_domain(maintenance)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(
    maintenance_id: UUID,
    payload: UpdateMaintenanceRequest,
    current_user: CurrentUser = Depends(require_admin),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    logger.debug(f"Admin {current_user.id} is attempting to update maintenance with ID: {maintenance_id}")
    try:
        cmd = UpdateMaintenanceCommand(
            maintenance_id=maintenance_id,
            car_id=payload.car_id,
            description=payload.description,
            date=payload.date,
            km_at_maintenance=payload.km_at_maintenance,
            cost=payload.cost,
            type=payload.type,
        )
        maintenance = service.update_maintenance(cmd)
        logger.debug(f"Admin {current_user.id} successfully updated maintenance with ID: {maintenance_id}")
        return MaintenanceResponse.from_domain(maintenance)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except ValueError as e:
        logger.error(f"Error updating maintenance: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance(
    maintenance_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
    service: MaintenanceService = Depends(get_maintenance_service),
):
    logger.debug(f"Admin {current_user.id} is attempting to delete maintenance with ID: {maintenance_id}")
    try:
        service.delete_maintenance(maintenance_id)
        logger.debug(f"Admin {current_user.id} successfully deleted maintenance with ID: {maintenance_id}")
    except ValueError as e:
        logger.error(f"Error deleting maintenance: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
