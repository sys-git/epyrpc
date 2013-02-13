
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.head.testManagement.TestManagement import \
    TestManagement
from epyrpc.api.eo_v1.interfaces.head.testManagement.iTestManagement import \
    iTestManagement
from epyrpc.api.eo_v1.interfaces.head.testManagement.tests.iTests import iTests
from epyrpc.core.transport.iIpcTransport import iIpcTransport
import unittest

class TestTestManagement(unittest.TestCase):
    def setUp(self):
        self.rootNs = "api"
        self.eNs = "api.testManagement".lower()
        self.ipc = MyTransport()
    def testNs(self):
        api = TestManagement(ns=self.rootNs, ipc=self.ipc)
        ns = api._getNamespace()
        assert ns == self.eNs, "Got: %(NS)s" % {"NS":ns}
    def testTests(self):
        api = TestManagement(ns=self.rootNs, ipc=self.ipc)
        what = api.tests
        eNs = "api.testManagement.tests".lower()
        assert isinstance(what, iTests)
        ns = what._getNamespace()
        assert ns == eNs, "Got: %(NS)s" % {"NS":ns}
    def testNoIpc(self):
        assert isinstance(TestManagement(ns=self.rootNs), iTestManagement)
    def testSetValidIpc(self):
        api = TestManagement(ns=self.rootNs)
        api.ipc = self.ipc
        assert api.ipc == self.ipc
        #    Now check all sub-apis:
        for _api in api._apis:
            assert _api.ipc == self.ipc
    def testSetInvalidIpc(self):
        api = TestManagement(ns=self.rootNs)
        try:
            api.ipc = object()
        except ApiParamError, e:
            assert e.item

class MyTransport(iIpcTransport):
    def __init__(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    unittest.main()
