
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApi import iApi

class iSignalFilter(iApi):
    def add(self, namespace):
        r"""
        @summary: Add namespaces to be filtered.
        @param namespace: a iNamespace of list of iNamespace to add.
        @raise iApiParamError: Error in parameters.
        @return: dict{ iNamespace : iFilterId }
        @attention: Filter's are added unmuted and enabled.
        """
        raise NotImplementedException("iSignalFilter.add")
    def remove(self, filters):
        r"""
        @summary: Remove namespaces that are filtered..
        @param filters: a iNamespace/iFilterId or list of iNamespace/iFilterId's to remove.
        @raise iApiParamError: Error in parameters.
        @return: dict{ iFilterId/iNamespace : iRemoved }
        """
        raise NotImplementedException("iSignalFilter.remove")
    def muteAll(self, enabler):
        r"""
        @summary: (un)Mute all filters (does not affect individual filters).
        @param enabler: eMute.ON - filters muted, eMute.OFF - otherwise.
        @raise iApiParamError: Error in parameters.
        @return: eMute - The new state of the global filter mute.
        """
        raise NotImplementedException("iSignalFilter.mute")
    def mute(self, filters):
        r"""
        @summary: Set the mute state for the filters.
        @param filters: A list of tuple(iNamespace/iFilterId, eMute) to mute.
        @raise iApiParamError: Error in parameters.
        @return: iFilter: iSignalFilterStatus and the mute state of filters implicitly affected.
        """
        raise NotImplementedException("iSignalFilter.mute")
    def query(self, filters):
        r"""
        @summary: Query some or all of the given signal filters.
        @param filters: a iNamespace/iFilterId or list of iNamespace/iFilterId's to query.
        @raise iApiParamError: Error in parameters.
        @return: {iNamespace/iFilterId:iASignalFilter/Exception}
        """
        raise NotImplementedException("iSignalFilter.query")
    def globalEnable(self, enabler):
        r"""
        @summary: Enable/Disable all filters (does not affect individual filters).
        @param enabler: eGlobalEnable.ON - filters muted, eGlobalEnable.OFF - otherwise.
        @raise iApiParamError: Error in parameters.
        @return: iSignalFilterStatus: The new state of the GlobalMute and GlobalEnable.
        """
        raise NotImplementedException("iSignalFilter.globalEnable")
    def status(self):
        r"""
        @summary: Query the current global eMute and eGlobalEnable status.
        @return: iSignalFilterStatus: The new state of the GlobalMute and GlobalEnable.
        """
        raise NotImplementedException("iSignalFilter.status")
    def archive(self, i_location=None):
        r"""
        @summary: Archive the signals to the given location for later retrieval.
        @return: iSignalFilterStatus: The new state of the GlobalMute and GlobalEnable.
        """
        raise NotImplementedException("iSignalFilter.archive")
    def retrieve(self, theRange=None):
        r"""
        @summary: Retrieve the signals in the given range.
        """
        raise NotImplementedException("iSignalFilter.retrieve")



