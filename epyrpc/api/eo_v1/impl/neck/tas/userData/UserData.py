
from epyrpc.api.eo_v1.interfaces.neck.tas.userData.iUserData import iUserData
from epyrpc.api.eo_v1.impl.checkers.tas.UserDataChecker import UserDataChecker
from epyrpc.api.eo_v1.impl.common.tas.userData.UserDataResult import UserDataResult
from epyrpc.api.eo_v1.impl.common.tas.userData.UserDataNoValueError import UserDataNoValueError

class UserData(iUserData):
    def __init__(self, ns="", solicited=True):
        super(UserData, self).__init__(ns=ns, solicited=solicited)
    def _getDefaultReturnValues(self, data):
        result = {}
        for key in data.keys():
            result[key] = UserDataNoValueError(key)
        return result
    """ HANDLERS: """
    def _handler_overwrite(self, tId, bSynchronous, data):
        data = self._handleStandardCheck(tId, bSynchronous, UserDataChecker.checkOverwrite, data)
        def _overwrite(data):
            #    Assign default values.
            result = self._getDefaultReturnValues(data)
            #    FIXME Implement this.
            pass
            #    Return the result
            return UserDataResult(result)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _overwrite(x), data)
    def _handler_update(self, tId, bSynchronous, data):
        data = self._handleStandardCheck(tId, bSynchronous, UserDataChecker.checkUpdate, data)
        def _update(data):
            #    Assign default values.
            result = self._getDefaultReturnValues(data)
            #    FIXME Implement this.
            pass
            #    Return the result
            return UserDataResult(result)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _update(x), data)
    def _handler_clear(self, tId, bSynchronous, data):
        data = self._handleStandardCheck(tId, bSynchronous, UserDataChecker.checkClear, data)
        def _clear(data):
            #    Assign default values.
            result = self._getDefaultReturnValues(data)
            #    FIXME Implement this.
            pass
            #    Return the result
            return UserDataResult(result)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _clear(x), data)
    def _handler_clearAll(self, tId, bSynchronous):
        def _clearAll(data):
            #    FIXME Implement this.
            pass
            #    Returns nothing!
        return self._handleStandardCall(tId, bSynchronous, _clearAll)
    def _handler_retrieve(self, tId, bSynchronous, data):
        data = self._handleStandardCheck(tId, bSynchronous, UserDataChecker.checkRetrieve, data)
        def _retrieve(data):
            #    Assign default values.
            result = self._getDefaultReturnValues(data)
            #    FIXME Implement this.
            pass
            #    Return the result
            return UserDataResult(result)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _retrieve(x), data)
    def _handler_retrieveAll(self, tId, bSynchronous):
        def _retrieveAll():
            #    FIXME Implement this.
            pass
            #    Return the result
            return UserDataResult({})
        return self._handleStandardCall(tId, bSynchronous, _retrieveAll)
