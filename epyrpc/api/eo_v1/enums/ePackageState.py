
from epyrpc.utils.Enum import Enum

class ePackageState(Enum):
    FAILED = -1
    MOVING = 1
    ZIPPING = 2
    COMPLETE = 3

ePackageState()
