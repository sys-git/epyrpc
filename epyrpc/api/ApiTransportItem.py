
from epyrpc.api.iApiTransportItem import iApiTransportItem

class ApiTransportItem(iApiTransportItem):
    def __init__(self, ns, args, kwargs, synchronous=True):
        self._ns = ns
        self._args = args
        self._kwargs = kwargs
        self._synchronous = synchronous
    def ns(self):
        return self._ns
    def args(self):
        return self._args
    def kwargs(self):
        return self._kwargs
    def synchronous(self):
        return self._synchronous
    def async(self, enabler=True):
        self._synchronous = enabler
