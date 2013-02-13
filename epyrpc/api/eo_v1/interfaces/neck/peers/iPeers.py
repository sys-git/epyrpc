
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iPeers(iApi):
    """ CALLABLES-EVENTS: """
    def peerStateChange(self, thePeer):
        r"""
        @summary: A Peer state-change has occurred, propagate back to the 'other-side'.
        """
        raise NotImplementedException("iPeer.peerStateChange")
    def peerStatsChange(self, i_peer_stats_result):
        r"""
        @summary: Peer stats have changed, propagate back to the 'other-side'.
        """
        raise NotImplementedException("iPeer.peerStatsChange")
    r""" HANDLERS: """
    def _handler_add(self, tId, bSynchronous, i_a_peer):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Add one or more Peers.
        @param i_a_peer: [iAPeer] or iAPeer
        @raise ApiParamError: Error in parameters.
        @return: dict{iAPeer:iPeer}
        @TODO: Implement adding of Peer.
        @see: PeerChecker
        """
        raise NotImplementedException("iPeer._handler_add")
    def _handler_remove(self, tId, bSynchronous, i_a_peer_remover):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Remove one or more Peers.
        @param i_a_peer_remover: [iAPeerRemover] or iAPeerRemover
        @raise ApiParamError: Error in parameters.
        @return: dict{iAPeer:iPeer}
        @TODO: Implement removing of Peer.
        @see: PeerChecker
        """
        raise NotImplementedException("iPeer._handler_remove")
    def _handler_stats(self, tId, bSynchronous):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Remove one or more Peers.
        @return: iPeerStatsResult
        @TODO: Implement Peer stats.
        @see: PeerChecker
        """
        raise NotImplementedException("iPeer._handler_stats")
    def _handler_query(self, tId, bSynchronous, i_a_peer):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Query the given peers.
        @param i_a_peer: The Peers to query?
        @raise ApiParamError: Error in parameters.
        @return: dict{iAPeer:iAPeer(for now)}
        @TODO: Implement Peer query.
        @see: PeerChecker
        """
        raise NotImplementedException("iPeer._handler_query")
    def _handler_queryAll(self, tId, bSynchronous):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Query ALL peers.
        @return: dict{iAPeer:iAPeer(for now)}
        @TODO: Implement all Peers query.
        @see: PeerChecker
        """
        raise NotImplementedException("iPeer._handler_queryAll")
