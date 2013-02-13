
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iSignalFilterStatus import iSignalFilterStatus
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.ApiParamError import ApiParamError

class SignalFilterStatus(iSignalFilterStatus):
    def __init__(self, globalMute, globalEnable, count=0):
        self.setGlobalMute(globalMute)
        self.setGlobalEnable(globalEnable)
        self._count = count
    def globalMute(self):
        return self._globalMute
    def globalEnable(self):
        return self._globalEnable
    def setGlobalMute(self, globalMute):
        if not eMute.isValid(globalMute):
            raise ApiParamError(globalMute, eMute)
        self._globalMute = globalMute
    def setGlobalEnable(self, globalEnable):
        if not eGlobalEnable.isValid(globalEnable):
            raise ApiParamError(globalEnable, eGlobalEnable)
        self._globalEnable = globalEnable
    def setCount(self, count):
        if count != None:
            if not isinstance(count, int):
                raise ApiParamError(count, int)
        self._count = count
    def count(self):
        return self._count
    def export(self):
        return SignalFilterStatus(self.globalMute(), self.globalEnable(), self.count())
