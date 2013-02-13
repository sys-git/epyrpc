
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.testManagement.tests.TestsChecker import \
    TestsChecker
from epyrpc.api.eo_v1.interfaces.head.testManagement.tests.iTests import iTests

class Tests(iTests):
    def __init__(self, ns="", solicited=True):
        super(Tests, self).__init__(ns=ns, solicited=solicited)
    """ CALLABLES-ACTIONS: """
    def abort(self, testIds):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, TestsChecker.checkAbort(testIds))
    def queryTests(self, testIds):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, TestsChecker.checkQueryTests(testIds))
    def queryAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def queryMetadata(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def stats(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
