'''
Created on 16 Jul 2012

@author: francis
'''

from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.common.peers.iPeerStatsResult import \
    iPeerStatsResult
from epyrpc.api.eo_v1.interfaces.common.tas.stats.iStatsResult import iStatsResult
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestResultsResult import \
    iTestResultsResult
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestStatsResult import \
    iTestStatsResult

class StatsResult(iStatsResult):
    def __init__(self, testStats, peerStats, resultStats):
        if not isinstance(testStats, iTestStatsResult):
            raise ApiParamError(testStats, iTestStatsResult)
        if not isinstance(peerStats, iPeerStatsResult):
            raise ApiParamError(testStats, iPeerStatsResult)
        if not isinstance(resultStats, iTestResultsResult):
            raise ApiParamError(resultStats, iTestResultsResult)
        self._testStats = testStats
        self._resultStats = resultStats
        self._peerStats = peerStats
    def resultStats(self):
        return self._resultStats
    def testStats(self):
        return self._testStats
    def peerStats(self):
        return self._peerStats
    def allStats(self):
        return [
                self._testStats,
                self._resultStats,
                self._peerStats,
                ]
