
from epyrpc.core.transport.algos.UnsupportedTransportCompressionError import \
    UnsupportedTransportCompressionError
from epyrpc.core.transport.algos.UnsupportedTransportEncryptionError import \
    UnsupportedTransportEncryptionError
from epyrpc.core.transport.algos.compression.NoCompressor import NoCompressor
from epyrpc.core.transport.algos.compression.ZlibCompressor import ZlibCompressor
from epyrpc.core.transport.algos.encryption.NoEncryption import NoEncryption

class TransportDataAlgoFactory(object):
    @staticmethod
    def get(packagerDetails=None):
        r"""
        @summary: Obtain a packager: iAlgo, to package and extract data over a
        given channel.
        """
        compressor = NoCompressor()
        encryptor = NoEncryption()
        if packagerDetails != None:
            (compression, encryption) = packagerDetails
            if compression != None:
                if compression.enable.PCDATA.lower() == "true":
                    algo = compression.algo.PCDATA.lower()
                    if algo == "zlib":
                        compressor = ZlibCompressor(compression.args)
                    else:
                        raise UnsupportedTransportCompressionError(algo)
            if encryption != None:
                if encryption.enable.PCDATA.lower() == "true":
                    algo = encryption.algo.PCDATA.lower()
                    raise UnsupportedTransportEncryptionError(algo)
        #    Now nest the compressor (default prioritised) and encryptor as specified by the config:
        orders = {}
        if compressor.order() == encryptor.order():
            encryptor.setOrder(compressor.order() + 1)
        orders[compressor.order()] = compressor
        orders[encryptor.order()] = encryptor
        keys = orders.keys()
        keys.sort()
        primary = orders[keys[0]]
        worker = orders[keys[1]]
        #   Now return the nested worker:
        primary.setWorker(worker)
        return primary

