
from epyrpc.utils.synchronisation.TransactionIdGeneratorBase import \
    TransactionIdGeneratorBase

class NeckTransactionIdGenerator(TransactionIdGeneratorBase):
    def __init__(self):
        super(NeckTransactionIdGenerator, self).__init__(self.NECK)

