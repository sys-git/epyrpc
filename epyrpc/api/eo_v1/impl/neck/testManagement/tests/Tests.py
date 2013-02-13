from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.testManagement.tests.TestsChecker import \
    TestsChecker
from epyrpc.api.eo_v1.impl.common.tests.ATest import ATest
from epyrpc.api.eo_v1.interfaces.neck.testManagement.tests.iTests import iTests
import copy

class Tests(iTests):
    def __init__(self, ns="", solicited=True):
        super(Tests, self).__init__(ns=ns, solicited=solicited)

    # CALLABLES EVENTS
    def testStateChange(self, cachedTests):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, tests=TestsChecker.checkTestStateChange(cachedTests))

    def testStatsChange(self, stats):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, stats=TestsChecker.checkStats(stats))

    def newTests(self, tests):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, tests=TestsChecker.checkNewTests(tests))

    def metadata(self, metadata):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, metadata=TestsChecker.checkMetadata(metadata))

    # HANDLERS
    def _handler_abort(self, tId, bSynchronous, testIds):
        testIds = self._handleStandardCheck(tId, bSynchronous,
            TestsChecker.checkAbort, testIds)

        def _abort(testIds):
            self._logger.warn("!! ABORT !!")
            result = {}
            for testId in testIds:
                try:
                    # TODO: Initiate abort for the given test.
                    response = ATest(testId.testId()).export()
                except Exception, response:
                    pass
                result[testId] = response
            return result

        return self._handleStandardCall(tId, bSynchronous,
            lambda(x): _abort(x), testIds)

    def _handler_queryAll(self, tId, bSynchronous):
        def _queryAll():
            self._logger.warn("!! QUERY_ALL_TESTS !!")
            tests = copy.deepcopy(ExecutionOrganiser().getCache().getAllTests())
            return tests
        return self._handleStandardCall(tId, bSynchronous, _queryAll)

    def _handler_queryTests(self, tId, bSynchronous, i_a_testIds__list):
        i_a_testIds__list = self._handleStandardCheck(tId, bSynchronous,
            TestsChecker.checkQueryTests, i_a_testIds__list)

        def _queryTests(i_a_testIds__list):
            self._logger.warn("!! QUERY_TESTS !!")
            result = {}
            tests = copy.deepcopy(ExecutionOrganiser().getCache().getAllTests())
            for testId in i_a_testIds__list:
                try:
                    response = tests[testId.testId()]
                except Exception, response:
                    pass
                result[testId] = response
            return result

        return self._handleStandardCall(tId, bSynchronous,
            lambda(x): _queryTests(x), i_a_testIds__list)

    def _handler_queryMetadata(self, tId, bSynchronous):
        def _queryMetadata():
            self._logger.warn("!! QUERY_TEST_PMETADATA !!")
            rtn = copy.deepcopy(ExecutionOrganiser().getCache().getTestMetadata())
            return rtn

        return self._handleStandardCall(tId, bSynchronous, _queryMetadata)

    def _handler_stats(self, tId, bSynchronous):
        def _stats():
            stats = ExecutionOrganiser().getCache().getStats()
            # Return the 'test' stats only!
            return stats.testStats()

        return self._handleStandardCall(tId, bSynchronous, _stats)
