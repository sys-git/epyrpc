
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iStateControl(iApi):
    r"""
    @summary: This mirrors the iStateControl class to provide handlers
    for the corresponding methods in iStateControl.
    @param tId: TransactionId.
    @param bSynchronous: True - method is being run synchronously and should
    return synchronously, False - otherwise.
    """
    """ CALLABLES-EVENTS: """
    def insufficientEnv(self):
        r"""
        @summary: Distribution is finished but incomplete due to unsatisfied
        environmental considerations.
        @attention: The ExecutionOrganiser is idling.
        """
        raise NotImplementedException("iSignalFilter.insufficientEnv")
    def distributionComplete(self):
        r"""
        @summary: Distribution is finished and complete.
        @attention: The ExecutionOrganiser is idling.
        """
        raise NotImplementedException("iSignalFilter.distributionComplete")
    """ HADNLERS: """
    def _handler_init(self, tId, bSynchronous):
        r"""
        @summary: Initialise the ExecutionOrganiser.
        @attention: Time-intensive, best to make this call asynchronous!
        @return: eStateControlResult
        """
        raise NotImplementedException("iSignalFilter._handler_init")
    def _handler_terminate(self, tId, bSynchronous):
        r"""
        @summary: Start the process of Terminating the ExecutionOrganiser.
        @return: eStateControlResult
        """
        raise NotImplementedException("iSignalFilter._handler_terminate")
    def _handler_run(self, tId, bSynchronous):
        r"""
        @summary: Start the process of Start the ExecutionOrganiser's Engine.
        @return: eStateControlResult
        """
        raise NotImplementedException("iSignalFilter._handler_run")
    def _handler_pause(self, tId, bSynchronous):
        r"""
        @summary: Start the process of Pausing the ExecutionOrganiser's Engine.
        @attention: This has the effect of Starting the ExecutionOrganiser's Engine if it's not already started.
        @return: eStateControlResult
        """
        raise NotImplementedException("iSignalFilter._handler_pause")
    def _handler_pauseAtEnd(self, tId, bSynchronous):
        r"""
        @summary: Tell the ExecutionOrganiser's Engine to pause execution at the end of test distribution.
        @attention: This has the effect of Starting the ExecutionOrganiser's Engine if it's not already started.
        @return: eStateControlResult
        """
        raise NotImplementedException("iSignalFilter._handler_pause")
    def _handler_stop(self, tId, bSynchronous, noFlush=False, noRecovery=False, allowReboots=True, noPackage=True, noUpload=True):
        r"""
        @summary: Start the process of Stopping the ExecutionOrganiser's Engine.
        @param noFlush: True - Do not flush results, False - otherwise.
        @param noRecovery: True - Do not allow recovery to continue, False - otherwise.
        @param allowReboots: True - Allow reboots to continue as part of the stop procedure, False - otherwise.
        @param noPackage: True - Do not package results, False - otherwise.
        @param noUpload: True - Do not upload results, False - otherwise.
        @raise iApiParamError: Error in parameters.
        @return: eStateControlResult
        """
        raise NotImplementedException("iSignalFilter._handler_stop")
