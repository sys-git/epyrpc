
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.tas.UserDataChecker import UserDataChecker
from epyrpc.api.eo_v1.interfaces.head.tas.userData.iUserData import iUserData

class UserData(iUserData):
    def __init__(self, ns="", solicited=True):
        super(UserData, self).__init__(ns=ns, solicited=solicited)
    """ CALLABLES-ACTIONS: """
    def overwrite(self, data):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, UserDataChecker.checkOverwrite(data))
    def update(self, data):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, UserDataChecker.checkUpdate(data))
    def clear(self, data):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, UserDataChecker.checkClear(data))
    def clearAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def retrieve(self, data):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, UserDataChecker.checkRetrieve(data))
    def retrieveAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
