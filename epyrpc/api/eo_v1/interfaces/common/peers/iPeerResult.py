
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iPeerResult(iApiData):
    def peers(self):
        r"""
        @summary: Get the dict of APeer's
        @return: type={APeer}
        """
        raise NotImplementedException("iPeerResult.peers")
    def count(self):
        r"""
        @summary: Get the number of Peers.
        @return: type=int
        """
        raise NotImplementedException("iPeerResult.count")
