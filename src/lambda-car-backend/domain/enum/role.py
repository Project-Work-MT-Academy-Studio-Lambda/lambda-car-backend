from enum import Enum
from constants import Constants

class Role(str, Enum):
    ADMIN = Constants.ADMIN
    USER = Constants.USER