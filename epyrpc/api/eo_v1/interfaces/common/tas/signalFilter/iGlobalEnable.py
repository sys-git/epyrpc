
from epyrpc.api.iApiData import iApiData
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iGlobalEnable(iApiData):
    def isEnabled(self):
        r"""
        @requires: True - Global filter enabler is ON, False - otherwise.
        """
        raise NotImplementedException("iGlobalEnable.isEnabled")
