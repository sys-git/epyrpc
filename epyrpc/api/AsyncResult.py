
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.api.iAsyncResult import iAsyncResult
import time

class AsyncResult(iAsyncResult):
    r"""
    @summary: This class holds information relating to a pending
    asynchronous response.
    """
    def __init__(self, apiAction, tId):
        self._apiAction = apiAction
        self._tId = tId
        self._timeStarted = time.time()
    def api(self):
        return self._apiAction
    def tId(self):
        return self._tId
    def howLong(self):
        duration = time.time() - self._timeStarted
        return duration
    def acquireNew(self, **kwargs):
        timeout = kwargs.pop("timeout", self.api().timeout)
        kw = {"timeout":timeout}
        if "purge" in kwargs:
            kw["purge"] = kwargs["purge"]
        tId = self.tId()
        result = self.api().ipc.getTransactionManager().acquireNew(tId, **kw)
        result = ApiTransportResponse.decode(result)
        #    Now either raise or return the result:
        if isinstance(result, Exception):
            raise result
        return result
    def __del__(self):
        api = self.api()
        if api:
            api.destroy()
