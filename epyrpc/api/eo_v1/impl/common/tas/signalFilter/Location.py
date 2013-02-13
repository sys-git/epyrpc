
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iLocation import iLocation

class Location(iLocation):
    def __init__(self, filename=None, theFormat=None, copyExisting=True):
        self._filename = filename
        self._format = theFormat
        self._copyExisting = copyExisting
    def filename(self):
        return self._filename
    def theFormat(self):
        return self._format
    def copyExisting(self):
        return self._copyExisting
