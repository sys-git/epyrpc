
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iStateControl(iApi):
    r"""
    @note: These 'EVENT_*' are api's that the caller can register
    it's own handler to receive.
    @attention: It is critically important that these strings are IDENTICAL
    to the method names in the relevant api: stateControl.py
    """
    EVENT__INSUFFICIENT_ENV = u"insufficientEnv"
    EVENT__DISTRIBUTION_COMPLETE = u"distributionComplete"
    """ CALLABLES-ACTIONS: """
    def init(self):
        r"""
        @summary: Initialise the ExecutionOrganiser.
        @attention: Time-intensive, best to make this call asynchronous!
        @return: eStateControlResult
        """
        raise NotImplementedException("iStateControl.init")
    def terminate(self):
        r"""
        @summary: Start the process of terminating the ExecutionOrganiser.
        @return: eStateControlResult
        """
        raise NotImplementedException("iStateControl.terminate")
    def run(self):
        r"""
        @summary: Start the ExecutionOrganiser's Engine.
        @return: eStateControlResult
        """
        raise NotImplementedException("iStateControl.run")
    def pause(self):
        r"""
        @summary: Pause the ExecutionOrganiser's Engine.
        @attention: This has the effect of Starting the ExecutionOrganiser's Engine if it's not already started.
        @return: eStateControlResult
        """
        raise NotImplementedException("iStateControl.pause")
    def pauseAtEnd(self):
        r"""
        @summary: Pause the ExecutionOrganiser's Engine once all tests which can be executed have been executed.
        @attention: This has the effect of Starting the ExecutionOrganiser's Engine if it's not already started.
        @return: eStateControlResult
        """
        raise NotImplementedException("iStateControl.pause")
    def stop(self, noFlush=False, noRecovery=False, allowReboots=True, noPackage=True, noUpload=True):
        r"""
        @summary: Stop the ExecutionOrganiser's Engine.
        @param noFlush: True - Do not flush results, False - otherwise.
        @param noRecovery: True - Do not allow recovery to continue, False - otherwise.
        @param allowReboots: True - Allow reboots to continue as part of the stop procedure, False - otherwise.
        @param noPackage: True - Do not package results, False - otherwise.
        @param noUpload: True - Do not upload results, False - otherwise.
        @raise iApiParamError: Error in parameters.
        @return: eStateControlResult
        """
        raise NotImplementedException("iStateControl.stop")
