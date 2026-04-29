import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str
    api_prefix: str
    jwt_secret: str
    jwt_expiration_minutes: int


def load_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "dev"),
        api_prefix=os.getenv("API_PREFIX", "/api/v1/lambdacar"),
        jwt_secret=os.getenv("JWT_SECRET", "dev-secret"),
        jwt_expiration_minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", "120")),
    )