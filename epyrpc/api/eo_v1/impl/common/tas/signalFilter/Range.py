
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iRange import iRange
import itertools

class Range(iRange):
    _uId = itertools.count(0)
    def __init__(self, start=None, end=None, chunkSize=16000, userData=None):
        self._start = start
        self._end = end
        self._chunkSize = chunkSize
        if userData == None:
            userData = Range._uId.next()
        self._userData = userData
    def start(self):
        return self._start
    def end(self):
        return self._end
    def chunkSize(self):
        return self._chunkSize
    def userData(self):
        return self._userData
