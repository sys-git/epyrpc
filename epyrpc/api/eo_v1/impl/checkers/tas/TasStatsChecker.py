
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.checkers.tas.iTasStatsChecker import \
    iTasStatsChecker
from epyrpc.api.eo_v1.interfaces.common.peers.iPeerStatsResult import \
    iPeerStatsResult
from epyrpc.api.eo_v1.interfaces.common.tas.stats.iStatsResult import iStatsResult
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestStatsResult import \
    iTestStatsResult

class TasStatsChecker(iTasStatsChecker):
    r"""
    @summary: Check the params for the api.tas.stats methods.
    """
    allowedTypes = [iStatsResult]
    @staticmethod
    def checkStatsChange(stats):
        return TasStatsChecker._checkStats(stats)
    @staticmethod
    def checkQuery(stats):
        return TasStatsChecker._checkStats(stats)
    @staticmethod
    def _checkStats(stats):
        if not isinstance(stats, iStatsResult):
            raise ApiParamError(stats, TasStatsChecker.allowedTypes)
        if isinstance(stats.testStats, iTestStatsResult):
            raise ApiParamError(stats.testStats, iTestStatsResult)
        if isinstance(stats.testStats, iPeerStatsResult):
            raise ApiParamError(stats.testStats, iPeerStatsResult)
        return stats
