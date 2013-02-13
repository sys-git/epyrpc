
from epyrpc.utils.Enum import Enum

class eApiType(Enum):
    r"""
    The 'type' of API is used in API object creation.
    """
    EO_V1 = "EO_V1"
    EO_V1__HANDLER = "EO_V1__HANDLER"
    UNSUPPORTED = "UNSUPPORTED"
eApiType()
