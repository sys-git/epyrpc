from epyrpc.api.eo_v1.impl.head.tas.configuration.Configuration import Configuration
from epyrpc.api.eo_v1.impl.head.tas.logging.Logging import Logging
from epyrpc.api.eo_v1.impl.head.tas.signalFilter.SignalFilter import SignalFilter
from epyrpc.api.eo_v1.impl.head.tas.stateControl.StateControl import StateControl
from epyrpc.api.eo_v1.impl.head.tas.userData.UserData import UserData
from epyrpc.api.eo_v1.interfaces.head.tas.iTas import iTas
from epyrpc.api.ApiAction import ApiAction

class Tas(iTas):
    """
    @attention: This class could be auto-generated from, say XML
    @see: iStateControl
    @see: iSignalFilter
    @see: iConfiguration
    @see: iLogging
    @see: iUserData
    """
    def __init__(self, ns="", solicited=True, ipc=None):
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

    """ CALLABLES-ACTIONS: """
    def stats(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)

