from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.tas.StateControlChecker import \
    StateControlChecker
from epyrpc.api.eo_v1.interfaces.head.tas.stateControl.iStateControl import \
    iStateControl

class StateControl(iStateControl):
    def __init__(self, ns="", solicited=True):
        iStateControl.__init__(self, ns, solicited)

    def init(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)

    # CALLABLES-ACTIONS

    def terminate(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)

    def run(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)

    def pause(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)

    def pauseAtEnd(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)

    def stop(self, **kwargs):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, **StateControlChecker.checkStop(**kwargs))
