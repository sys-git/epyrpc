
from epyrpc.api.iApiData import iApiData
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iLoggingResult(iApiData):
    def location(self):
        raise NotImplementedException("iLoggingResult.location")
    def isOn(self):
        raise NotImplementedException("iLoggingResult.isOn")
