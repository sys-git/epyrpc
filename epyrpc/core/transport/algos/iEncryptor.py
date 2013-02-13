
from epyrpc.core.transport.algos.iAlgoImpl import iAlgoImpl

class iEncryptor(iAlgoImpl):
    DEFAULT_ORDER = 1
    FORMAT_ID__ENCRYPTOR = "encryptor"
    def __init__(self, *args, **kwargs):
        super(iEncryptor, self).__init__(*args, **kwargs)
        self._format.append(iEncryptor.FORMAT_ID__ENCRYPTOR)
