
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData

class iSignalFilterStatus(iApiData):
    def globalMute(self):
        raise NotImplementedException("iSignalFilterStatus.globalMute")
    def globalEnable(self):
        raise NotImplementedException("iSignalFilterStatus.globalEnable")
