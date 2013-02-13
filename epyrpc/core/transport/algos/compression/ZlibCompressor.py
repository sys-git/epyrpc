
from epyrpc.core.transport.algos.compression.NoCompressor import NoCompressor
import zlib

class ZlibCompressor(NoCompressor):
    DEFAULT_LEVEL = 5
    FORMAT_ID__ZLIB_COMPRESSOR = "zlib"
    def __init__(self, args):
        level = ZlibCompressor.DEFAULT_LEVEL
        order = ZlibCompressor.DEFAULT_ORDER
        if hasattr(args, "level"):
            level = int(args.level.PCDATA)
        self._level = level
        if hasattr(args, "order"):
            order = int(args.order.PCDATA)
        super(ZlibCompressor, self).__init__(order)
        self._engine = zlib
        self._format[-1] = ZlibCompressor.FORMAT_ID__ZLIB_COMPRESSOR
    def extract(self, data, hint=None):
        data = super(ZlibCompressor, self).extract(data)
        data = self._engine.decompress(data)
        return data
    def package(self, data):
        data = self._engine.compress(data, self._level)
        data = super(ZlibCompressor, self).package(data)
        return data

