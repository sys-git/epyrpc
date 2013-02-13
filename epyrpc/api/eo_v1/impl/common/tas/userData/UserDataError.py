
from epyrpc.api.eo_v1.interfaces.common.tas.userData.iUserDataError import iUserDataError

class UserDataError(iUserDataError):
    def __init__(self, error):
        super(UserDataError, self).__init__()
        self._error = error
    def error(self):
        return self._error
