
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iStats(iApi):
    """ HANDLERS: """
    def statsChange(self, i_stats_result):
        r"""
        @summary: A stats change has occurred, propagate back to the 'other-side'.
        @return: N/A.
        """
        raise NotImplementedException("iStats.statsChange")
