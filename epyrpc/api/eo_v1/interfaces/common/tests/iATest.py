
from epyrpc.api.iApiData import iApiData
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iATest(iApiData):
    def testId(self):
        raise NotImplementedException("iATest.testId")
