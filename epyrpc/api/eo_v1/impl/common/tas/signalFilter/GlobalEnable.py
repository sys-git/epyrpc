
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iGlobalEnable import iGlobalEnable

class GlobalEnable(iGlobalEnable):
    def __init__(self, enabler=eGlobalEnable.ON):
        assert eGlobalEnable.isValid(enabler)
        self._eEnabled = enabler
    def isEnabled(self):
        return self._eEnabled == eGlobalEnable.ON
    def export(self):
        return GlobalEnable(self._eEnabled)
