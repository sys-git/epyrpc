
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iATest(iApiData):
    def testId(self):
        raise NotImplementedException("iATest.testId")
