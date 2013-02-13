
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iAsyncResult(Interface):
    def api(self):
        r"""
        @return: The iApiAction object associated with this api call.
        """
        raise NotImplementedException("iAsyncResult.api")
    def tId(self):
        r"""
        @return: The unique transactionId associated with this api call.
        """
        raise NotImplementedException("iAsyncResult.tId")
    def howLong(self):
        r"""
        @return: The current duration of the api call.
        """
        raise NotImplementedException("iAsyncResult.howLong")
    def acquireNew(self, **kwargs):
        r"""
        @summary: Wait on the asynchronous result.
        @param kwargs["timeout"]: See: iSynchroniser.acquireNew(timeout)
        @param kwargs["purge"]: See: iSynchroniser.acquireNew(purge)
        @see: Same behaviour as 'iSynchroniser.acquireNew()'.
        """
        raise NotImplementedException("iAsyncResult.howLong")
