
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.checkers.testManagement.tests.TestsChecker import \
    TestsChecker
from epyrpc.api.eo_v1.interfaces.checkers.testManagement.iResultsChecker import \
    iResultsChecker
from epyrpc.api.eo_v1.interfaces.common.peers.iAPeer import iAPeer
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestResultsResult import \
    iTestResultsResult

class ResultsChecker(iResultsChecker):
    r"""
    @summary: Check the params for the api.tas.testManagement.results methods.
    """
    validTypes = [iAPeer, list]
    @staticmethod
    def checkTestResult(peerIds):
        return TestsChecker._checkTestIds(peerIds)
    @staticmethod
    def checkPeerResult(peerIds):
        return ResultsChecker._checkPeerIds(peerIds)
    @staticmethod
    def _checkPeerIds(peerIds):
        if not (isinstance(peerIds, iAPeer) or isinstance(peerIds, list)):
            raise ApiParamError(peerIds, ResultsChecker.validTypes)
        args = []
        if isinstance(peerIds, list):
            for i in peerIds:
                if i != None:
                    args.append(ResultsChecker._checkPeerId(i))
        else:
            args.append(ResultsChecker._checkPeerId(peerIds))
        if len(args) == 0:
            raise ApiParamError(peerIds, ResultsChecker.validTypes)
        return args
    @staticmethod
    def _checkPeerId(peerId):
        if not isinstance(peerId, iAPeer):
            raise ApiParamError(peerId, ResultsChecker.validTypes)
        return peerId
    @staticmethod
    def checkStats(stats):
        if not isinstance(stats, iTestResultsResult):
            raise ApiParamError(stats, iTestResultsResult)
        return stats
