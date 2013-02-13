
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.interfaces.head.tas.logging.iLogging import iLogging

class Logging(iLogging):
    def __init__(self, ns="", solicited=True):
        super(Logging, self).__init__(ns=ns, solicited=solicited)
    """ CALLABLES-ACTIONS: """
    def turnOn(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def turnOff(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def query(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
