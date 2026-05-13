from ..repositories.user_repository import UserRepository
from ..security.password_hasher import PasswordHasher
from ..security.token_service import TokenService
from ..commands.auth_commands import LoginCommand
from ..constants import Constants
from ..domain.enum.role import Role
from ..logger import get_logger


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
        self.logger = get_logger(__name__)

    def login(self, cmd: LoginCommand) -> str:
        user = self._authenticate(cmd)

        if user.role not in Constants.SUPPORTED_BASE_API_ROLES:
            raise ValueError(Constants.INVALID_CREDENTIALS)

        return self.token_service.create_token(str(user.id), user.role)

    def _authenticate(self, cmd: LoginCommand):
        self.logger.debug(f"Authenticating user with email: {cmd.email}")
        user = self.user_repository.get_by_email(cmd.email)
        self.logger.debug(f"User found: {user is not None}")
        if user is None:
            self.logger.warning(f"User not found for email: {cmd.email}")
            raise ValueError(Constants.INVALID_CREDENTIALS)
        self.logger.debug(f"Verifying password for user with email: {cmd.email}")
        self.logger.debug(f"Hashed password: {user.hashed_password}, Provided password: {cmd.password}")
        if not self.password_hasher.verify(cmd.password, user.hashed_password):
            self.logger.warning(f"Invalid password for email: {cmd.email}")
            raise ValueError(Constants.INVALID_CREDENTIALS)

        return user