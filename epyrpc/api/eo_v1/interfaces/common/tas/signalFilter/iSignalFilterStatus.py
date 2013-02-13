
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iSignalFilterStatus(iApiData):
    def globalMute(self):
        raise NotImplementedException("iSignalFilterStatus.globalMute")
    def globalEnable(self):
        raise NotImplementedException("iSignalFilterStatus.globalEnable")
