
from epyrpc.api.eo_v1.interfaces.common.tas.userData.iUserDataStoreError import iUserDataStoreError

class UserDataStoreError(iUserDataStoreError):
    def __init__(self, key=None, exc=None):
        super(UserDataStoreError, self).__init__(exc)
        self._key = key
    def key(self):
        return self._key
    def error(self):
        return self.message
