from epyrpc.utils.synchronisation.TransactionIdGeneratorBase import \
    TransactionIdGeneratorBase

class HeadTransactionIdGenerator(TransactionIdGeneratorBase):
    def __init__(self):
        super(HeadTransactionIdGenerator, self).__init__(self.HEAD)

