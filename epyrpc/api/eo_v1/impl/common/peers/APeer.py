
from epyrpc.api.eo_v1.interfaces.common.peers.iAPeer import iAPeer

class APeer(iAPeer):
    def __init__(self, peerId):
        self._macAddress = peerId
    def macAddress(self):
        return self._macAddress
    def export(self):
        return APeer(self._macAddress)
