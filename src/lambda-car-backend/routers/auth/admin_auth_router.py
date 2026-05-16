from fastapi import APIRouter, Depends, HTTPException, Response, status

from ...schemas.auth_schemas import AuthUserResponse, LoginRequest, TokenResponse
from ...commands.auth_commands import LoginCommand
from ...services.auth_service import AuthService
from ...dependencies import get_auth_service
from ...settings import load_settings

from ...constants import Constants

from ...logger import get_logger


router = APIRouter(prefix="/admin/auth", tags=["admin-auth"])
logger = get_logger(__name__)
settings = load_settings()

@router.post("/login", response_model=TokenResponse)
def admin_login(
    payload: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    try:
        cmd = LoginCommand(
            email=payload.email,
            password=payload.password,
        )
        access_token, user = service.login_session(cmd)
        response.set_cookie(
            key=settings.session_cookie_name,
            value=access_token,
            max_age=settings.jwt_expiration_minutes * 60,
            expires=settings.jwt_expiration_minutes * 60,
            httponly=True,
            secure=settings.session_cookie_secure,
            samesite=settings.session_cookie_samesite,
            path="/",
        )
        logger.info(f"Login successful for email: {payload.email}")
        return TokenResponse(
            access_token=access_token,
            token_type=Constants.BEARER,
            user=AuthUserResponse(
                id=str(user.id),
                name=user.name,
                email=user.email,
                role=user.role.value if hasattr(user.role, "value") else user.role,
            ),
        )

    except ValueError as e:
        logger.warning(f"Login failed for email {payload.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Constants.INVALID_CREDENTIALS,
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def admin_logout(response: Response):
    response.delete_cookie(
        key=settings.session_cookie_name,
        path="/",
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=settings.session_cookie_samesite,
    )
