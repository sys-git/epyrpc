
import itertools

class iFilterIdentifier(Interface):
    nId = itertools.count(0)
    def id_(self):
        r"""
        @return: The unique id.
        """
        raise NotImplementedException("iFilterIdentifier.nId")
