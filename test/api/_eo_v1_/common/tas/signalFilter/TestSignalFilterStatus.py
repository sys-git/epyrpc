
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.impl.common.tas.signalFilter.SignalFilterStatus import \
    SignalFilterStatus
import unittest

class TestSignalFilterStatus(unittest.TestCase):
    def testOnOn(self):
        self._do(eMute.ON, eGlobalEnable.ON)
    def testOnOff(self):
        self._do(eMute.ON, eGlobalEnable.OFF)
    def testOffOff(self):
        self._do(eMute.OFF, eGlobalEnable.OFF)
    def testOffOn(self):
        self._do(eMute.OFF, eGlobalEnable.ON)
    def _do(self, gM, gE):
        result = SignalFilterStatus(gM, gE)
        assert result.globalMute() == gM
        assert result.globalEnable() == gE
    def testInvalidMute(self):
        eM = ~eMute.OFF
        assert not eMute.isValid(eM)
        try:
            self._do(eM, eGlobalEnable.ON)
        except ApiParamError, e:
            assert e.item == eM
            assert eMute in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False
    def testInvalidEnable(self):
        eG = ~eGlobalEnable.OFF
        assert not eGlobalEnable.isValid(eG)
        try:
            self._do(eMute.ON, eG)
        except ApiParamError, e:
            assert e.item == eG
            assert eGlobalEnable in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False


if __name__ == '__main__':
    unittest.main()
