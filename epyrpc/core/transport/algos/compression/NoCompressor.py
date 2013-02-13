
from epyrpc.core.transport.algos.iCompressor import iCompressor

class NoCompressor(iCompressor):
    FORMAT_ID__PASSTHROUGH_COMPRESSOR = "passthrough"
    def __init__(self, *args, **kwargs):
        super(NoCompressor, self).__init__(*args, **kwargs)
        self._format.append(NoCompressor.FORMAT_ID__PASSTHROUGH_COMPRESSOR)
    def extract(self, data, hint=None):
        if self._worker != None:
            data = self._worker.extract(data)
        return data
    def package(self, data):
        if self._worker != None:
            data = self._worker.package(data)
        return data

