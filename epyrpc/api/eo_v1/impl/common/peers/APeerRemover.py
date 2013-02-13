
from epyrpc.api.eo_v1.interfaces.common.peers.iAPeerRemover import iAPeerRemover
from epyrpc.api.eo_v1.enums.ePeerRemoval import ePeerRemoval

class APeerRemover(iAPeerRemover):
    def __init__(self, i_a_peer, how=ePeerRemoval.IMMEDIATELY):
        self._peer = i_a_peer
        self._how = how
    def peer(self):
        return self._peer
    def how(self):
        return self._how
    def export(self):
        return APeerRemover(self._peer, self._how)
