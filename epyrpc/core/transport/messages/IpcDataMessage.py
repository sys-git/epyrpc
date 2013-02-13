
from epyrpc.core.transport.messages.IpcMessageBase import IpcMessageBase

class IpcDataMessage(IpcMessageBase):
    r"""
    @summary: All content (non-transport) related messages ride in this car.
    """
    def __init__(self, message, tId=None):
        super(IpcDataMessage, self).__init__(tId)
        self._message = message
    def message(self):
        return self._message
    def __str__(self):
        s = ["IpcDataMessage[%(TID)s]" % {"TID":self.tId}]
        s.append("%(M)s" % {"M":self._message})
        return " ".join(s)
