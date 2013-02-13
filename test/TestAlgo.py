
from epyrpc.core.transport.algos.TransportDataAlgoFactory import \
    TransportDataAlgoFactory
from epyrpc.core.transport.algos.UnsupportedTransportCompressionError import \
    UnsupportedTransportCompressionError
from epyrpc.core.transport.algos.UnsupportedTransportEncryptionError import \
    UnsupportedTransportEncryptionError
from epyrpc.core.transport.algos.compression.NoCompressor import NoCompressor
from epyrpc.core.transport.algos.compression.ZlibCompressor import ZlibCompressor
from epyrpc.core.transport.algos.encryption.NoEncryption import NoEncryption
from epyrpc.core.transport.algos.iAlgoImpl import iAlgoImpl
from epyrpc.core.transport.algos.iCompressor import iCompressor
from epyrpc.core.transport.algos.iEncryptor import iEncryptor
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
import unittest

def _makeFormats():
    eFormats = {}
    eF = []
    eF.append(iAlgoImpl.FORMAT_ID__ALGO)
    eF.append(iEncryptor.FORMAT_ID__ENCRYPTOR)
    eF.append(NoEncryption.FORMAT_ID__PASSTHROUGH_ENCRYPTION)
    eF.append(iAlgoImpl.FORMAT_ID__ALGO)
    eF.append(iCompressor.FORMAT_ID__COMPRESSOR)
    eF.append(NoCompressor.FORMAT_ID__PASSTHROUGH_COMPRESSOR)
    eFormats["None"] = ".".join(eF)
    eF = []
    eF.append(iAlgoImpl.FORMAT_ID__ALGO)
    eF.append(iEncryptor.FORMAT_ID__ENCRYPTOR)
    eF.append(NoEncryption.FORMAT_ID__PASSTHROUGH_ENCRYPTION)
    eF.append(iAlgoImpl.FORMAT_ID__ALGO)
    eF.append(iCompressor.FORMAT_ID__COMPRESSOR)
    eF.append(ZlibCompressor.FORMAT_ID__ZLIB_COMPRESSOR)
    eFormats["zlib_only"] = ".".join(eF)
    eF = []
    eF.append(iAlgoImpl.FORMAT_ID__ALGO)
    eF.append(iCompressor.FORMAT_ID__COMPRESSOR)
    eF.append(ZlibCompressor.FORMAT_ID__ZLIB_COMPRESSOR)
    eF.append(iAlgoImpl.FORMAT_ID__ALGO)
    eF.append(iEncryptor.FORMAT_ID__ENCRYPTOR)
    eF.append(NoEncryption.FORMAT_ID__PASSTHROUGH_ENCRYPTION)
    eFormats["zlib_only_reversed"] = ".".join(eF)
    return eFormats

class TestTransportDataAlgoFactory(unittest.TestCase):
    def setUp(self):
        ConfigurationManager.destroySingleton()
        self.eFormats = _makeFormats()
    def testNoConfig(self):
        algo = TransportDataAlgoFactory.get()
        assert isinstance(algo, iCompressor)
        assert isinstance(algo, NoCompressor)
        worker = algo._worker
        assert isinstance(worker, iEncryptor)
        assert isinstance(worker, NoEncryption)
        #    Now check the format:
        f = algo.getFormat()
        assert f == self.eFormats["None"]
    def testConfigNoneEnabled(self):
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("a").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        packagerDetails = (compression, encryption)
        algo = TransportDataAlgoFactory.get(packagerDetails)
        assert isinstance(algo, iCompressor)
        assert isinstance(algo, NoCompressor)
        worker = algo._worker
        assert isinstance(worker, iEncryptor)
        assert isinstance(worker, NoEncryption)
        #    Now check the format:
        f = algo.getFormat()
        assert f == self.eFormats["None"]
    def testConfigZlibOnly(self):
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("b").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        packagerDetails = (compression, encryption)
        algo = TransportDataAlgoFactory.get(packagerDetails)
        assert isinstance(algo, iCompressor)
        assert isinstance(algo, ZlibCompressor)
        assert algo._level == 9
        worker = algo._worker
        assert isinstance(worker, iEncryptor)
        assert isinstance(worker, NoEncryption)
        #    Now check the format:
        f = algo.getFormat()
        assert f == self.eFormats["zlib_only"]
    def testConfigUnknownCompressor(self):
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("c").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        packagerDetails = (compression, encryption)
        try:
            TransportDataAlgoFactory.get(packagerDetails)
        except UnsupportedTransportCompressionError, e:
            assert e.algo() == "blah"
        else:
            assert False
    def testConfigUnknownEncryptor(self):
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("d").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        packagerDetails = (compression, encryption)
        try:
            TransportDataAlgoFactory.get(packagerDetails)
        except UnsupportedTransportEncryptionError, e:
            assert e.algo() == "blahdblah"
        else:
            assert False

class TestTransportDataAlgoFactoryInvertedOrder(unittest.TestCase):
    r"""
    @attention: Test only relevant when we have an actual encryptor!
    """
    def setUp(self):
        ConfigurationManager.destroySingleton()
        self.eFormats = _makeFormats()
    def testNoConfig(self):
        algo = TransportDataAlgoFactory.get()
        assert isinstance(algo, iCompressor)
        assert isinstance(algo, NoCompressor)
        worker = algo._worker
        assert isinstance(worker, iEncryptor)
        assert isinstance(worker, NoEncryption)
        #    Now check the format:
        f = algo.getFormat()
        eF = self.eFormats["None"]
        assert f == eF
    def testConfigNoneEnabled(self):
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("aa").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        packagerDetails = (compression, encryption)
        algo = TransportDataAlgoFactory.get(packagerDetails)
        assert isinstance(algo, iCompressor)
        assert isinstance(algo, NoCompressor)
        worker = algo._worker
        assert isinstance(worker, iEncryptor)
        assert isinstance(worker, NoEncryption)
        #    Now check the format:
        f = algo.getFormat()
        eF = self.eFormats["None"]
        assert f == eF
    def testConfigZlibOnly(self):
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("bb").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        packagerDetails = (compression, encryption)
        algo = TransportDataAlgoFactory.get(packagerDetails)
        assert isinstance(algo, iCompressor)
        assert isinstance(algo, ZlibCompressor)
        assert algo._level == 5
        worker = algo._worker
        assert isinstance(worker, iEncryptor)
        assert isinstance(worker, NoEncryption)
        #    Now check the format:
        f = algo.getFormat()
        eF = self.eFormats["zlib_only"]
        assert f == eF

if __name__ == '__main__':
    unittest.main()
