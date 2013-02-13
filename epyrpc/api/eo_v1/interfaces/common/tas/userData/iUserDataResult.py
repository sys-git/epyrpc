
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iUserDataResult(iApiData):
    r"""
    @summary: The class returned by all UserData methods when applicable.
    """
    def data(self):
        raise NotImplementedException("iUserDataResult.data")
