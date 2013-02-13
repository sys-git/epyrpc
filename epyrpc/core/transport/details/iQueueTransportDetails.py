
from epyrpc.core.transport.details.iTransportDetails import iTransportDetails
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iQueueTransportDetails(iTransportDetails):
    def qRx(self):
        raise NotImplementedException("iTransportDetails.qRx")
    def qTx(self):
        raise NotImplementedException("iTransportDetails.qTx")
    def del_qRx(self):
        raise NotImplementedException("iTransportDetails.del_qRx")
    def del_qTx(self):
        raise NotImplementedException("iTransportDetails.del_qTx")
