    
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iTas(iApi):
    r"""
    @note: These 'EVENT_*' are api's that the caller can register
    it's own handler to receive.
    @attention: It is critically important that these strings are IDENTICAL
    to the method names in the relevant api: tas.py
    """
    EVENT__SIGNAL = u"signal"
    EVENT__ERROR = u"error"
    EVENT__ENGINE_STATE_CHANGE = u"engineStateChange"
    EVENT__SIGN_INT = u"sigInt"
    EVENT__STATS_CHANGE = "statsChange"
    def stats(self):
        r"""
        @summary: Query ALL the stats (peer and test).
        @return: iStatsResult.
        """
        raise NotImplementedException("iTas.stats")
