
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData

class iGlobalEnable(iApiData):
    def isEnabled(self):
        r"""
        @requires: True - Global filter enabler is ON, False - otherwise.
        """
        raise NotImplementedException("iGlobalEnable.isEnabled")
