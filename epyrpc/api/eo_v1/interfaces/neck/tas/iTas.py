
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iTas(iApi):
    r""" CALLABLES-EVENTS: """
    def signal(self, *args, **kwargs):
        r"""
        @summary: A signal is received and filtered-in.
        """
        raise NotImplementedException("iTasHandler.signal")
    def error(self, error):
        r"""
        @summary: An Error is received.
        """
        raise NotImplementedException("iTasHandler.error")
    def engineStateChange(self, uId, newState, previousState):
        r"""
        @summary: An ExecutionOrganiser EngineStateChange is received.
        """
        raise NotImplementedException("iTasHandler.engineStateChange")
    def sigInt(self):
        r"""
        @summary: A Signal-Interrupt (Ctrl-C) is received.
        """
        raise NotImplementedException("iTasHandler.sigInt")
    def statsChange(self):
        r"""
        @summary: A Stats-Change event is received.
        """
        raise NotImplementedException("iTasHandler.statsChange")
    r""" HANDLERS: """
    def _handler_stats(self, tId, bSynchronous):
        r"""
        @summary: Query ALL the stats (peer and test).
        @return: iStatsResult.
        """
        raise NotImplementedException("iTasStats._handler_stats")
