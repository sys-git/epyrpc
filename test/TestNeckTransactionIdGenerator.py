
from epyrpc.synchronisation.generators.NeckTransactionIdGenerator import \
    NeckTransactionIdGenerator
from epyrpc.utils.synchronisation.TransactionIdGeneratorBase import \
    TransactionIdGeneratorBase
import unittest

class TestNeckTrasactionGenerator(unittest.TestCase):
    def testType(self):
        h = NeckTransactionIdGenerator()
        t = h.eType
        assert t == TransactionIdGeneratorBase.NECK, "Expecting: %(E)s but got %(G)s" % {""}

if __name__ == '__main__':
    unittest.main()
