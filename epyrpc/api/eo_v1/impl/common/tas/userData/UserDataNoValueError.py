
from epyrpc.api.eo_v1.interfaces.common.tas.userData.iUserDataNoValueError import iUserDataNoValueError

class UserDataNoValueError(iUserDataNoValueError):
    def __init__(self, key):
        super(UserDataNoValueError, self).__init__()
        self._key = key
    def key(self):
        return self._key
