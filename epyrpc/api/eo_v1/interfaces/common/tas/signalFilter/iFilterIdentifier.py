
import itertools
from YouView.TAS.Master.MasterBusinessLogic.Utils.Interfaces import Interface
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iFilterIdentifier(Interface):
    nId = itertools.count(0)
    def id_(self):
        r"""
        @return: The unique id.
        """
        raise NotImplementedException("iFilterIdentifier.nId")
