
from epyrpc.utils.synchronisation.TransactionIdGeneratorBase import TransactionIdGeneratorBase

class StandardTransactionGenerator(TransactionIdGeneratorBase):
    def __init__(self):
        super(StandardTransactionGenerator, self).__init__()
