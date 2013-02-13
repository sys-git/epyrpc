
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iLocation(Interface):
    FILE = "file"
    MEMORY = "memory"
    def details(self):
        r"""
        @summary: Retrieve the details where/how ths signals are stored.
        """
        raise NotImplementedException("iLocation.details")
    def theFormat(self):
        r"""
        @summary: Retrieve the format of the stored signals.
        """
        raise NotImplementedException("iLocation.theFormat")
    def copyExisting(self):
        r"""
        @summary: Copy any existing stored signals into the new store.
        """
        raise NotImplementedException("iLocation.copyExisting")
    def removeExisting(self):
        r"""
        @summary: Remove any existing store.
        """
        raise NotImplementedException("iLocation.removeExisting")
