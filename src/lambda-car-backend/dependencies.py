from infrastructure.dynamodb.tables import DynamoDbTables
from infrastructure.dynamodb.repositories.dynamodb_user_repository import DynamoDbUserRepository
from infrastructure.dynamodb.repositories.dynamodb_car_repository import DynamoDbCarRepository
from infrastructure.dynamodb.repositories.dynamodb_trip_repository import DynamoDbTripRepository
from infrastructure.dynamodb.repositories.dynamodb_refueling_repository import DynamoDbRefuelingRepository
from infrastructure.dynamodb.repositories.dynamodb_commit_repository import DynamoDbCommitRepository

from services.user_service import UserService
from services.trip_service import TripService
from services.car_service import CarService
from services.refueling_service import RefuelingService
from services.commit_service import CommitService
from services.auth_service import AuthService

from security.password_hasher import ArgonPasswordHasher
from security.token_service import TokenService
from constants import Constants
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer


_tables = DynamoDbTables()
_password_hasher = ArgonPasswordHasher()
_secret = os.getenv(Constants.JWT_SECRET, Constants.DEV_SECRET)
_token_service = TokenService(secret=_secret)

_user_repository = DynamoDbUserRepository(_tables.user_table)
_car_repository = DynamoDbCarRepository(_tables.car_table)
_trip_repository = DynamoDbTripRepository(_tables.trip_table)
_refueling_repository = DynamoDbRefuelingRepository(_tables.refueling_table)
_commit_repository = DynamoDbCommitRepository(_tables.commit_table)

security = HTTPBearer()

def get_auth_service() -> AuthService:
    return AuthService(
        user_repository=_user_repository,
        password_hasher=_password_hasher,
        token_service=_token_service,
    )

def get_user_service() -> UserService:
    return UserService(
        user_repository=_user_repository,
        password_hasher=_password_hasher,
    )

def get_current_user(
    credentials=Depends(security),
):
    try:
        user_id = _token_service.verify_token(credentials.credentials)
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail=Constants.INVALID_TOKEN)

def get_current_token_payload(credentials=Depends(security)):
    try:
        return _token_service.verify_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Constants.INVALID_TOKEN,
        )

def require_user(payload=Depends(get_current_token_payload)):
    if payload.get(Constants.ROLE) not in Constants.SUPPORTED_BASE_API_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=Constants.INVALID_CREDENTIALS,
        )
    return payload[Constants.SUB]


def require_admin(payload=Depends(get_current_token_payload)):
    if payload.get(Constants.ROLE) != Constants.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=Constants.INVALID_CREDENTIALS,
        )
    return payload[Constants.SUB]

def get_car_service() -> CarService:
    return CarService(
        car_repository=_car_repository,
    )


def get_trip_service() -> TripService:
    return TripService(
        trip_repository=_trip_repository,
        car_repository=_car_repository,
        user_repository=_user_repository,
        commit_repository=_commit_repository,
        refueling_repository=_refueling_repository,
    )


def get_refueling_service() -> RefuelingService:
    return RefuelingService(
        refueling_repository=_refueling_repository,
        trip_repository=_trip_repository,
    )


def get_commit_service() -> CommitService:
    return CommitService(
        commit_repository=_commit_repository,
        trip_repository=_trip_repository,
    )