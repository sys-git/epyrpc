
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterIdentifier import iFilterIdentifier

class iNamespace(iApiData, iFilterIdentifier):
    r"""
    @attention: IMPORTANT - The regx must be UNESCAPED - it will be escaped automatically.
    """
    def isRegx(self):
        r"""
        @summary: Determine if the namespace is a regx expression.
        @return: True - is regx, False - otherwise.
        """
        raise NotImplementedException("iNamespace.isRegx")
    def namespace(self):
        r"""
        @summary: Get the namespace such that it can be used by the SEH.
        @return: type=str - the namespace is allow through.
        """
        raise NotImplementedException("iNamespace.namespace")
    def compare(self, other, ignoreDirection=False):
        r"""
        @summary: Compare namespace with self.
        @param ignoreDirection: True = Ignore the direction component, False = otherwise.
        @return: True - namespace is the same and of same type, False - otherwise.
        """
        raise NotImplementedException("iNamespace.compare")
    def setDirection(self, e_filter_direction):
        r"""
        @set the filter direction (Filter-in, Filter-out).
        """
        raise NotImplementedException("iNamespace.setDirection")
    def direction(self):
        r"""
        @summary: Determine the filter direction.
        @return: eFilterDirection.
        """
        raise NotImplementedException("iNamespace.direction")

