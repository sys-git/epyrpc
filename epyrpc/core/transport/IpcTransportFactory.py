
from epyrpc.core.eHeadType import eHeadType
from epyrpc.core.eIpcTransportType import eIpcTransportType
from epyrpc.core.transport.UnsupportedTransportError import \
    UnsupportedTransportError
from epyrpc.core.transport.details.QueueTransportDetails import \
    QueueTransportDetails
from epyrpc.core.transport.iIpcTransportDetailsFactory import \
    iIpcTransportDetailsFactory

class IpcTransportDetailsFactory(iIpcTransportDetailsFactory):
    _details = None
    @staticmethod
    def reset():
        IpcTransportDetailsFactory._details = None
    @staticmethod
    def getStatic(ipcConfig, e_head_type):
        r"""
        @summary: If the interface needs to be created before process spawning (ie: Queue),
        do it now.
        """
        t = ipcConfig.type.PCDATA
        try:
            type_ = eIpcTransportType.lookupEnumerationValue(t)
        except ValueError:
            raise UnsupportedTransportError(t)
        if type_ == eIpcTransportType.MQUEUE:
            compression = None
            if hasattr(ipcConfig, "compression"):
                compression = ipcConfig.compression
            encryption = None
            if hasattr(ipcConfig, "encryption"):
                encryption = ipcConfig.encryption
            if e_head_type == eHeadType.NECK:
                #    Check the cache:
                if IpcTransportDetailsFactory._details == None:
                    IpcTransportDetailsFactory._details = QueueTransportDetails(compression, encryption)
                return IpcTransportDetailsFactory._details
            return QueueTransportDetails(compression, encryption)
        raise UnsupportedTransportError(type_)
    @staticmethod
    def get(ipcConfig, e_head_type):
        t = ipcConfig.type.PCDATA
        try:
            type_ = eIpcTransportType.lookupEnumerationValue(t)
        except ValueError:
            raise UnsupportedTransportError(t)
        if type_ == eIpcTransportType.MQUEUE:
            if e_head_type == eHeadType.NECK:
                return IpcTransportDetailsFactory.getStatic(ipcConfig, e_head_type)
            return QueueTransportDetails()
        raise UnsupportedTransportError(type_)
