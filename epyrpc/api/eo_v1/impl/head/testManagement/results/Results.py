
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.testManagement.results.ResultsChecker import \
    ResultsChecker
from epyrpc.api.eo_v1.interfaces.head.testManagement.results.iResults import \
    iResults

class Results(iResults):
    def __init__(self, ns="", solicited=True):
        super(Results, self).__init__(ns=ns, solicited=solicited)
    """ CALLABLES-ACTIONS: """
    def testResult(self, testIds):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, ResultsChecker.checkTestResult(testIds))
    def peerResult(self, peerIds):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, ResultsChecker.checkPeerResult(peerIds))
    def package(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def stats(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
