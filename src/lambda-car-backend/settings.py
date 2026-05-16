import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str
    api_prefix: str
    jwt_secret: str
    jwt_expiration_minutes: int
    log_level: str
    cors_allowed_origins: list[str]
    session_cookie_name: str
    session_cookie_secure: bool
    session_cookie_samesite: str


def load_settings() -> Settings:
    app_env = os.getenv("APP_ENV", "dev")
    default_origins = "http://localhost:5173,http://127.0.0.1:5173"
    cors_allowed_origins = [
        origin.strip()
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", default_origins).split(",")
        if origin.strip()
    ]

    return Settings(
        app_env=app_env,
        api_prefix=os.getenv("API_PREFIX", "/api/v1/lambdacar"),
        jwt_secret=os.getenv("JWT_SECRET", "dev-secret"),
        jwt_expiration_minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", "120")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        cors_allowed_origins=cors_allowed_origins,
        session_cookie_name=os.getenv("SESSION_COOKIE_NAME", "lambda_car_session"),
        session_cookie_secure=os.getenv("SESSION_COOKIE_SECURE", str(app_env != "dev")).lower() == "true",
        session_cookie_samesite=os.getenv("SESSION_COOKIE_SAMESITE", "lax"),
    )
