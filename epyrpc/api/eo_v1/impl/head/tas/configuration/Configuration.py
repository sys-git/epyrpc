from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.tas.ConfigurationChecker import \
    ConfigurationChecker
from epyrpc.api.eo_v1.interfaces.head.tas.configuration.iConfiguration import \
    iConfiguration

class Configuration(iConfiguration):
    def __init__(self, ns="", solicited=False):
        iConfiguration.__init__(self, ns, solicited)

    # CALLABLES-ACTIONS
    def configure(self, args={}):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, ConfigurationChecker.checkConfigure(args))

    def query(self, args=[]):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, ConfigurationChecker.checkQuery(args))

    def queryAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited)
