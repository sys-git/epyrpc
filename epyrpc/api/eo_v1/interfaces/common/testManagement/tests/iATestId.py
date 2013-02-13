
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iATestId(iApiData):
    def testId(self):
        r"""
        @return: The testId.
        """
        raise NotImplementedException("iTestId.testId")

