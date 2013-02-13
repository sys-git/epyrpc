
from epyrpc.core.transport.algos.iAlgo import iAlgo

class iAlgoImpl(iAlgo):
    FORMAT_ID__ALGO = "algo"
    def __init__(self, order=0):
        self._worker = None
        self._order = order
        self._format = [iAlgoImpl.FORMAT_ID__ALGO]
    def setWorker(self, worker):
        self._worker = worker
    def order(self):
        return self._order
    def setOrder(self, order):
        self._order = order
    def getFormat(self):
        r"""
        @summary: Return something that allows
        us to decode the packaged message.
        """
        if self._worker != None:
            workerFormat = self._worker.getFormat()
            result = ".".join(workerFormat + self._format)
        else:
            result = self._format
        return result
