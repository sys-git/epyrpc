
import itertools
from epyrpc.utils.Interfaces import Interface
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iFilterIdentifier(Interface):
    nId = itertools.count(0)
    def id_(self):
        r"""
        @return: The unique id.
        """
        raise NotImplementedException("iFilterIdentifier.nId")
