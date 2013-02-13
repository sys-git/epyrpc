
from epyrpc.api.eo_v1.enums.eLoggingState import eLoggingState
from epyrpc.api.eo_v1.interfaces.common.tas.logging.iLoggingResult import \
    iLoggingResult

class LoggingResult(iLoggingResult):
    def __init__(self, state, location):
        self._state = state
        self._location = location
    def location(self):
        return self._location
    def isOn(self):
        return self._state == eLoggingState.ON
    def export(self):
        return LoggingResult(self.location(), self._state)
