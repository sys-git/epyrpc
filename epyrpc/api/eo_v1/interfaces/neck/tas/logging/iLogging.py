
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iLogging(iApi):
    def _handler_turnOn(self, tId, bSynchronous):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Turn logging ON.
        @see: iLogging._handler_turnOn()
        @return: iLoggingResult
        """
        raise NotImplementedException("iConfiguration._handler_turnOn")
    def _handler_turnOff(self, tId, bSynchronous):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Turn logging OFF.
        @see: iLogging._handler_turnOff()
        @return: iLoggingResult
        """
        raise NotImplementedException("iConfiguration._handler_turnOff")
    def _handler_query(self, tId, bSynchronous):
        r"""
        @summary: Query logging state and location.
        @return: iLoggingResult
        """
        raise NotImplementedException("iConfiguration ._handler_query")
