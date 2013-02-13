
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iStatsResult(iApiData):
    def testStats(self):
        raise NotImplementedException("iStatsResult.testStats")
    def peerStats(self):
        raise NotImplementedException("iStatsResult.peerStats")
    def allStats(self):
        raise NotImplementedException("iStatsResult.allStats")
