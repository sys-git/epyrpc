
from epyrpc.utils.Enum import Enum

class eIpcTransportState(Enum):
    OPEN = 1
    CLOSED = 0
    DISCONNECTED = -1
eIpcTransportState()
