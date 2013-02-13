
from epyrpc.utils.synchronisation.StandardTransactionIdGenerator import \
    StandardTransactionGenerator
from epyrpc.utils.synchronisation.Synchroniser import Synchroniser
from epyrpc.utils.synchronisation.iSynchroniserItem import iSynchroniserItem

class CallbackSynchroniser(Synchroniser):
    r"""
    @summary: Used for Head-2-Neck API transaction processing.
    """
    class CallbackItem(iSynchroniserItem):
        r"""
        @summary: Used for handling callback rather than async events.
        The caller can call acquire even when a callback listener is specified but a TypeError will be raised!
        """
        def __init__(self, i, callback):
            self._i = i
            self._callback = callback
            self._result = None
        def result(self, result):
            iSynchroniserItem.result(self, result, lambda(x): self._callback(self._i, x))
        def getResult(self):
            return self._result
    def __init__(self, tIdGenerator=StandardTransactionGenerator()):
        super(CallbackSynchroniser, self).__init__(tIdGenerator=tIdGenerator)
    def _getItem(self, i, callback=None):
        if callback == None:
            return super(CallbackSynchroniser, self)._getItem(i, callback=callback)
        return CallbackSynchroniser.CallbackItem(i, callback)
    def _acquire(self, item, timeout):
        if isinstance(item, Synchroniser.Item):
            return super(CallbackSynchroniser, self)._acquire(item, timeout)
        raise TypeError("Cannot acquire on a CallbackItem !")

