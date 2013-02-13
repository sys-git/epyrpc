
import itertools
from epyrpc.utils.synchronisation.iTransactionIdGenerator import iTransactionIdGenerator
from epyrpc.utils.synchronisation.TransactionIdError import TransactionIdError

class TransactionIdGeneratorBase(iTransactionIdGenerator):
    UNKNOWN = 0
    HEAD = 1
    NECK = 2
    def __init__(self, t=0):
        self.eType = t
        self._id = itertools.count(1)
    def getType(self):
        return self._type
    def setType(self, t):
        self._type = t
    eType = property(getType, setType)
    def next(self):
        return (self.eType, self._id.next())
    def verify(self, tId):
        if tId:
            (_eType, _id) = tId
            if _eType != self.eType:
                raise TransactionIdError("Expecting type: %(E)s but got: %(G)s" % {"E":self.eType, "G":_eType})
