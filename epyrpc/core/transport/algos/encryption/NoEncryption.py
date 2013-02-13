
from epyrpc.core.transport.algos.iEncryptor import iEncryptor

class NoEncryption(iEncryptor):
    FORMAT_ID__PASSTHROUGH_ENCRYPTION = "passthrough"
    def __init__(self, *args, **kwargs):
        super(NoEncryption, self).__init__(*args, **kwargs)
        self._format.append(NoEncryption.FORMAT_ID__PASSTHROUGH_ENCRYPTION)
    def extract(self, data, hint=None):
        if self._worker != None:
            data = self._worker.extract(data)
        return data
    def package(self, data):
        if self._worker != None:
            data = self._worker.package(data)
        return data

