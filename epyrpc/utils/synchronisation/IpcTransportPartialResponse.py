
class IpcTransportPartialResponse(object):
    def __init__(self, tId, combinerMethod, index, numChunks, response):
        self._tId = tId
        self._combinerMethod = combinerMethod
        self._index = index
        self._numChunks = numChunks
        self._response = response
    def tId(self):
        return self._tId
    def index(self):
        return self._index
    def numChunks(self):
        return self._numChunks
    def combinerMethod(self):
        return self._combinerMethod
    def response(self):
        return self._response
