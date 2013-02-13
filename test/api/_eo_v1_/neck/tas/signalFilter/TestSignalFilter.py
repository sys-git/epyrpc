
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.impl.neck.tas.SignalFilter import SignalFilter
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iSignalFilterStatus import \
    iSignalFilterStatus
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
import os
import sys
import unittest

class TestGlobalEnable(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = os.path.realpath("config/ipc")
        ConfigurationManager(cwd=path)
        self.eo = ExecutionOrganiser()
    def tearDown(self):
        pass
    def testEnabled(self):
        sf = SignalFilter(ns="me")
        eNs = "me.signalfilter"
        assert sf._getNamespace() == eNs, "Got: %(NS)s" % {"NS":eNs}
        tId = 123
        bSynchronous = True
        filters = self.eo.signalFilters()
        #    On:
        enabler = eGlobalEnable.ON
        result = sf._handler_globalEnable(tId, bSynchronous, enabler)
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == enabler
        status = filters.status()
        assert status.globalEnable() == enabler
        #    Off:
        enabler = eGlobalEnable.OFF
        result = sf._handler_globalEnable(tId, bSynchronous, enabler)
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == enabler
        status = filters.status()
        assert status.globalEnable() == enabler

class TestStatus(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = os.path.realpath("config/ipc")
        ConfigurationManager(cwd=path)
        self.eo = ExecutionOrganiser()
    def tearDown(self):
        pass
    def testEnabled(self):
        sf = SignalFilter(ns="me")
        eNs = "me.signalfilter"
        assert sf._getNamespace() == eNs, "Got: %(NS)s" % {"NS":eNs}
        tId = 123
        bSynchronous = True
        filters = self.eo.signalFilters()
        #    On:
        enabler = eGlobalEnable.ON
        result = sf._handler_globalEnable(tId, bSynchronous, enabler)
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == enabler
        status = filters.status()
        assert status.globalEnable() == enabler

        result = sf._handler_status(tId, bSynchronous)
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == enabler
        assert result.globalMute() == filters.status().globalMute()
        assert result.globalEnable() == filters.status().globalEnable()

        #    Off:
        enabler = eGlobalEnable.OFF
        result = sf._handler_globalEnable(tId, bSynchronous, enabler)
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == enabler
        status = filters.status()
        assert status.globalEnable() == enabler

        result = sf._handler_status(tId, bSynchronous)
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == enabler
        assert result.globalMute() == filters.status().globalMute()
        assert result.globalEnable() == filters.status().globalEnable()

if __name__ == '__main__':
    unittest.main()

