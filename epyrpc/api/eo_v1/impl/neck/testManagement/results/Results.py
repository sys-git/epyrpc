
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.testManagement.results.ResultsChecker import \
    ResultsChecker
from epyrpc.api.eo_v1.impl.common.testManagement.results.PackageResult import \
    PackageResult
from epyrpc.api.eo_v1.impl.common.tests.ATestResult import ATestResult
from epyrpc.api.eo_v1.interfaces.neck.testManagement.results.iResults import \
    iResults
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
import copy

class Results(iResults):
    def __init__(self, ns="", solicited=False):
        super(Results, self).__init__(ns=ns, solicited=solicited)

    # CALLABLES-EVENTS
    def packageStatusChange(self, e_package_state, stagePercentComplete, totalPercentComplete):
        api = ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited,
            state=e_package_state,
            stagePercentComplete=stagePercentComplete,
            totalPercentComplete=totalPercentComplete)
        return api

    def trmsUpload(self, e_upload_code, testIds, data, percentComplete):
        api = ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited,
            uploadCode=e_upload_code, testIds=testIds, data=data,
            percentComplete=percentComplete)
        return api

    def resultsStatsChange(self, stats):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, stats=ResultsChecker.checkStats(stats))

    """ HANDLERS: """
    def _handler_testResult(self, tId, bSynchronous, testIds):
        testIds = self._handleStandardCheck(tId, bSynchronous, ResultsChecker.checkTestResult, testIds)
        def _testResult(testIds):
            #    Return a dict{iTestId:iATestResult}
            result = {}
            for testId in testIds:
                #    FIXME: For now, just return empty objects:
                try:
                    aTestResult = ATestResult(testId).export()
                except Exception, e:
                    aTestResult = e
                result[testId] = aTestResult
            return result
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _testResult(x), testIds)
    def _handler_peerResult(self, tId, bSynchronous, peerIds):
        peerIds = self._handleStandardCheck(tId, bSynchronous, ResultsChecker.checkPeerResult, peerIds)
        def _peerResult(peerIds):
            #    Return a dict{iPeerId:iATestResult}
            result = {}
            for peerId in peerIds:
                #    FIXME: For now, just return empty objects:
                try:
                    aTestResult = ATestResult(peerId).export()
                except Exception, e:
                    aTestResult = e
                result[peerId] = aTestResult
            return result
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _peerResult(x), peerIds)
    def _handler_package(self, tId, bSynchronous):
        def _package():
            #    TODO: Package up the results, emitting package events as it goes.
            return PackageResult()
        return self._handleStandardCall(tId, bSynchronous, _package)
    def _handler_stats(self, tId, bSynchronous):
        def _stats():
            return copy.deepcopy(ExecutionOrganiser().getCache().getStats().resultStats())
        return self._handleStandardCall(tId, bSynchronous, _stats)


