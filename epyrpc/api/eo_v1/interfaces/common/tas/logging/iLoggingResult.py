
from epyprc.exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData

class iLoggingResult(iApiData):
    def location(self):
        raise NotImplementedException("iLoggingResult.location")
    def isOn(self):
        raise NotImplementedException("iLoggingResult.isOn")
