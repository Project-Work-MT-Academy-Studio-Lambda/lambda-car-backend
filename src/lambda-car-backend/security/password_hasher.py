from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

class ArgonPasswordHasher:
    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self._hasher.verify(hashed_password, plain_password)
        except (VerifyMismatchError, InvalidHashError):
            return False

    def needs_rehash(self, hashed_password: str) -> bool:
        return self._hasher.check_needs_rehash(hashed_password)