
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTests(iApi):
    r"""
    @note: These 'EVENT_*' are api's that the caller can register
    it's own handler to receive.
    @attention: It is critically important that these strings are IDENTICAL
    to the method names in the relevant api: tas.py
    """
    EVENT__TEST_STATE_CHANGE = u"testStateChange"
    EVENT__TEST_STATS_CHANGE = u"testStatsChange"
    EVENT__NEW_TESTS = u"newTests"
    EVENT__METADATA = u"metadata"
    """ CALLABLES-ACTIONS: """
    def abort(self, testIds):
        r"""
        @summary: Abort the given testIds.
        @return: ???
        """
        raise NotImplementedException("iTests.abort")
    def queryTests(self, testIds):
        r"""
        @summary: Query the given testIds.
        @return: ???
        """
        raise NotImplementedException("iTests.queryTests")
    def queryMetadata(self):
        r"""
        @summary: Query the current test-pack meta-data.
        @return: CachedTestMetadataDetails
        """
        raise NotImplementedException("iTests.queryMetadata")
    def stats(self):
        r"""
        @summary: Query the currently test stats.
        @return: iTestStatsResult
        """
        raise NotImplementedException("iTests.stats")
