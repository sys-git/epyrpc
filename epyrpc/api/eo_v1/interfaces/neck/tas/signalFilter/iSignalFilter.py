
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApi import iApi

class iSignalFilter(iApi):
    r"""
    @summary: This mirrors the iSignalFilter class to provide handlers
    for the corresponding methods in iSignalFilter.
    @param tId: TransactionId.
    @param bSynchronous: True - method is being run synchronously and should
    return synchronously, False - otherwise.
    """
    def _handler_add(self, tId, bSynchronous, i_namespaces):
        r"""
        @summary: Add namespaces to be filtered.
        @param i_namespaces: a namespace of list of namespaces to add.
        @raise iApiParamError: Error in parameters.
        @return: dict{ iNamespace : iFilterId }
        """
        raise NotImplementedException("iSignalFilter._handler_add")
    def _handler_remove(self, tId, bSynchronous, filters):
        r"""
        @summary: remove namespaces that are filtered.
        @param filters: a iNamespace/iFilterId or list of iNamespace/iFilterId's to remove.
        @raise iApiParamError: Error in parameters.
        @return: dict{ iFilterId/iNamespace : iRemoved }
        """
        raise NotImplementedException("iSignalFilter._handler_remove")
    def _handler_muteAll(self, tId, bSynchronous, e_global_mute):
        r"""
        @summary: (un)Mute all filters (does not affect individual filters).
        @param e_global_mute: eMute.ON - filters muted, eMute.OFF - otherwise.
        @raise iApiParamError: Error in parameters.
        @return: eMute - The new state of the global filter mute.
        """
        raise NotImplementedException("iSignalFilter._handler_muteAll")
    def _handler_mute(self, tId, bSynchronous, filters):
        r"""
        @summary: (un)Mute all filters (does not affect individual filters).
        @param filters: A list of iNamespace/iFilterId's to mute.
        @raise iApiParamError: Error in parameters.
        @return: iFilter: iSignalFilterStatus and the mute state of filters implicitaly affected.
        """
        raise NotImplementedException("iSignalFilter._handler_mute")
    def _handler_query(self, tId, bSynchronous, filters):
        r"""
        @summary: Query some or all of the given signal filters.
        @param filters: a iNamespace/iFilterId or list of iNamespace/iFilterId's to query.
        @raise iApiParamError: Error in parameters.
        @return: iFilter: iSignalFilterStatus and the mute state of filters implicitaly affected.
        """
        raise NotImplementedException("iSignalFilter._handler_query")
    def _handler_globalEnable(self, tId, bSynchronous, e_global_enable):
        r"""
        @summary: Enable/Disable all filters (does not affect individual filters).
        @param e_global_enable: eGlobalEnable.ON - filters muted, eGlobalEnable.OFF - otherwise.
        @raise iApiParamError: Error in parameters.
        @return: iSignalFilterStatus: The new state of the GlobalMute and GlobalEnable.
        """
        raise NotImplementedException("iSignalFilter._handler_globalEnable")
    def _handler_status(self, tId, bSynchronous):
        r"""
        @summary: Query the current global eMute and eGlobalEnable status.
        @return: iSignalFilterStatus: The new state of the GlobalMute and GlobalEnable.
        """
        raise NotImplementedException("iSignalFilter._handler_status")



