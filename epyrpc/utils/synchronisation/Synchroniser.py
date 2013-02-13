

from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.synchronisation.StandardTransactionIdGenerator import \
    StandardTransactionGenerator
from epyrpc.utils.synchronisation.TransactionFailed import TransactionFailed
from epyrpc.utils.synchronisation.iSynchroniser import iSynchroniser
from epyrpc.utils.synchronisation.iSynchroniserItem import iSynchroniserItem
from multiprocessing.synchronize import Semaphore, RLock
# import pydevd

class Synchroniser(iSynchroniser):
    """ 
    @summary: Makes inter-thread comms synchronous.
    """
    class Item(iSynchroniserItem):
        def __init__(self, i):
            self._i = i
            self._sem = Semaphore(0)
            self._result = None
        def acquire(self, timeout=None):
            return self._sem.acquire(block=True, timeout=timeout)
        def result(self, result):
            iSynchroniserItem.result(self, result, lambda(x): self._sem.release())
        def getResult(self):
            return self._result
    def __init__(self, tIdGenerator=None):
        if tIdGenerator == None:
            tIdGenerator = StandardTransactionGenerator()
        self._i = tIdGenerator
        self._items = {}
        self.__lock = RLock()
        self._logger = LogManager().getLogger(self.__class__.__name__)
    def _lock(self):
        self.__lock.acquire()
    def _unlock(self):
        self.__lock.release()
    def isValidTransactionId(self, i):
        if (i is None):
            return False
        self._lock()
        try:
            if i in self._items.keys():
                return True
        finally:
            self._unlock()
        return False
    def create(self, enabler=True, callback=None):
        if not enabler: return
        self._lock()
        try:
            i = self._i.next()
            self._items[i] = self._getItem(i, callback)
            return i
        finally:
            self._unlock()
    def _getItem(self, i, callback=None):
        return Synchroniser.Item(i)
    def acquire(self, i, timeout=None, purgeOnFailure=False):
        """ 
        @summary: Wait for the result to the command.
        @param i: The unique synchronisationId as returned by create().
        @param timeout: Timeout in seconds to wait for the synchronisation to occur in.
        @param purge: True - Purge the synchronisationId before this method returns or raises an exception.
        Use this if the caller never needs to know when the transaction returns.
        @return: True - synchronised, False - otherwise.
        @see: getResult() - obtain the result of the synchronisation.
        """
        self._lock()
        try:
            item = self._items[i]
        except Exception, _e:
            self._logger.exception("Acquire on a non-existent synchroniser: %(I)s" % {"I":i})
            raise
        finally:
            self._unlock()
        #    Now wait on the semaphore:
        result = item.acquire(timeout=timeout)
        if not result and purgeOnFailure:
            self.purge(i)
        return result
    def acquireNew(self, i, timeout=None, purge=False):
        #    Check for transactionId validity:
        self._i.verify(i)
        self._lock()
        try:
            item = self._items[i]
        except KeyError, _e:
            self._logger.exception("Acquire on a non-existent synchroniser: %(I)s" % {"I":i})
            raise
        finally:
            self._unlock()
#        pydevd.settrace(stdoutToServer = True, stderrToServer = True)
        result = self._acquire(item, timeout)
#        pydevd.settrace(stdoutToServer = True, stderrToServer = True)
        if not result:
            purge and self.purge(i)
            raise TransactionFailed(i)
        result = item.getResult()
        if purge:
            self.purge(i)
        return result
    def _acquire(self, item, timeout):
        #    Now wait on the semaphore:
        result = item.acquire(timeout=timeout)
        return result
    def release(self, i, result=None):
        #    Check for transactionId validity:
        self._i.verify(i)
        self._lock()
        try:
            item = self._items[i]
            #    Store the result and release the resultant mechanism:
            item.result(result)
        except KeyError, _e:
            self._logger.exception("Release on a non-existent synchroniser: %(I)s" % {"I":i})
            raise
        finally:
            self._unlock()
    def getResult(self, i, purge=False):
        """ 
        @summary: Get the result of the synchroniser command:
        """
        self._lock()
        try:
            item = self._items[i]
        except KeyError, _e:
            self._logger.exception("Result called on a non-existent synchroniser: %(I)s" % {"I":i})
            raise
        else:
            result = item.getResult()
            if purge == True:
                self._items.pop(i)
            return result
        finally:
            self._unlock()
    def purge(self, i):
        self._lock()
        try:
            self._items.pop(i)
        except Exception, _e:
            #    Don't care!
            pass
        finally:
            self._unlock()
    def purgeAll(self):
        self._items = {}
    def releaseAll(self, result, purge=True):
        self._lock()
        try:
            for tId in self._items.keys():
                try:
                    self.release(tId, result)
                except Exception, _e:
                    #    Error triggering result in user handler.
                    pass
            if purge == True:
                self.purgeAll()
        finally:
            self._unlock()
    def __del__(self):
        self.purgeAll()
