
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTestResultsResult(iApiData):
    def stats(self):
        raise NotImplementedException("iTestResultsResult.stats")
