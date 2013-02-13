
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.checkers.peers.PeersChecker import PeersChecker
from epyrpc.api.eo_v1.impl.common.peers.APeer import APeer
from epyrpc.api.eo_v1.impl.common.peers.PeerResult import PeerResult
from epyrpc.api.eo_v1.interfaces.neck.peers.iPeers import iPeers
from epyrpc.api.eo_v1.enums.ePeerRemoval import ePeerRemoval
import copy

class Peers(iPeers):
    def __init__(self, ns="", solicited=False, ipc=None):
        super(Peers, self).__init__(ns=ns, solicited=solicited)

    # CALLABLES-EVENTS
    def peerStateChange(self, thePeers):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, peers=PeersChecker.checkStateChange(thePeers))

    def peerStatsChange(self, i_peer_stats_result):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited,
            stats=PeersChecker.checkStatsChange(i_peer_stats_result))

    def newPeers(self, newPeers):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, peers=PeersChecker.checkNewPeers(newPeers))

    def peerHeartbeat(self, peer):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()),
            self.solicited, peer=PeersChecker.checkHeartbeat(peer))

    """ HANDLERS: """
    def _handler_add(self, tId, bSynchronous, i_a_peer):
        i_a_peer = self._handleStandardCheck(tId, bSynchronous, PeersChecker.checkAdd, i_a_peer)
        def _add(i_a_peer):
            result = {}
            for peer in i_a_peer:
                try:
                    #    TODO: Remove peer from the ExecutionOrganiser, return ok/err-code for each attempt.
                    #    TODO: Eventual PeerStateChange api will be called.
                    macAddress = peer.macAddress()
                    response = APeer(macAddress)
                    self._logger.info("TODO: Request to add peer with mac address: %(M)s, method: %(T)s" % {"M":macAddress})
                except Exception, response: pass
                result[peer] = response
            return PeerResult(result)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _add(x), i_a_peer)
    def _handler_remove(self, tId, bSynchronous, i_a_peer_remover):
        i_a_peer_remover = self._handleStandardCheck(tId, bSynchronous, PeersChecker.checkRemove, i_a_peer_remover)
        def _remove(i_a_peer_remover):
            result = {}
            for remover in i_a_peer_remover:
                try:
                    #    TODO: Remove peer: 'remover.peer()' from the ExecutionOrganiser, return ok/err-code for each attempt.
                    #    TODO: Eventual PeerStateChange api will be called.
                    peer = remover.peer()
                    macAddress = peer.macAddress()
                    how = remover.how()
                    howMethod = ePeerRemoval.enumerateAttributes(how)
                    self._logger.info("TODO: Request to remove peer with mac address: %(M)s, method: %(H)s" % {"H":howMethod, "M":macAddress})
                    pass
                    response = APeer(macAddress)
                except remover, response: pass
                result[remover] = response
            return PeerResult(result)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _remove(x), i_a_peer_remover)
    def _handler_stats(self, tId, bSynchronous):
        def _stats():
            stats = copy.deepcopy(ExecutionOrganiser().getCache().getStats())
            #    Return the 'peer' stats only!
            return stats.peerStats()
        return self._handleStandardCall(tId, bSynchronous, _stats)
    def _handler_query(self, tId, bSynchronous, list__i_a_peer):
        list__i_a_peer = self._handleStandardCheck(tId, bSynchronous, PeersChecker.checkQuery, list__i_a_peer)
        def _query(list__i_a_peer):
            result = {}
            thePeers = copy.deepcopy(ExecutionOrganiser().getCache().getAllPeers())
            for peer in list__i_a_peer:
                macAddress = peer.macAddress()
                try:
                    response = thePeers[macAddress]
                except Exception, response:
                    pass
                result[macAddress] = response
            return result
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _query(x), list__i_a_peer)
    def _handler_queryAll(self, tId, bSynchronous):
        def _queryAll():
            return copy.deepcopy(ExecutionOrganiser().getCache().getAllPeers())
        return self._handleStandardCall(tId, bSynchronous, _queryAll)

