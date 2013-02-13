
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApiData import iApiData

class iFilters(iApiData):
    def status(self):
        r"""
        @return: iSignalFilterStatus.
        """
        raise NotImplementedException("iFilters.status")
    def filters(self):
        r"""
        @return: The list of filters.
        """
        raise NotImplementedException("iFilters.status")
