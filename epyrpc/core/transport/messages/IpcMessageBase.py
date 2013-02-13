
from epyrpc.utils.Interfaces import Interface

class IpcMessageBase(Interface):
    r"""
    @summary: The base-class for all messages flowing over the ipc.
    """
    def __init__(self, tId=None):
        self._tId = tId
    def getTid(self):
        return self._tId
    def setTid(self, tId):
        self._tId = tId
    tId = property(getTid, setTid)
