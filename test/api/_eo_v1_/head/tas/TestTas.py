
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.head.tas.Tas import Tas
from epyrpc.api.eo_v1.interfaces.head.tas.configuration.iConfiguration import \
    iConfiguration
from epyrpc.api.eo_v1.interfaces.head.tas.iTas import iTas
from epyrpc.api.eo_v1.interfaces.head.tas.logging.iLogging import iLogging
from epyrpc.api.eo_v1.interfaces.head.tas.signalFilter.iSignalFilter import \
    iSignalFilter
from epyrpc.api.eo_v1.interfaces.head.tas.stateControl.iStateControl import \
    iStateControl
from epyrpc.api.iApiAction import iApiAction
from epyrpc.core.transport.iIpcTransport import iIpcTransport
import unittest

class TestTas(unittest.TestCase):
    def setUp(self):
        self.rootNs = "api"
        self.eNs = "api.tas".lower()
        self.ipc = MyTransport()
    def testNs(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        ns = api._getNamespace()
        assert ns == self.eNs, "Got: %(NS)s" % {"NS":ns}
    def testSignalFilter(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        what = api.signalFilter
        eNs = "api.tas.signalFilter".lower()
        assert isinstance(what, iSignalFilter)
        ns = what._getNamespace()
        assert ns == eNs, "Got: %(NS)s" % {"NS":ns}
    def testStateControl(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        what = api.stateControl
        eNs = "api.tas.stateControl".lower()
        assert isinstance(what, iStateControl)
        ns = what._getNamespace()
        assert ns == eNs, "Got: %(NS)s" % {"NS":ns}
    def testConfiguration(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        what = api.configuration
        eNs = "api.tas.Configuration".lower()
        assert isinstance(what, iConfiguration)
        ns = what._getNamespace()
        assert ns == eNs, "Got: %(NS)s" % {"NS":ns}
    def testLogging(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        what = api.logging
        eNs = "api.tas.Logging".lower()
        assert isinstance(what, iLogging)
        ns = what._getNamespace()
        assert ns == eNs, "Got: %(NS)s" % {"NS":ns}
    def testSignalFilterCallthrough(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        what = api.signalFilter
        assert isinstance(what, iSignalFilter)
        assert isinstance(what.status(), iApiAction)
    def testNoIpc(self):
        assert isinstance(Tas(ns=self.rootNs), iTas)
    def testSetValidIpc(self):
        api = Tas(ns=self.rootNs)
        api.ipc = self.ipc
        assert api.ipc == self.ipc
        #    Now check all sub-apis:
        for _api in api._apis:
            assert _api.ipc == self.ipc
    def testSetInvalidIpc(self):
        api = Tas(ns=self.rootNs)
        try:
            api.ipc = object()
        except ApiParamError, e:
            assert e.item

class MyTransport(iIpcTransport):
    def __init__(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    unittest.main()
