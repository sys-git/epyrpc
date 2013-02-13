
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.impl.checkers.tas.SignalFilterChecker import \
    SignalFilterChecker
from epyrpc.api.eo_v1.interfaces.head.tas.signalFilter.iSignalFilter import iSignalFilter

class SignalFilter(iSignalFilter):
    def __init__(self, ns="", solicited=True):
        super(SignalFilter, self).__init__(ns=ns, solicited=solicited)
    """ CALLABLES-ACTIONS: """
    def add(self, namespace):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkAdd(namespace))
    def remove(self, filters):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkRemove(filters))
    def removeAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def muteAll(self, mute=eMute.ON):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkMuteAll(mute))
    def mute(self, filters):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkMute(filters))
    def query(self, filters):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkQuery(filters))
    def queryAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def globalEnable(self, enabler):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkGlobalEnable(enabler))
    def status(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def archive(self, i_location):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkArchive(i_location))
    def retrieve(self, i_range=None):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, SignalFilterChecker.checkRetrieve(i_range))
