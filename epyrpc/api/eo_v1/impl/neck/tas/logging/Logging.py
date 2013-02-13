
from epyrpc.api.eo_v1.impl.common.tas.LoggingResult import LoggingResult
from epyrpc.api.eo_v1.interfaces.head.tas.logging.iLogging import iLogging
from epyrpc.utils.LogManager import LogManager

class Logging(iLogging):
    def __init__(self, ns="", solicited=True):
        super(Logging, self).__init__(ns=ns, solicited=solicited)
    """ HANDLERS: """
    def  _handler_turnOn(self, tId, bSynchronous):
        def _turnOn():
            lm = LogManager()
            lm.turnOnLogging()
            return LoggingResult(lm.isOn(), LogManager.FILENAME)
        return self._handleStandardCall(tId, bSynchronous, _turnOn)
    def  _handler_turnOff(self, tId, bSynchronous):
        def _turnOff():
            lm = LogManager()
            lm.turnOffLogging()
            return LoggingResult(lm.isOn(), LogManager.FILENAME)
        return self._handleStandardCall(tId, bSynchronous, _turnOff)
    def  _handler_query(self, tId, bSynchronous):
        def _query():
            lm = LogManager()
            return LoggingResult(lm.isOn(), LogManager.FILENAME)
        return self._handleStandardCall(tId, bSynchronous, _query)
