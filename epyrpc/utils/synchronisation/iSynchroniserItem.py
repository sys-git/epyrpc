
from epyrpc.utils.Interfaces import Interface
from epyrpc.utils.synchronisation.IncompleteTransactionError import \
    IncompleteTransactionError
from epyrpc.utils.synchronisation.IpcTransportPartialResponse import \
    IpcTransportPartialResponse
from epyrpc.utils.synchronisation.PartialResponse import PartialResponse

class iSynchroniserItem(Interface):
    def result(self, result, releaseMethod):
        if isinstance(result, IpcTransportPartialResponse):
            if self._result == None:
                self._result = PartialResponse(result)
                try:
                    self._result.check()
                except IncompleteTransactionError, _e:
                    return
            else:
                try:
                    result = self._result.update(result)
                except IncompleteTransactionError, _e:
                    return
        else:
            self._result = result
        #    Now the result is complete, release it:
        releaseMethod(result)




