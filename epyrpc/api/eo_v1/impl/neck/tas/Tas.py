from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.tas.TasStatsChecker import TasStatsChecker
from epyrpc.api.eo_v1.impl.neck.tas.configuration.Configuration import \
    Configuration
from epyrpc.api.eo_v1.impl.neck.tas.logging.Logging import Logging
from epyrpc.api.eo_v1.impl.neck.tas.signalFilter.SignalFilter import SignalFilter
from epyrpc.api.eo_v1.impl.neck.tas.stateControl.StateControl import StateControl
from epyrpc.api.eo_v1.impl.neck.tas.userData.UserData import UserData
from epyrpc.api.eo_v1.interfaces.neck.tas.iTas import iTas
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser

class Tas(iTas):
    """
    @attention: This class could be auto-generated from, say XML.
    @attention: attr(signalFilter) = The signalFilter object.
    @attention: attr(stateControl) = The stateControl object.
    @attention: attr(configuration) = The configuration object.
    @attention: attr(logging) = The logging object.
    @attention: attr(userData) = The userData object.
    @see: iStateControl.
    @see: iSignalFilter.
    @see: iConfiguration.
    @see: iLogging.
    @see: iUserData.
    """
    def __init__(self, ns="", solicited=False, ipc=None):
        super(Tas, self).__init__(ns=ns, solicited=solicited)
        self._setup(ns=self._getNamespace(), solicited=self.solicited)

    def _setup(self, **kwargs):
        self.signalFilter = SignalFilter(**kwargs)
        self._apis.append(self.signalFilter)
        self.stateControl = StateControl(**kwargs)
        self._apis.append(self.stateControl)
        self.configuration = Configuration(**kwargs)
        self._apis.append(self.configuration)
        self.logging = Logging(**kwargs)
        self._apis.append(self.logging)
        self.userData = UserData(**kwargs)
        self._apis.append(self.userData)

    # HANDLERS
    def _handler_stats(self, tId, bSynchronous):
        def _stats():
            return ExecutionOrganiser().getCache().getStats()
        return self._handleStandardCall(tId, bSynchronous, _stats)

    # CALLABLES-EVENTS
    def signal(self, signalCount, filterId, namespace, signal, status):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, signalCount=signalCount, filterId=filterId,
            namespace=namespace, signal=signal, status=status)

    def error(self, error):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, error=error)

    def engineStateChange(self, uId, newState, previousState):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, uId=uId, newState=newState,
            previousState=previousState)

    def sigInt(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)

    def statsChange(self, stats):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, stats=TasStatsChecker.checkStatsChange(stats))
