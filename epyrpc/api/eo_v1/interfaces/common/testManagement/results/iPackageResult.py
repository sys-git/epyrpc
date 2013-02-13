
from epyrpc.api.iApiData import iApiData
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iPackageResult(iApiData):
    def result(self):
        raise NotImplementedException("iPackageResult.result")
