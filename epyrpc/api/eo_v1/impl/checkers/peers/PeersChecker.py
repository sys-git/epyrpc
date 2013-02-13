
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.checkers.peers.iPeersChecker import iPeersChecker
from epyrpc.api.eo_v1.interfaces.common.peers.iAPeer import iAPeer
from epyrpc.api.eo_v1.interfaces.common.peers.iAPeerRemover import iAPeerRemover
from epyrpc.api.eo_v1.interfaces.common.peers.iPeerStats import iPeerStats
from epyrpc.api.eo_v1.interfaces.common.peers.iPeerStatsResult import \
    iPeerStatsResult

class PeersChecker(iPeersChecker):
    r"""
    @summary: Check the params for the api.peer methods.
    """
    allowedTypes = {"checkHeartbeat":[CachedPeerDetails], "checkNewPeers":[dict], "checkStateChange":[CachedPeerDetails], "add":[list, iAPeer], "remove":[list, iAPeerRemover], "stats":[iPeerStats], "peerStateChange":[iPeerStatsResult]}
    @staticmethod
    def checkAdd(i_a_peer):
        return PeersChecker._checkPeer(i_a_peer)

    @staticmethod
    def _checkPeer(i_a_peer):
        if not isinstance(i_a_peer, list):
            raise ApiParamError(i_a_peer, PeersChecker.allowedTypes["add"])

        newArgs = []
        for i in i_a_peer:
            if i == None: continue

            if not isinstance(i, iAPeer):
                raise ApiParamError(i, PeersChecker.allowedTypes["add"])
            newArgs.append(i)

        if len(newArgs) == 0:
            raise ApiParamError(i_a_peer, PeersChecker.allowedTypes["add"])
        return newArgs

    @staticmethod
    def checkRemove(i_a_peer_remove):
        if not isinstance(i_a_peer_remove, list):
            raise ApiParamError(i_a_peer_remove, PeersChecker.allowedTypes["remove"])
        newArgs = []
        for i in i_a_peer_remove:
            if i != None:
                if not isinstance(i, iAPeerRemover):
                    raise ApiParamError(i, PeersChecker.allowedTypes["remove"])
                newArgs.append(i)
        if len(newArgs) == 0:
            raise ApiParamError(i_a_peer_remove, PeersChecker.allowedTypes["remove"])
        return newArgs
    @staticmethod
    def checkQuery(i_a_peer):
        return PeersChecker._checkPeer(i_a_peer)
    @staticmethod
    def checkStateChange(thePeers):
        if not isinstance(thePeers, dict):
            raise ApiParamError(thePeers, PeersChecker.allowedTypes["checkStateChange"])
        for i in thePeers.values():
            if not isinstance(i, CachedPeerDetails):
                raise ApiParamError(i, PeersChecker.allowedTypes["checkStateChange"])
        return thePeers
    @staticmethod
    def checkStatsChange(i_peer_stats_result):
        if not isinstance(i_peer_stats_result, iPeerStatsResult):
            raise ApiParamError(i_peer_stats_result, PeersChecker.allowedTypes["peerStateChange"])
        return i_peer_stats_result
    @staticmethod
    def checkNewPeers(peers):
        if not isinstance(peers, dict):
            raise ApiParamError(peers, PeersChecker.allowedTypes["checkNewPeers"])
        newPeers = {}
        for macAddress, i in peers.items():
            if not isinstance(i, CachedPeerDetails):
                raise ApiParamError(i, PeersChecker.allowedTypes["checkNewPeers"])
            newPeers[macAddress] = i
        if len(newPeers.keys()) == 0:
            raise ApiParamError(newPeers, PeersChecker.allowedTypes["checkNewPeers"])
        return newPeers
    @staticmethod
    def checkHeartbeat(peer):
        if not isinstance(peer, CachedPeerDetails):
            raise ApiParamError(peer, PeersChecker.allowedTypes["checkHeartbeat"])
        return peer
