
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase

class api(ApiBase):
    r"""
    @summary: Used by the Neck to handle API requests.
    """
    def __init__(self, ns="", solicited=False, ipc=None, ignoreUnhandled=False, maxAsync=None):
        super(api, self).__init__("Body", ns=ns, solicited=solicited, ignoreUnhandled=ignoreUnhandled, maxAsync=maxAsync)
        if ipc != None:
            self.ipc = ipc
    r""" FYI-HANDLEABLE-EVENTS: """
    def getEventsToHandle(self):
        return []
    """ HANDLERS: """
    def _handler_status(self, tId, bSynchronous):
        def _status():
            return
        return self._handleStandardCall(tId, bSynchronous, _status)



