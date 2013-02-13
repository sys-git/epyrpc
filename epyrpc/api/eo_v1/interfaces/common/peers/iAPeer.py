
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData

class iAPeer(iApiData):
    def macAddress(self):
        r"""
        @summary: Get the macAddress.
        """
        raise NotImplementedException("iAPeer.macAddress")
