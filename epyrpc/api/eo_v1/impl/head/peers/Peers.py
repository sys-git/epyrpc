
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.peers.PeersChecker import PeersChecker
from epyrpc.api.eo_v1.interfaces.head.peers.iPeers import iPeers

class Peers(iPeers):
    def __init__(self, ns="", solicited=True, ipc=None):
        super(Peers, self).__init__(ns=ns, solicited=solicited)
    """ CALLABLES-ACTIONS: """
    def add(self, i_a_peer):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, PeersChecker.checkAdd(i_a_peer))
    def remove(self, i_a_peer_remove):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, PeersChecker.checkRemove(i_a_peer_remove))
    def stats(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def query(self, i_a_peer):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, PeersChecker.checkQuery(i_a_peer))
    def queryAll(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
