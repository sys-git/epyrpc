
from epyrpc.api.iApiData import iApiData
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iTestStatsResult(iApiData):
    def stats(self):
        raise NotImplementedException("iTestStatsResult.stats")
