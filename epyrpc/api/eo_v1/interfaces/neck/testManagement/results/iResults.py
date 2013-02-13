
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iResults(iApi):
    def _handler_testResult(self, testIds):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Get all the results for a given Test.
        @param testIds: [iATestId] or iATestId
        @see: iResults._handler_configure()
        @raise ApiParamError: Error in parameters.
        @return: dict{iATestId:iATestResult}
        @TODO: Implement getting of test results.
        """
        raise NotImplementedException("iResults.testResult")
    def _handler_peerResult(self, tId, bSynchronous, peerIds):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Get all the results for a given Peer.
        @param peerIds: [iAPeer] or iAPeer
        @see: iResults._handler_configure()
        @raise ApiParamError: Error in parameters.
        @return: dict{iResultsId:iATestResult}
        @TODO: Implement getting of peer results.
        """
        raise NotImplementedException("iResults.peerResult")
    def _handler_package(self, tId, bSynchronous):
        r"""
        @summary: Package the results up.
        @attention: This can only be achieved when the ExecutionOrganiser is
        in the correct state.
        @attention: Same rules apply to the arguments as that of the API that called it
        @see: iResults._handler_configure()
        @raise ApiParamError: Error in parameters.
        @raise Exception: Invalid-state, error when packaging.
        @return: dict{iResultsId:iATestResult}
        @TODO: Implement packaging of results.
        """
        raise NotImplementedException("iResults.package")
    def packageStatusChange(self, e_package_state, stagePercentComplete, totalPercentComplete):
        r"""
        @summary: Packaging state-change has occurred, propagate back to the 'other-side'.
        @raise ApiParamError: Error in parameters.
        @return: N/A.
        """
        raise NotImplementedException("iResults.package")
    def trmsUpload(self, e_upload_code, testIds, data, percentComplete):
        r"""
        @summary: Upload to TRMS has occurred, propagate back to the 'other-side'.
        @raise ApiParamError: Error in parameters.
        @return: N/A.
        """
        raise NotImplementedException("iResults.trmsUpload")

