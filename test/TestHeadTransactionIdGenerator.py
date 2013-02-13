
from epyrpc.synchronisation.generators.HeadTransactionIdGenerator import \
    HeadTransactionIdGenerator
from epyrpc.utils.synchronisation.TransactionIdGeneratorBase import \
    TransactionIdGeneratorBase
import unittest

class TestHeadTrasactionGenerator(unittest.TestCase):
    def testType(self):
        h = HeadTransactionIdGenerator()
        t = h.eType
        assert t == TransactionIdGeneratorBase.HEAD, "Expecting: %(E)s but got %(G)s" % {""}

if __name__ == '__main__':
    unittest.main()
