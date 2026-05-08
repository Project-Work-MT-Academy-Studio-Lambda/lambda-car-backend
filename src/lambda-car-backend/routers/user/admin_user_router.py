from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ...commands.user_commands import (
    CreateUserCommand, 
    UpdateUserCommand,
    ChangePasswordCommand
)

from ...dependencies import (
    get_user_service,
    require_admin
)
from ...schemas.user_schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    ChangePasswordRequest
)
from ...services.user_service import UserService
from ...logger import get_logger

from ...domain.user import CurrentUser

router = APIRouter(prefix="/admin/users", tags=["admin-users"])

logger = get_logger(__name__)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: CreateUserRequest,
    current_user: CurrentUser = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    try:
        cmd = CreateUserCommand(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            role=payload.role,
        )
        user = service.create_user(cmd)
        return UserResponse.from_domain(user)
    except ValueError as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.get_user(user_id)
        return UserResponse.from_domain(user)
    except ValueError as e:
        logger.warning(f"Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    payload: UpdateUserRequest,
    current_user: CurrentUser = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    try:
        cmd = UpdateUserCommand(
            user_id=user_id,
            name=payload.name,
            email=payload.email
        )
        user = service.update_user(cmd)
        return UserResponse.from_domain(user)
    except ValueError as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{user_id}/password", status_code=204)
def change_user_password(
    user_id: UUID,
    payload: ChangePasswordRequest,
    current_user: CurrentUser = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    logger.debug(f"Attempting to change password for user_id: {user_id}")
    try:
        cmd = ChangePasswordCommand(
            user_id=user_id,
            new_password=payload.new_password,
        )
        user = service.get_user(user_id)
        service.change_password(cmd)
        logger.debug(f"Password change successful for user_id: {user_id}")
    except ValueError as e:
        logger.error(f"Error changing user password: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))