
from epyrpc.api.eo_v1.impl.common.testManagement.NoStatError import NoStatError
from epyrpc.api.eo_v1.interfaces.common.peers.iPeerStatsResult import \
    iPeerStatsResult
import copy

_INDEX_PREFIX = u"INDEX"
_INDEX_TOTAL = "TOTAL"
_INDEX_DEAD = u"DEAD"
_INDEX_CANNOT_REVIVE = u"CANNOT_REVIVE"
_INDEX_UNRESPONSIVE = u"UNRESPONSIVE"
_INDEX_CANNOT_REBOOT = u"CANNOT_REBOOT"
_INDEX_REBOOTING = u"REBOOTING"
_INDEX_PENDING = u"PENDING"
_INDEX_SYNC_CODE = u"SYNC_CODE"
_INDEX_ACTIVE = u"ACTIVE"
_INDEX_TESTING = u"TESTING"

_blankStats = { _INDEX_DEAD:0,
                _INDEX_CANNOT_REVIVE:0,
                _INDEX_UNRESPONSIVE:0,
                _INDEX_CANNOT_REBOOT:0,
                _INDEX_REBOOTING:0,
                _INDEX_PENDING:0,
                _INDEX_SYNC_CODE:0,
                _INDEX_ACTIVE:0,
                _INDEX_TESTING:0,
               }

class PeerStatsResult(iPeerStatsResult):
    INDEX_TOTAL = _INDEX_TOTAL
    INDEX_DEAD = _INDEX_DEAD
    INDEX_CANNOT_REVIVE = _INDEX_CANNOT_REVIVE
    INDEX_UNRESPONSIVE = _INDEX_UNRESPONSIVE
    INDEX_CANNOT_REBOOT = _INDEX_CANNOT_REBOOT
    INDEX_REBOOTING = _INDEX_REBOOTING
    INDEX_PENDING = _INDEX_PENDING
    INDEX_SYNC_CODE = _INDEX_SYNC_CODE
    INDEX_ACTIVE = _INDEX_ACTIVE
    INDEX_TESTING = _INDEX_TESTING
    _indexes = []
    def __init__(self, stats=_blankStats, flush=False):
        self._stats = stats
        self._noraise = False
        self._flush = None  #    Guarantee default value.
        self.flushed = flush
        if len(PeerStatsResult._indexes) == 0:
            #    Calculate the available indexes:
            for i in dir(PeerStatsResult):
                if i.isupper() and i.startswith(_INDEX_PREFIX):
                    PeerStatsResult._indexes.append(i)
    def getItems(self):
        return self._indexes
    def stats(self):
        return self._stats
    def export(self):
        return PeerStatsResult(copy.deepcopy(self._stats))
    @staticmethod
    def compute(peers, flush=False):
        r"""
        @summary: Compile the stats from an array of CachedPeerDetails objects.
        @static-constructor.
        @type peers: dict.
        """
        result = PeerStatsResult(flush=flush)
        if peers == None:
            result.total = 0
            return result
        r""" Calculate stats... """
        #    #Total peers:
        result.total = len(peers.keys())
        #    Only generate other stats if we have any peers (setters will raise Exceptions otherwise).
        if result.total > 0:
            dead = cannotRevive = unresponsive = cannotReboot = rebooting = pending = syncCode = active = testing = 0
            for peer in peers.values():
                peer = peer.peer()
                state = peer.state
                if state == ActivePeerState.DEAD:
                    dead += 1
                elif state == ActivePeerState.CANNOT_REVIVE():
                    cannotRevive += 1
                elif state == ActivePeerState.UNRESPONSIVE():
                    unresponsive += 1
                elif state == ActivePeerState.CANNOT_REBOOT():
                    cannotReboot += 1
                elif state == ActivePeerState.REBOOTING():
                    rebooting += 1
                elif state == ActivePeerState.PENDING():
                    pending += 1
                elif state == ActivePeerState.SYNC_CODE():
                    syncCode += 1
                elif state == ActivePeerState.ACTIVE():
                    active += 1
                elif state == ActivePeerState.TESTING():
                    testing += 1
            #    Set the stats:
            result.dead = dead
            result.cannotRevive = cannotRevive
            result.unresponsive = unresponsive
            result.cannotReboot = cannotReboot
            result.rebooting = rebooting
            result.pending = pending
            result.syncCode = syncCode
            result.active = active
            result.testing = testing
        return result
    r""" SETTERS & GETTERS for properties: """
    def setFlushed(self, flush):
        if not isinstance(flush, bool):
            raise ValueError("flush must be a boolean, but got: %(F)s" % {"F":flush})
        self._flush = flush
    def setTotal(self, total):
        self._setStats(PeerStatsResult.INDEX_TOTAL, total)
    def setDead(self, total):
        self._setStats(PeerStatsResult.INDEX_DEAD, total)
    def setCannotRevive(self, total):
        self._setStats(PeerStatsResult.INDEX_CANNOT_REVIVE, total)
    def setCannotReboot(self, total):
        self._setStats(PeerStatsResult.INDEX_CANNOT_REBOOT, total)
    def setRebooting(self, total):
        self._setStats(PeerStatsResult.INDEX_REBOOTING, total)
    def setPending(self, total):
        self._setStats(PeerStatsResult.INDEX_PENDING, total)
    def setSyncCode(self, total):
        self._setStats(PeerStatsResult.INDEX_SYNC_CODE, total)
    def setActive(self, total):
        self._setStats(PeerStatsResult.INDEX_ACTIVE, total)
    def setTesting(self, total):
        self._setStats(PeerStatsResult.INDEX_TESTING, total)
    def getFlushed(self):
        return self._flush
    def getTotal(self):
        return self._getStat(PeerStatsResult.INDEX_TOTAL)
    def getDead(self):
        return self._getStat(PeerStatsResult.INDEX_DEAD)
    def getCannotRevive(self):
        return self._getStat(PeerStatsResult.INDEX_CANNOT_REVIVE)
    def getCannotReboot(self):
        return self._getStat(PeerStatsResult.INDEX_CANNOT_REBOOT)
    def getRebooting(self):
        return self._getStat(PeerStatsResult.INDEX_REBOOTING)
    def getPending(self):
        return self._getStat(PeerStatsResult.INDEX_PENDING)
    def getSyncCode(self):
        return self._getStat(PeerStatsResult.INDEX_SYNC_CODE)
    def getActive(self):
        return self._getStat(PeerStatsResult.INDEX_ACTIVE)
    def getTesting(self):
        return self._getStat(PeerStatsResult.INDEX_TESTING)
    r""" PROPERTIES: """
    flushed = property(getFlushed, setFlushed)
    total = property(getTotal, setTotal)
    dead = property(getDead, setDead)
    cannotRevive = property(getCannotRevive, setCannotRevive)
    cannotReboot = property(getCannotReboot, setCannotReboot)
    rebooting = property(getRebooting, setRebooting)
    pending = property(getPending, setPending)
    syncCode = property(getSyncCode, setSyncCode)
    active = property(getActive, setActive)
    testing = property(getTesting, setTesting)
    r""" MISC: """
    def _getStat(self, index):
        if index not in self._stats:
            raise KeyError("Cannot get stats for: %(W)s" % {"W":index})
        if (index != PeerStatsResult.INDEX_TOTAL) and (self.total == 0):
            if self._noraise == False:
                raise NoStatError("Cannot get stat: %(W)s when there are no peers!" % {"W":index})
            return 0
        return self._stats[index]
    def _setStats(self, index, value):
        if value == None or value < 0:
            value = 0
        self._stats[index] = value
    def setNoRaise(self, enabler=True):
        self._noraise = bool(enabler)
        pass



