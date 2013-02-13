
from epyrpc.api.eo_v1.interfaces.common.tests.iATestResult import iATestResult

class ATestResult(iATestResult):
    def __init__(self, testId):
        self._testId = testId
    def testId(self):
        return self._testId
    def export(self):
        return ATestResult(self._testId)
