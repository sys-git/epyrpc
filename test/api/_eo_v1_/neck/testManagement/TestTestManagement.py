
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.neck.testManagement.TestManagement import \
    TestManagement
from epyrpc.api.eo_v1.interfaces.neck.testManagement.iTestManagement import \
    iTestManagement
from epyrpc.api.eo_v1.interfaces.neck.testManagement.tests.iTests import iTests
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
import os
import sys
import unittest

class MyTransport(iIpcTransport):
    def __init__(self, *args, **kwargs):
        pass

class TestTestManagement(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        self.rootNs = "api"
        self.eNs = "api.testManagement".lower()
        self.ipc = MyTransport()
        path = os.path.realpath("config/ipc")
        ConfigurationManager(cwd=path)
    def testNs(self):
        api = TestManagement(ns=self.rootNs, ipc=self.ipc)
        ns = api._getNamespace()
        assert ns == self.eNs, "Got: %(NS)s" % {"NS":ns}
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
    def testTests(self):
        api = TestManagement(ns=self.rootNs, ipc=self.ipc)
        what = api.tests
        eNs = "api.testManagement.tests".lower()
        assert isinstance(what, iTests)
        ns = what._getNamespace()
        assert ns == eNs, "Got: %(NS)s" % {"NS":ns}

if __name__ == '__main__':
    unittest.main()
