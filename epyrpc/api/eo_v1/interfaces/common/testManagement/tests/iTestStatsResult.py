
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTestStatsResult(iApiData):
    def stats(self):
        raise NotImplementedException("iTestStatsResult.stats")
