
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.api.eo_v1.enums.eStateControlResult import eStateControlResult
from epyrpc.api.eo_v1.impl.checkers.tas.StateControlChecker import \
    StateControlChecker
from epyrpc.api.eo_v1.interfaces.neck.tas.stateControl.iStateControl import \
    iStateControl
from multiprocessing.synchronize import Semaphore
import threading

class StateControl(iStateControl):
    r"""
    Handlers are preceded with '_handler_'.
    In theory, you could have a symmetrical API all in the same iApi file as the Head (if we
    wanted the head to be able to talk to it's ExecutionOrganiser (if it had one that we wanted
    to export to the Neck!)
    Handlers MUST obey the IPC iIpcTransportDataReceiveListener.transportDataReceive contract.
    @attention: All return objects are either native types, Exceptions or iApiData.
    @attention: The return type must be PICKLABLE!
    """
    def __init__(self, ns="", solicited=False):
        super(StateControl, self).__init__(ns=ns, solicited=solicited)
    """ HANDLERS: """
    def _handler_init(self, tId, bSynchronous):
        def _init():
            #    We need to listen for the SystemReady signal.
            class Result(object):
                def __init__(self, result=eStateControlResult.FAILURE):
                    self._result = result
                    self._completed = Semaphore(0)
                def wait(self, timeout=None):
                    self._completed.acquire(timeout=timeout)
                def getResult(self):
                    return self._result
                def setResult(self, result):
                    self._result = result
                    self._completed.release()
            result = Result()
            systemReadyListener = None
            errorListener = None
            seh = SignalExchangeHub()
            def removeListeners():
                #    Potential race-condition with finally block below but we must remove the listener immediately and in the finally block.
                try:    seh.removeListener(systemReadyListener)
                except: pass
                try:    seh.removeListener(errorListener)
                except: pass
            def initComplete(signal):
                result.setResult(eStateControlResult.SUCCESS)
                removeListeners()
                #    FIXME: Hack until the ExecutionOrganiser startup stages are counted properly.
                ExecutionOrganiser().signalFilters().startArchiver()
            def errorDuringInit(signal):
                self._logger.debug("ERROR DURING INIT!!!")
                result.setResult(eStateControlResult.FAILURE)
                removeListeners()
            try:
                systemReadyListener = SystemReady.createListener(initComplete)
                seh.addListener(systemReadyListener)
                errorListener = Error.createListener(errorDuringInit)
                seh.addListener(errorListener)
                eo = ExecutionOrganiser()
                eo.createProcess()
                eo.initProcess()
                self._logger.debug("INIT WAITING!!!")
                result.wait()
                self._logger.debug("INIT COMPLETE!!!")
            finally:
                try:
                    removeListeners()
                except Exception, _e:
                    #    Don't care.
                    pass
            rtn = result.getResult()
            return rtn
        return self._handleStandardCall(tId, bSynchronous, lambda: _init())
    def _handler_terminate(self, tId, bSynchronous):
        r"""
        @summary: Special-case: We need to return the result (terminate started)
        immediately, then wait for it to be sent, then start the teardown.
        """
        def _terminate():
            ExecutionOrganiser.destroySingleton()
        threading.Timer(2, _terminate).start()
        return ApiTransportResponse(eStateControlResult.SUCCESS)
    def _handler_run(self, tId, bSynchronous):
        def _run():
            #    Kick off the ExecutionOrganiser.
            eo = ExecutionOrganiser()
            eo.start()
            return eStateControlResult.SUCCESS
        return self._handleStandardCall(tId, bSynchronous, lambda: _run())
    def _handler_pause(self, tId, bSynchronous):
        def _pause():
            eo = ExecutionOrganiser()
            eo.pause()
            return eStateControlResult.SUCCESS
        return self._handleStandardCall(tId, bSynchronous, lambda: _pause())
    def _handler_pauseAtEnd(self, tId, bSynchronous):
        def _pauseAtEnd():
            eo = ExecutionOrganiser()
            eo.pauseAtEnd()
            return eStateControlResult.SUCCESS
        return self._handleStandardCall(tId, bSynchronous, lambda: _pauseAtEnd())
    def _handler_stop(self, tId, bSynchronous, **kwargs):
        kwargs = self._handleStandardCheck(tId, bSynchronous, StateControlChecker.checkStop, **kwargs)
        def _stop():
            eo = ExecutionOrganiser()
            eo.stop()
            return eStateControlResult.SUCCESS
        return self._handleStandardCall(tId, bSynchronous, lambda: _stop(), **kwargs)
    """ CALLABLES-EVENTS: """
    def insufficientEnv(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    def distributionComplete(self):
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)

