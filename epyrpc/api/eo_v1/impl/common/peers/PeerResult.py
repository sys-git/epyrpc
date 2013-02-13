
from epyrpc.api.eo_v1.interfaces.common.peers.iPeerResult import iPeerResult
from epyrpc.api.iApiData import iApiData

class PeerResult(iPeerResult):
    def __init__(self, peers):
        self._peers = peers
    def peers(self):
        return self._peers
    def count(self):
        return len(self._peers.keys())
    def export(self):
        peers = {}
        for key, value in self._peers.items():
            if isinstance(value, iApiData):
                peers[key] = value.export()
            elif isinstance(value, Exception):
                peers[key] = value
            else:
                raise Exception("No idea how to export this data: key: <%(K)s>, value: <%(V)s>" % {"K":key, "V":value})
        return PeerResult(peers)
