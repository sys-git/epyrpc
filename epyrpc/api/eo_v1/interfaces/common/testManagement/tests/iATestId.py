from epyrpc.api.iApiData import iApiData
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iATestId(iApiData):
    def testId(self):
        r"""
        @return: The testId.
        """
        raise NotImplementedException("iTestId.testId")

