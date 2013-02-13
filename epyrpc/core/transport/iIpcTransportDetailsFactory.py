
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iIpcTransportDetailsFactory(Interface):
    @staticmethod
    def getStatic(ipcConfig, e_head_type):
        raise NotImplementedException("iIpcTransportDetailsFactory.getStatic")
    @staticmethod
    def get(ipcConfig, e_head_type):
        raise NotImplementedException("iIpcTransportDetailsFactory.get")
