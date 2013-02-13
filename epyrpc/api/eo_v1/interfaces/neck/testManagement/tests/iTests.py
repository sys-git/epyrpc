
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTests(iApi):
    r""" HANDLERS: """
    def _handler_abort(self, tId, bSynchronous, testIds):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Abort the given testIds.
        @see: iTests._handler_abort()
        @return: ???
        """
        raise NotImplementedException("iTests._handler_abort")
    def _handler_queryTests(self, tId, bSynchronous, testIds):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Query the given testIds.
        @see: iTests._handler_queryTests()
        @return: ???
        """
        raise NotImplementedException("iTests._handler_queryTests")
    def _handler_queryTestPacks(self, tId, bSynchronous):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Query the currently selected test-packs.
        @return: TestPacks
        """
        raise NotImplementedException("iTests._handler_queryTestPacks")
    def _handler_stats(self, tId, bSynchronous):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Query the currently test stats.
        @return: iTestStatsResult
        """
        raise NotImplementedException("iTests._handler_stats")
    r""" CALLABLES-EVENTS: """
    def testStateChange(self, cachedTest):
        r"""
        @summary: A test has changed state, propagate back to the 'other-side'.
        @return: N/A.
        @type cachedTest: CachedTestDetails 
        """
        raise NotImplementedException("iTests.testStateChange")
    def testStatsChange(self, test_stats_result):
        r"""
        @summary: Test stats have changed, propagate back to the 'other-side'.
        @return: N/A.
        @type test_stats_result: testStatsResult
        """
        raise NotImplementedException("iTests.testStatsChange")
    def newTests(self, tests):
        r"""
        @summary: New tests have appeared, propagate back to the 'other-side'.
        @return: N/A.
        @type test_stats_result: dict{int testId:CachedTestDetails}
        """
        raise NotImplementedException("iTests.newTests")
    def metadata(self, tests):
        r"""
        @summary: New Test Metadata has appeared, propagate back to the 'other-side'.
        @return: N/A.
        @type test_stats_result: CachedTestMetadataDetails
        """
        raise NotImplementedException("iTests.metadata")
