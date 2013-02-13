
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iStats(iApi):
    """ HANDLERS: """
    def statsChange(self, i_stats_result):
        r"""
        @summary: A stats change has occurred, propagate back to the 'other-side'.
        @return: N/A.
        """
        raise NotImplementedException("iStats.statsChange")
