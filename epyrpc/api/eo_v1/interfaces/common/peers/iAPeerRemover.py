
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iAPeerRemover(iApiData):
    def peer(self):
        r"""
        @return: The Peer to remove
        """
        raise NotImplementedException("iAPeerRemover.peer")
    def how(self):
        r"""
        @return: The e_peer_removal method
        """
        raise NotImplementedException("iAPeerRemover.method")
