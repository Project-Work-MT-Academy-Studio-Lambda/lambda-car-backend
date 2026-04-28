from enum import Enum
from constants import Constants

class RefuelingType(str, Enum):
    GASOLINE = Constants.GASOLINE
    DIESEL = Constants.DIESEL
    ADBLUE = Constants.ADBLUE
    GPL = Constants.GPL
    METHANE = Constants.METHANE
    ELECTRIC = Constants.ELECTRIC