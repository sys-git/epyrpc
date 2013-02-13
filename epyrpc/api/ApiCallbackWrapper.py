
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.utils.LogManager import LogManager

class ApiCallbackWrapper(object):
    logger = LogManager().getLogger("ApiCbWrapper")
    def __init__(self, cb):
        self._callback = cb
    def _cb(self, tId, result):
        originalResult = result
        result = ApiTransportResponse.decode(result)
        ApiCallbackWrapper.logger.debug("Decoded %(T)s." % {"T":tId, "O":originalResult, "N":result})
        #    Now call the original callback:
        return self._callback(tId, result)
    def cb(self):
        return self._cb
    @staticmethod
    def callback(cb):
        if cb == None:
            return None
        wrapper = ApiCallbackWrapper(cb)
        ApiCallbackWrapper.logger.debug("Created callback wrapper.")
        return wrapper.cb()

