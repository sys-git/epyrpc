
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iSynchroniser(Interface):
    def isValidTransactionId(self, i):
        r"""
        @summary: Determine if the given tId is a tId which we've created.
        @return: True - Is valid, False - otherwise.
        """
        raise NotImplementedException("iSynchroniser.isValidTransactionId")
    def create(self, enabler=True, callback=None):
        r"""
        @summary: Create a new transaction
        @param enabler: True - create a new tId, False - otherwise.
        @param callback: The callback to be called when the transaction completes RATHER THAN
        calling acquireNew().
        @return: tId - A new unique transactionId.
        """
        raise NotImplementedException("iSynchroniser.create")
    def acquireNew(self, i, timeout=None, purge=False):
        """ 
        @summary: Wait for the result to the command.
        @param i: The unique synchronisationId as returned by create().
        @param timeout: Timeout in seconds to wait for the synchronisation to occur in.
        @param purge: True - Purge the synchronisationId before this method returns or raises an exception.
        Use this if the caller never needs to know when the transaction returns.
        @return: The result of the synchronisation.
        @raise: TransactionFailed - synchronisation failed in the given timeout!
        @raise: KeyError - Attempt to acquire non-existent synchronisationId
        @attention: Deprecates method: acquire().
        """
        raise NotImplementedException("iSynchroniser.acquireNew")
    def release(self, i, result=None):
        """ 
        @summary: Store the result for the command.
        @param i: The unique synchronisationId as returned by create().
        @param result: The raw result.
        """
        raise NotImplementedException("iSynchroniser.release")
    def getResult(self, i, purge=False):
        """ 
        @summary: Get the result of the synchroniser command:
        @param i: The unique synchronisationId as returned by create().
        @param purge: Purge the synchronisationId before this call returns.
        @raise: KeyError - Attempt to aquire non-existent synchronisationId
        @return: The result.
        """
        raise NotImplementedException("iSynchroniser.getResult")
    def purge(self, i):
        """ 
        @summary: Purge the given value from our items.
        @param i: The unique synchronisationId as returned by create().
        """
        raise NotImplementedException("iSynchroniser.purge")
    def purgeAll(self):
        """ 
        @summary: Purge all items from the Synchroniser.
        """
        raise NotImplementedException("iSynchroniser.purgeAll")
    def releaseAll(self, result, purge=True):
        r"""
        @summary: Release all waiting clients.
        @result: The result to release the clients with.
        @param purge: Purge ALL the synchronisationIds before this call returns.
        """
        raise NotImplementedException("iSynchroniser.releaseAll")


