
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iLogging(iApi):
    def turnOn(self):
        r"""
        @summary: Turn logging ON.
        @see: iLogging.turnOn()
        @return: iLoggingResult
        """
        raise NotImplementedException("iConfiguration.turnOn")
    def turnOff(self):
        r"""
        @summary: Turn logging OFF.
        @see: iLogging.turnOff()
        @return: iLoggingResult
        """
        raise NotImplementedException("iConfiguration.turnOff")
    def query(self):
        r"""
        @summary: Query logging state and location.
        @return: iLoggingResult
        """
        raise NotImplementedException("iConfiguration .query")
