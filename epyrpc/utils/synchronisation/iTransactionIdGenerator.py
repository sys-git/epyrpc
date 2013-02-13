
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iTransactionIdGenerator(Interface):
    def next(self):
        r"""
        @summary: Get the next unique transaction identifier.
        @attention: The return value MUST be hashable.
        """
        raise NotImplementedException("iTransactionIdGenerator.next")
    def verify(self):
        r"""
        @summary: Verify the identifier is of the correct signature.
        @return: None - no error.
        @raise TransactionIdError - transactionId is NOT from 'this' side.
        """
        raise NotImplementedException("iTransactionIdGenerator.verify")

