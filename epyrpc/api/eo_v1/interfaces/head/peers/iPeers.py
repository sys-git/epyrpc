
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iPeers(iApi):
    r"""
    @note: These 'EVENT_*' are api's that the caller can register
    it's own handler to receive.
    @attention: It is critically important that these strings are IDENTICAL
    to the method names in the relevant api: peers.py
    """
    EVENT__PEER_STATE_CHANGE = u"peerStateChange"
    EVENT__PEER_STATS_CHANGE = u"peerStatsChange"
    EVENT__PEERS_NEW = u"newPeers"
    EVENT__PEER_HEARTBEAT = u"peerHeartbeat"
    """ CALLABLES-ACTIONS: """
    def add(self, i_a_peer):
        r"""
        @summary: Add one or more Peers.
        @param i_a_peer: [iAPeer] or iAPeer to add to the ExecutionOrganiser.
        @raise ApiParamError: Error in parameters.
        @return: dict{iAPeer:iAPeer(for now)}
        """
        raise NotImplementedException("iPeer.add")
    def remove(self, i_a_peer):
        r"""
        @summary: Remove one or more Peers.
        @param i_a_peer_remover: [iAPeerRemover] or iAPeerRemover to remove from the ExecutionOrganiser.
        @raise ApiParamError: Error in parameters.
        @return: dict{iAPeerRemover:iAPeer(for now)}
        """
        raise NotImplementedException("iPeer.remove")
    def stats(self, i_peer_stats):
        r"""
        @summary: Get the peer stats.
        @param i_peer_stats: The stats to query?
        @raise ApiParamError: Error in parameters.
        @return: iPeerStatsResult
        """
        raise NotImplementedException("iPeer.stats")
    def query(self, i_a_peer):
        r"""
        @summary: Query the given peers.
        @param i_a_peer: The Peers to query?
        @raise ApiParamError: Error in parameters.
        @return: dict{iAPeer:iAPeer(for now)}
        """
        raise NotImplementedException("iPeer.query")
    def queryAll(self):
        r"""
        @summary: Query ALL peers.
        @return: dict{iAPeer:iAPeer(for now)}
        """
        raise NotImplementedException("iPeer.queryAll")

