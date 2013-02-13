
from epyrpc.api.eo_v1.interfaces.common.tas.userData.iUserDataResult import iUserDataResult

class UserDataResult(iUserDataResult):
    def __init__(self, data={}):
        self._data = data
    def data(self):
        return self._data
