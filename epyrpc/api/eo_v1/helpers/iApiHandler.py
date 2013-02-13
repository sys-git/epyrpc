
from epyrpc.utils.Interfaces import Interface
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iApiHandler(Interface):
    #    cls._EVENT_API_CALLBACK must be defined.
    def _createApiCallbackMap(self):
        r"""
        @summary: Perform initialization in here.
        """
        raise NotImplementedException("iApiHandler._createApiCallbackMap")
    def initialize(self):
        r"""
        @summary: Perform initialization in here.
        """
        raise NotImplementedException("iApiHandler.initialize")
    def _actionEmit(self, signal, hasData, result):
        r"""
        @summary: Perform the actual emition of the API call result data.
        """
        raise NotImplementedException("iApiHandler._actionEmit")
    def _onSignal(self, tId, bSynchronous, signalCount, filterId, namespace, signal, status):
        raise NotImplementedException("iApiHandler._onSignal")
    def _onError(self, tId, bSynchronous, error):
        raise NotImplementedException("iApiHandler._onError")
    def _onSigInt(self, tId, bSynchronous):
        raise NotImplementedException("iApiHandler._onSigInt")
    def _onEngineStateChange(self, tId, bSynchronous, uId, newState, previousState):
        raise NotImplementedException("iApiHandler._onEngineStateChange")
    def _onInsufficientEnv(self, tId, bSynchronous):
        raise NotImplementedException("iApiHandler._onInsufficientEnv")
    def _onDistributionComplete(self, tId, bSynchronous):
        raise NotImplementedException("iApiHandler._onDistributionComplete")
    def _onNewTests(self, tId, bSynchronous, tests):
        raise NotImplementedException("iApiHandler._onNewTests")
    def _onTestMetadata(self, tId, bSynchronous, metadata):
        raise NotImplementedException("iApiHandler._onTestMetadata")
    def _onTestStatsChange(self, tId, bSynchronous, stats):
        raise NotImplementedException("iApiHandler._onTestStatsChange")
    def _onTestStateChange(self, tId, bSynchronous, cachedTest):
        raise NotImplementedException("iApiHandler._onTestStateChange")
    def _onPeerStatsChange(self, tId, bSynchronous, stats):
        raise NotImplementedException("iApiHandler._onPeerStatsChange")
    def _onPeerStateChange(self, tId, bSynchronous, thePeer):
        raise NotImplementedException("iApiHandler._onPeerStateChange")
    def _onPeersNew(self, tId, bSynchronous, thePeers):
        raise NotImplementedException("iApiHandler._onPeersNew")
    def _onPeerHeartbeat(self, tId, bSynchronous, thePeer):
        raise NotImplementedException("iApiHandler._onPeerHeartbeat")
    def _onTasStatsChange(self, tId, bSynchronous, stats):
        raise NotImplementedException("iApiHandler._onTasStatsChange")
    def _onTrmsUpload(self, tId, bSynchronous, e_upload_code, testIds, data, percentComplete):
        raise NotImplementedException("iApiHandler._onTrmsUpload")
    def _onPackageStatusChange(self, tId, bSynchronous, e_package_state, stagePercentComplete, totalPercentComplete):
        raise NotImplementedException("iApiHandler._onPackageStatusChange")
    def _onResultsStats(self, tId, bSynchronous, stats):
        raise NotImplementedException("iApiHandler._onResultsStats")


