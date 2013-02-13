
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iAlgo(Interface):
    def extract(self, data, hint=None):
        raise NotImplementedException("iAlgoImpl.extract")
    def package(self, data):
        raise NotImplementedException("iAlgoImpl.package")
