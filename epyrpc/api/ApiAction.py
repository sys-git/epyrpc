
from epyrpc.api.ApiCallbackWrapper import ApiCallbackWrapper
from epyrpc.api.ApiTransportItem import ApiTransportItem
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.api.AsyncResult import AsyncResult
from epyrpc.api.eSync import eSync
from epyrpc.api.iApiAction import iApiAction
from epyrpc.api.iApiParamError import iApiParamError
from epyrpc.core.IpcExceptions import IpcException
from epyrpc.utils.synchronisation.TransactionFailed import TransactionFailed
import itertools
import threading
import traceback

class ApiAction(iApiAction):
    r"""
    @summary: An object which describes the command to be actioned over IPC.
    """
    debugHandler = None
    _dId = itertools.count(0)
    @staticmethod
    def setDebugHandler(handler=None):
        ApiAction.debugHandler = handler
    def __call__(self, sync=None, timeout= -1, solicited=None, callback= -1, ignoreErrors=None):
        #    Check override params:
        if sync != None:
            self.sync = sync
        if timeout != -1:
            self.timeout = timeout
        if solicited != None:
            self.solicited = solicited
        if callback != -1:
            self.callback = callback
        try:
            return self._executeAction()
        except (IpcException, TransactionFailed, iApiParamError), e:
            if ignoreErrors != True:
                self._logger.warning(traceback.format_exc())
                raise e
    def _executeAction(self):
        ns = self.namespace
        args = self.args()
        kwargs = self.kwargs()
        ipc = self.ipc
        transactionManager = ipc.getTransactionManager()
        data = ApiTransportItem(ns, args, kwargs)
        #    Now decide how to handle the call - synchronous is different to asynchronous.
        data.async((self.sync == eSync.SYNCHRONOUS))
        callback = self.callback
        if self.sync == eSync.SYNCHRONOUS:
            #    Send the data:
            solicited = self.solicited
            wrapper = ApiCallbackWrapper.callback(callback)
            tId = ipc.sendData(data, solicited=solicited, callback=wrapper)
            dId = self._debugSync(tId=tId, timeout=self.timeout, data=data, solicited=solicited, callback=wrapper)
            #    For solicited calls, we must wait for the response - unless a callback is set.
            if solicited:
                if callback == None:
                    result = transactionManager.acquireNew(tId, timeout=self.timeout, purge=True)
                    result = ApiTransportResponse.decode(result)
                    self._debugResult(dId, result)
                    if isinstance(result, Exception):
                        raise result
                    else:
                        return result
                else:
                    self._startCallbackTimeoutTimer(dId, tId, transactionManager)
                return AsyncResult(self, tId)  #    WTF - this is synchronous ?!?!!
            #    By definition, unsolicited calls are fire-and-forget, so no return value necessary.
        else:
            #    Send the data:
            solicited = self.solicited
            wrapper = ApiCallbackWrapper.callback(callback)
            tId = ipc.sendData(data, solicited, callback=wrapper)
            dId = ApiAction._dId.next()
            self._startCallbackTimeoutTimer(dId, tId, transactionManager)
            #    Now return an object which we can use to later wait for the response.
            result = AsyncResult(self, tId)
            self._debugAsync(dId, result, timeout=self.timeout, data=data, solicited=solicited, callback=wrapper)
            return result
    def _timeoutViaCallback(self, dId, tId, transactionManager):
        if self:
            self._logger.warn("Callback transaction timed-out")
            self._callbackTimer = None
            self._debugTimeout(dId, tId)
            try:
                transactionManager.release(tId, TransactionFailed(tId))
            except:
                self._logger.warn("Callback transaction - failed to release!")
    def _startCallbackTimeoutTimer(self, dId, tId, transactionManager):
        timeout = self.timeout
        if timeout != None:
            #    Start a Timer to call the Synchroniser with the timeout result.
            r"""
            @summary: The timer will fire and trigger the synchroniser.release()
            @attention: It is up to the callback to purge the tId from the synchroniser,
            or ignore the result for a duplicate tId!
            """
            t = threading.Timer(timeout, self._timeoutViaCallback, args=[dId, tId, transactionManager])
            t.setName("ApiSynCbckTimer_%(C)s_%(T)s_seconds" % {"C":iApiAction.apiCall.next(), "T":timeout})
            t.setDaemon(True)
            self._callbackTimer = t
            t.start()
    def destroy(self):
        try:    self._callbackTimer.cancel()
        except: pass
    def __del__(self):
        self.destroy()
    def _debugAsync(self, dId, asyncResult=None, timeout=None, data=None, solicited=None, callback=None):
        handler = ApiAction.debugHandler
        if handler == None:
            return
        try:    handler.apiAsyncCall(dId, asyncResult, timeout, data, solicited, callback)
        except Exception, _e:
            self._logger.exception("d'oh!")
        return dId
    def _debugSync(self, tId=None, timeout=None, data=None, solicited=None, callback=None):
        handler = ApiAction.debugHandler
        if handler == None:
            return
        dId = ApiAction._dId.next()
        try:
            handler.apiSyncCall(dId, tId, timeout, data, solicited, callback)
        except Exception, _e:
            self._logger.exception("d'oh!")
        return dId
    def _debugResult(self, dId, result):
        handler = ApiAction.debugHandler
        if handler == None:
            return
        try:
            handler.apiResult(dId, result)
        except Exception, _e:
            self._logger.exception("d'oh!")
    def _debugTimeout(self, dId, tId):
        handler = ApiAction.debugHandler
        if handler == None:
            return
        try:
            handler.apiTimeout(dId, tId)
        except Exception, _e:
            self._logger.exception("d'oh!")
