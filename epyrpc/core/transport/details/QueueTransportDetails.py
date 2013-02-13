
from epyrpc.core.eIpcTransportType import eIpcTransportType
from epyrpc.core.transport.details.iQueueTransportDetails import \
    iQueueTransportDetails
from multiprocessing.queues import Queue

class QueueTransportDetails(iQueueTransportDetails):
    _type = eIpcTransportType.MQUEUE
    def __init__(self, compression=None, encryption=None):
        self._qRx = Queue()
        self._qTx = Queue()
        self._compression = compression
        self._encryption = encryption
    def qRx(self):
        return self._qRx
    def qTx(self):
        return self._qTx
    def del_qTx(self):
        try:
            del self._qTx
        except Exception, _e:
            #    Don't care.
            pass
        self._qTx = None
    def del_qRx(self):
        try:
            del self._qRx
        except Exception, _e:
            #    Don't care.
            pass
        self._qRx = None
    def isqRxClosed(self):
        try:
            return self._qRx._closed
        except Exception, _e:
            return True
    def isqTxClosed(self):
        try:
            return self._qTx._closed
        except Exception, _e:
            return True
    def getType(self):
        return self._type
    def invert(self):
        qRx = self._qRx
        qTx = self._qTx
        result = QueueTransportDetails(compression=self._compression, encryption=self._encryption)
        result._qRx = qTx
        result._qTx = qRx
        return result
    def packager(self):
        return (self._compression, self._encryption)

