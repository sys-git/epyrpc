
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iPackageResult(iApiData):
    def result(self):
        raise NotImplementedException("iPackageResult.result")
