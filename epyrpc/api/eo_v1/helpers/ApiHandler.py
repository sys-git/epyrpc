
from epyrpc.api.eSync import eSync
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.enums.eStateControlResult import eStateControlResult
from epyrpc.api.eo_v1.helpers.ApiRefs import ApiRefs
from epyrpc.api.eo_v1.helpers.iApiHandler import iApiHandler
from epyrpc.api.eo_v1.interfaces.head.peers.iPeers import iPeers
from epyrpc.api.eo_v1.interfaces.head.tas.iTas import iTas
from epyrpc.api.eo_v1.interfaces.head.tas.stateControl.iStateControl import \
    iStateControl
from epyrpc.api.eo_v1.interfaces.head.testManagement.results.iResults import \
    iResults
from epyrpc.api.eo_v1.interfaces.head.testManagement.tests.iTests import iTests
from epyrpc.core.IpcExceptions import TransportStateError
from epyrpc.utils.LogManager import LogManager
import inspect

class _NoCallbackRequired(object):
    pass

class ApiHandler(iApiHandler):
    r"""
    @summary: Encapsulates sending and receiving API calls, callbacks and events.
    """
    def __init__(self, parent, logger=None):
        self._parent = parent
        if logger == None:
            logger = LogManager().getLogger(self.__class__.__name__)
        self._logger = logger
        self.__noCallbackRequired = _NoCallbackRequired()
        self._createApiCallbackMap()
        self._setup()

    def _setup(self):
        #    Setup our API event listeners:
        r""" api.tas: """
        self.api.tas.setHandler(iTas.EVENT__SIGNAL, self._onSignal)
        self.api.tas.setHandler(iTas.EVENT__ERROR, self._onError)
        self.api.tas.setHandler(iTas.EVENT__ENGINE_STATE_CHANGE, self._onEngineStateChange)
        self.api.tas.setHandler(iTas.EVENT__SIGN_INT, self._onSigInt)
        self.api.tas.setHandler(iTas.EVENT__STATS_CHANGE, self._onTasStatsChange)
        r""" api.tas.stateControl: """
        self.api.tas.stateControl.setHandler(iStateControl.EVENT__INSUFFICIENT_ENV, self._onInsufficientEnv)
        self.api.tas.stateControl.setHandler(iStateControl.EVENT__DISTRIBUTION_COMPLETE, self._onDistributionComplete)
        r""" api.testManagement.tests: """
        self.api.testManagement.tests.setHandler(iTests.EVENT__TEST_STATE_CHANGE, self._onTestStateChange)
        self.api.testManagement.tests.setHandler(iTests.EVENT__TEST_STATS_CHANGE, self._onTestStatsChange)
        self.api.testManagement.tests.setHandler(iTests.EVENT__NEW_TESTS, self._onNewTests)
        self.api.testManagement.tests.setHandler(iTests.EVENT__METADATA, self._onTestMetadata)
        r""" api.testManagement.results: """
        self.api.testManagement.results.setHandler(iResults.EVENT__TRMS_UPLOAD, self._onTrmsUpload)
        self.api.testManagement.results.setHandler(iResults.EVENT__PACKAGE_STATUS_CHANGE, self._onPackageStatusChange)
        self.api.testManagement.results.setHandler(iResults.EVENT__STATS, self._onResultsStats)
        r""" api.peers: """
        self.api.peers.setHandler(iPeers.EVENT__PEER_STATS_CHANGE, self._onPeerStatsChange)
        self.api.peers.setHandler(iPeers.EVENT__PEER_STATE_CHANGE, self._onPeerStateChange)
        self.api.peers.setHandler(iPeers.EVENT__PEERS_NEW, self._onPeersNew)
        self.api.peers.setHandler(iPeers.EVENT__PEER_HEARTBEAT, self._onPeerHeartbeat)

    r""" MISC: """
    def _getMyConfig(self):
        return self._parent.config
    def _getMyApi(self):
        return self._parent._api
    def _getMyContext(self):
        return self._parent.cntxt
    def _getMyEmit(self):
        return self._parent.emit

    api = property(_getMyApi)
    config = property(_getMyConfig)
    cntxt = property(_getMyContext)
    emit = property(_getMyEmit)

    r""" API-CALLERS: """
    def engineInit(self, sync=eSync.ASYNCHRONOUS):
        timeout = int(self.config.timeouts.executionOrganiserInit.PCDATA)
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_INIT, self.api.tas.stateControl.init, sync=sync, timeout=timeout)

    def engineStart(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_START, self.api.tas.stateControl.run, sync=sync, callback=self.__noCallbackRequired)

    def engineStop(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_STOP, self.api.tas.stateControl.stop, sync=sync, callback=self.__noCallbackRequired)

    def enginePause(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_PAUSE, self.api.tas.stateControl.pause, sync=sync, callback=self.__noCallbackRequired)

    def enginePauseAtEnd(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_PAUSEATEND, self.api.tas.stateControl.pauseAtEnd, sync=sync, callback=self.__noCallbackRequired)

    def engineTerminate(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_TERMINATE, self.api.tas.stateControl.terminate, sync=sync)

    def signalFilterAdd(self, ns, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSADD, self.api.tas.signalFilter.add, sync=sync, args=[ns])

    def signalFilterMuteAll(self, mute=eMute.ON, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSMUTEALL, self.api.tas.signalFilter.muteAll, sync=sync, args=[mute])

    def signalFilterEnableAll(self, enable=eGlobalEnable.ON, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSENABLEALL, self.api.tas.signalFilter.globalEnable, sync=sync, args=[enable])

    def signalFilterQuery(self, filters=None, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSQUERY, self.api.tas.signalFilter.query, sync=sync, args=[filters])

    def signalFilterQueryAll(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSQUERYALL, self.api.tas.signalFilter.queryAll, sync=sync)

    def signalFilterRemoveAll(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSREMOVEALL, self.api.tas.signalFilter.removeAll, sync=sync)

    def signalFilterRemove(self, fltr, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSREMOVE, self.api.tas.signalFilter.remove, sync=sync, args=[fltr])

    def signalsRetrieve(self, i_range=None, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_SIGNALSRETRIEVE, self.api.tas.signalFilter.retrieve, sync=sync, args=[i_range])

    def statsRefreshTest(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_TESTS_STATS_REFRESH, self.api.testManagement.tests.stats, sync=sync)

    def statsRefreshPeer(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_PEERS_STATS_REFRESH, self.api.peers.stats, sync=sync)

    def statsRefreshResults(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_RESULT_STATS_REFRESH, self.api.testManagement.results.stats, sync=sync)

    def statsRefresh(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_TAS_STATS, self.api.tas.stats, sync=sync)

    def peersRemove(self, i_a_peer_remover, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_PEERS_REMOVE, self.api.peers.remove, sync=sync, args=[i_a_peer_remover])

    def peersQueryAll(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_PEERS_QUERY_ALL, self.api.peers.queryAll, sync=sync)

    def peersQuery(self, i_a_peer__list, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_PEERS_QUERY, self.api.peers.query, sync=sync, args=[i_a_peer__list])

    def testsQueryAll(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_TESTS_QUERY_ALL, self.api.testManagement.tests.queryAll, sync=sync)

    def testsMetadata(self, sync=eSync.ASYNCHRONOUS):
        return self._callApiMethod(self._whoami(), ApiRefs.WHAT__API_TESTS_QUERY_METADATA, self.api.testManagement.tests.queryMetadata, sync=sync)

    r""" API-CALLBACK HANDLER """
    def _onGenericApiCallback(self, args):
        r"""
        @summary: All self.api async methods which specified callbacks will emit their data into here (see args[2]).
        @attention: This is where we will update the UI model that feeds the various physical views...
        @attention: The purpose of this method is to emit events which the views can register to listen for.
         """
        (tId, what, result) = args
        self._logger.warn("** ** onApiCallback[%(T)s] %(W)s ** **" % {"W":what, "T":tId})
        try:
            if isinstance(result, Exception):
                self._logger.error("Api raised an exception: ")
            if what == ApiRefs.WHAT__API_INIT:
                isInit = (result == eStateControlResult.SUCCESS)
                self.cntxt.isInit = isInit
                result = isInit
            elif what == ApiRefs.WHAT__API_TERMINATE:
                result = (result == eStateControlResult.SUCCESS)
            elif (what not in self.cntxt.asyncResults):
                raise Exception("Unhandled API cb: %(W)s" % {"W":what})
            #    Fire the event with the (potentially modified) result data:
            self._formatResultEmit(what, result)
            #    Now clear-out the asyncResult from our context:
            self.cntxt.asyncResults[what] = None
        finally:
            pass

    r""" MISC: """

    def _callApiMethod(self, whoami, index, method, args=[], kwargs={}, sync=eSync.ASYNCHRONOUS, timeout=None, callback=None):
        self._logger.warn("** ** %(WAI)s ** **" % {"WAI":whoami})
        def cb(tId, result):
            self._triggerGenericApiCallback(tId, index, result)
        if callback == self.__noCallbackRequired:
            callback = None
        elif callback == None:
            callback = cb
        return self._makeThatCall(index, method, callback=callback, args=args, kwargs=kwargs, sync=sync, timeout=timeout)

    def _makeThatCall(self, index, method, callback=None, args=[], kwargs={}, sync=eSync.ASYNCHRONOUS, timeout=None):
        try:
            self.cntxt.asyncResults[index] = method(*args, **kwargs)(sync=sync, callback=callback)
        except TransportStateError, e:
            self._logger.debug("Cannot call API: %(M)s due to IPC transport state: %(E)s" % {"M":method, "E":e})
        except Exception, _e:
            self._logger.exception("Error in %(W)s:" % {"W":method})
        else:
            return index

    def _formatResultEmit(self, what, result):
        (signal, hasData) = self._apiCallbackMap[what]
        self._actionEmit(signal, hasData, result)

    def _whoami(self):
        return inspect.stack()[1][3]

    def _triggerGenericApiCallback(self, tId, index, result):
        #    Purge because we don't require this anymore.
        self.cntxt.transactionManager.purge(tId)
        self._actionEmit(self._EVENT_API_CALLBACK, True, (tId, index, result))





