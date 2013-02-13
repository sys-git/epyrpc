
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iStateControlChecker(iApi):
    @staticmethod
    def checkArgs(args):
        raise NotImplementedException("iSignalFilterChecker.checkArgs")

