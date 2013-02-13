
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iTransportDetails(Interface):
    def getType(self):
        r"""
        @see: eIpcTransportType
        """
        raise NotImplementedException("iTransportDetails.getType")
    def invert(self):
        r"""
        @return: Return an inverted COPY of the details (head becomes neck etc).
        """
        raise NotImplementedException("iTransportDetails.invert")
    def packager(self):
        r"""
        @return: Return packager details.
        """
        raise NotImplementedException("iTransportDetails.packager")
