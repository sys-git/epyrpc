
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.core.arbitor.ApiArb import ApiArb
from epyrpc.core.eHeadType import eHeadType
from epyrpc.core.eIpcTransportType import eIpcTransportType
from epyrpc.core.transport.queue.QueueTransporter import QueueTransporter
from epyrpc.head.HeadQueueTransporter import HeadQueueTransporter
 
class TransportFactory(object):
    r"""
    @summary: IPC transport factory.
    """
    @staticmethod
    def _get(e_head_type, i_transport_details, *args, **kwargs):
        e_ipc_transport_type = i_transport_details.getType()
        if not eIpcTransportType.isValid(e_ipc_transport_type):
            raise ApiParamError(e_ipc_transport_type, eIpcTransportType)
        if not eHeadType.isValid(e_head_type):
            raise ApiParamError(e_head_type, eHeadType)
        if e_ipc_transport_type == eIpcTransportType.MQUEUE:
            if e_head_type == eHeadType.HEAD:
                return HeadQueueTransporter(i_transport_details, *args, **kwargs)
            return QueueTransporter(i_transport_details, *args, **kwargs)
    @staticmethod
    def get(*args, **kwargs):
        return ApiArb.create(TransportFactory._get(*args, **kwargs))
    @staticmethod
    def getNoArb(*args, **kwargs):
        return TransportFactory._get(*args, **kwargs)
