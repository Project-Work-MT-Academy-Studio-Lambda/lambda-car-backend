from pydantic import BaseModel, EmailStr
from ..constants import Constants


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthUserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Constants.BEARER
    user: AuthUserResponse
