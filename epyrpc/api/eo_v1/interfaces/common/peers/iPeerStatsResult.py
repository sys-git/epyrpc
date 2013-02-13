
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData

class iPeerStatsResult(iApiData):
    def stats(self):
        raise NotImplementedException("iPeerStatsResult.stats")
