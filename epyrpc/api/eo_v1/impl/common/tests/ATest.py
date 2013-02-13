
from epyrpc.api.eo_v1.interfaces.common.tests.iATest import iATest

class ATest(iATest):
    def __init__(self, testId):
        self._testId = testId
    def testId(self):
        return self._testId
    def export(self):
        return ATest(self._testId)
