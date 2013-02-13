
from epyrpc.core.transport.algos.iAlgoImpl import iAlgoImpl

class iCompressor(iAlgoImpl):
    DEFAULT_ORDER = 0
    FORMAT_ID__COMPRESSOR = "compressor"
    def __init__(self, *args, **kwargs):
        super(iCompressor, self).__init__(*args, **kwargs)
        self._format.append(iCompressor.FORMAT_ID__COMPRESSOR)
