
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTestsChecker(iApi):
    @staticmethod
    def checkAbort(testIds):
        raise NotImplementedException("iTestsChecker.checkAbort")
    @staticmethod
    def checkQueryTests(testIds):
        raise NotImplementedException("iTestsChecker.checkQueryTests")

