
from epyrpc.core.transaction.iTransactionManager import iTransactionManager
from epyrpc.synchronisation.CallbackSynchroniser import CallbackSynchroniser

class TransactionManager(CallbackSynchroniser, iTransactionManager):
    r"""
    @summary: A thin wrapper around the Synchroniser using a custom transactionId generator.
    """
    def __init__(self, tIdGenerator=None):
        super(TransactionManager, self).__init__(tIdGenerator)
