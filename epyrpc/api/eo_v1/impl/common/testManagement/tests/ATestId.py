
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iATestId import iATestId

class ATestId(iATestId):
    def __init__(self, testId):
        if not isinstance(testId, int):
            raise ApiParamError(testId, int)
        self._id = testId
    def testId(self):
        return self._id
    def export(self):
        fId = ATestId(self._id)
        return fId
    def __eq__(self, other):
        if isinstance(other, iATestId):
            if other.testId() == self.testId():
                return True
        return False
