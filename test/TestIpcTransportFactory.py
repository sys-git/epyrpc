
from epyrpc.core.eHeadType import eHeadType
from epyrpc.core.eIpcTransportType import eIpcTransportType
from epyrpc.core.transport.IpcTransportFactory import IpcTransportDetailsFactory
from epyrpc.core.transport.UnsupportedTransportError import \
    UnsupportedTransportError
from epyrpc.core.transport.details.iQueueTransportDetails import \
    iQueueTransportDetails
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
from multiprocessing.queues import Queue
import unittest

class TestIpcTransportDetailsFactory(unittest.TestCase):
    def setUp(self):
        path = "config/ipc"
        self._config = ConfigurationManager(cwd=path).getConfiguration("masterLauncher").configuration.Configurations
    def tearDown(self):
        IpcTransportDetailsFactory._details = None
    def testNeck(self):
        details = IpcTransportDetailsFactory.get(self._config.api.ipc, eHeadType.NECK)
        assert isinstance(details, iQueueTransportDetails)
        assert isinstance(details.qRx(), Queue)
        assert isinstance(details.qTx(), Queue)
        assert details.qRx() != details.qTx()
        packager = details.packager()
        assert packager == (None, None)
        return details
    def testHead(self):
        details = IpcTransportDetailsFactory.get(self._config.api.ipc, eHeadType.HEAD)
        assert isinstance(details, iQueueTransportDetails)
        assert isinstance(details.qRx(), Queue)
        assert isinstance(details.qTx(), Queue)
        assert details.qRx() != details.qTx()
        return details
    def testHeadDifferentToNeck(self):
        h = self.testHead()
        n = self.testNeck()
        assert h.qRx() != n.qRx()
        assert h.qTx() != n.qTx()

class TestIpcTransportDetailsFactoryUnsupportedHead(unittest.TestCase):
    def tearDown(self):
        IpcTransportDetailsFactory._details = None
        ConfigurationManager.destroySingleton()
    def testUnsupported(self, head=eHeadType.HEAD):
        path = "config/ipc"
        self._config = ConfigurationManager(cwd=path).getConfiguration("ipcTransportFactory").configuration
        try:
            IpcTransportDetailsFactory.get(self._config.ipc, head)
        except UnsupportedTransportError, e:
            assert e.message == eIpcTransportType.UNKNOWN
    def testUnsupportedType(self, head=eHeadType.HEAD):
        path = "config/ipc"
        self._config = ConfigurationManager(cwd=path).getConfiguration("ipcTransportFactory1").configuration
        try:
            IpcTransportDetailsFactory.get(self._config.ipc, head)
        except UnsupportedTransportError, e:
            assert e.message == "something-else-altogether"

class TestIpcTransportDetailsFactoryUnsupportedNeck(TestIpcTransportDetailsFactoryUnsupportedHead):
    def tearDown(self):
        IpcTransportDetailsFactory._details = None
        ConfigurationManager.destroySingleton()
    def testUnsupported(self, head=eHeadType.NECK):
        super(TestIpcTransportDetailsFactoryUnsupportedNeck, self).testUnsupported(head)
    def testUnsupportedType(self, head=eHeadType.NECK):
        super(TestIpcTransportDetailsFactoryUnsupportedNeck, self).testUnsupportedType(head)

if __name__ == '__main__':
    unittest.main()
