from fastapi import APIRouter, Depends, HTTPException, status

from schemas.auth_schemas import LoginRequest, TokenResponse
from commands.auth_commands import LoginCommand
from services.auth_service import AuthService
from dependencies import get_auth_service

from constants import Constants


router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])


@router.post("/login", response_model=TokenResponse)
def admin_login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        cmd = LoginCommand(
            email=payload.email,
            password=payload.password,
        )
        access_token = service.login_admin(cmd)

        return TokenResponse(access_token=access_token, token_type=Constants.BEARER)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Constants.INVALID_CREDENTIALS,
        )