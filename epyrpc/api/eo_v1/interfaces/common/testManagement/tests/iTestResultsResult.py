
from epyrpc.api.iApiData import iApiData
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iTestResultsResult(iApiData):
    def stats(self):
        raise NotImplementedException("iTestResultsResult.stats")
