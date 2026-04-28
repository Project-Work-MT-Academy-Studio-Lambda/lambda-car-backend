from pydantic import BaseModel, EmailStr
from constants import Constants


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Constants.BEARER