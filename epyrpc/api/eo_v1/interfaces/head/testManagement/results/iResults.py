
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iResults(iApi):
    r"""
    @note: These 'EVENT_*' are api's that the caller can register
    it's own handler to receive.
    @attention: It is critically important that these strings are IDENTICAL
    to the method names in the relevant api: results.py
    """
    EVENT__PACKAGE_STATUS_CHANGE = u"packageStatusChange"
    EVENT__TRMS_UPLOAD = u"trmsUpload"
    EVENT__STATS = u"resultsStatsChange"
    """ CALLABLES-ACTIONS: """
    def testResult(self, testIds):
        r"""
        @summary: Get all the results for a given Test.
        @param peerIds: [iATestId] or iATestId
        @raise ApiParamError: Error in parameters.
        @return: dict{iATestId:iATestResult}
        """
        raise NotImplementedException("iResults.testResult")
    def peerResult(self, peerIds):
        r"""
        @summary: Get all the results for a given Peer.
        @param peerIds: [iAPeer] or iAPeer
        @raise ApiParamError: Error in parameters.
        @return: dict{iResultsId:iATestResult}
        """
        raise NotImplementedException("iResults.peerResult")
    def package(self):
        r"""
        @summary: Package the results up.
        @attention: This can only be achieved when the ExecutionOrganiser is
        in the correct state.
        @raise Exception: Invalid-state, error when packaging.
        """
        raise NotImplementedException("iResults.package")
