
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.neck.tas.Tas import Tas
from epyrpc.api.eo_v1.interfaces.neck.tas.iTas import iTas
from epyrpc.api.iApiAction import iApiAction
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
import os
import unittest

class MyTransport(iIpcTransport):
    def __init__(self, *args, **kwargs):
        pass

class TestTas(unittest.TestCase):
    def setUp(self):
        self.rootNs = "api"
        self.eNs = "api.tas"
        self.ipc = MyTransport()
        path = os.path.realpath("config/ipc")
        ConfigurationManager(cwd=path)
    def testNs(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        ns = api._getNamespace()
        assert ns == self.eNs, "Got: %(NS)s" % {"NS":ns}
    def testErrorApiCreation(self):
        assert Tas(ns=self.rootNs, ipc=self.ipc).error
    def testError(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        args = 123
        r = api.error(123)
        assert isinstance(r, iApiAction)
        assert r.args()[0] == args
    def testSignalApiCreation(self):
        assert Tas(ns=self.rootNs, ipc=self.ipc).signal
    def testSignal(self):
        api = Tas(ns=self.rootNs, ipc=self.ipc)
        args = (1, 2, 3)
        kwargs = {"four":4}
        r = api.signal(*args, **kwargs)
        assert isinstance(r, iApiAction)
        assert r.args()[0] == args
        assert r.args()[1] == kwargs
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

if __name__ == '__main__':
    unittest.main()
