
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.core.TransportFactory import TransportFactory
from epyrpc.core.arbitor.ApiArb import ApiArb
from epyrpc.core.eHeadType import eHeadType
from epyrpc.core.eIpcTransportType import eIpcTransportType
from epyrpc.core.transaction.TransactionManager import TransactionManager
from epyrpc.core.transport.details.QueueTransportDetails import \
    QueueTransportDetails
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener
from epyrpc.core.transport.queue.QueueTransporter import QueueTransporter
from epyrpc.head.HeadQueueTransporter import HeadQueueTransporter
import unittest

class TestTransportFactory(unittest.TestCase, iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    def setUp(self):
        self.transportDetails = QueueTransportDetails()
        self.transactionManager = TransactionManager()
        self.scl = self
        self.drl = self
    def teasrDown(self):
        self.transportDetails.del_qRx()
        self.transportDetails.del_qTx()
        del self.transportDetails
    def testHeadMQueue(self):
        h = TransportFactory.get(eHeadType.HEAD, self.transportDetails, self.transactionManager, self, self)
        assert isinstance(h, ApiArb)
        assert isinstance(h, iIpcTransport)
    def testNeckMQueue(self):
        h = TransportFactory.get(eHeadType.NECK, self.transportDetails, self.transactionManager, self, self)
        assert isinstance(h, ApiArb)
        assert isinstance(h, iIpcTransport)
    def testHeadMQueueNoArb(self):
        h = TransportFactory.getNoArb(eHeadType.HEAD, self.transportDetails, self.transactionManager, self, self)
        assert isinstance(h, HeadQueueTransporter)
        assert isinstance(h, iIpcTransport)
    def testNeckMQueueNoArb(self):
        h = TransportFactory.getNoArb(eHeadType.NECK, self.transportDetails, self.transactionManager, self, self)
        assert isinstance(h, QueueTransporter)
        assert isinstance(h, iIpcTransport)
    def testInvalidType(self):
        headType = eHeadType.HEAD
        type_ = eIpcTransportType.MQUEUE + "hello.world!"
        self.transportDetails._type = type_
        try:
            TransportFactory.get(headType, self.transportDetails, self.transactionManager, self, self)
        except ApiParamError, e:
            assert e.item == type_
            assert len(e.allowedTypes) == 1
            assert eIpcTransportType in e.allowedTypes
        else:
            assert False
    def testInvalidHead(self, type_=eIpcTransportType.MQUEUE):
        headType = eHeadType.HEAD + "hello.world!"
        assert not eHeadType.isValid(headType)
        try:
            TransportFactory.get(headType, self.transportDetails, self.transportDetails, self.transactionManager, self, self)
        except ApiParamError, e:
            assert e.item == headType
            assert len(e.allowedTypes) == 1
            assert eHeadType in e.allowedTypes
        else:
            assert False

if __name__ == '__main__':
    unittest.main()
