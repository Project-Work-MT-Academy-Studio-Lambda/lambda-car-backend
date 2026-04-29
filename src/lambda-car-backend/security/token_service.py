import jwt
from datetime import (
    datetime,
    timedelta,
    timezone
)

class TokenService:
    def __init__(self, secret: str, expiration_minutes: int):
        self.secret = secret
        self.expiration_minutes = expiration_minutes

    def create_token(self, user_id: str, role: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expiration_minutes),
            "role": role
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        return payload