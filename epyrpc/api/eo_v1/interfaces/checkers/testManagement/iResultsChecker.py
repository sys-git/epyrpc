
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iResultsChecker(iApi):
    @staticmethod
    def checkTestResult(testIds):
        raise NotImplementedException("iResultsChecker.checkTestResult")
    @staticmethod
    def checkPeerResult(peerIds):
        raise NotImplementedException("iResultsChecker.checkPeerResult")

