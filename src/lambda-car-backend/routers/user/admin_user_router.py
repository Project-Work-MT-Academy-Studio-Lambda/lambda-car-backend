from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from commands.user_commands import (
    CreateUserCommand, 
    UpdateUserCommand,
    ChangePasswordCommand
)

from dependencies import (
    get_user_service,
    require_admin
)
from schemas.user_schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    ChangePasswordRequest
)
from services.user_service import UserService


router = APIRouter(prefix="/admin/users", tags=["admin-users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: CreateUserRequest,
    admin_id: UUID = Depends(require_admin),
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    admin_id: UUID = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.get_user(user_id)
        return UserResponse.from_domain(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    payload: UpdateUserRequest,
    admin_id: UUID = Depends(require_admin),
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    admin_id: UUID = Depends(require_admin),
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
    admin_id: UUID = Depends(require_admin),
    service: UserService = Depends(get_user_service),
):
    try:
        cmd = ChangePasswordCommand(
            user_id=user_id,
            new_password=payload.new_password,
        )
        service.change_password(cmd)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))