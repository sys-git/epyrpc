
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase
from epyrpc.api.eo_v1.interfaces.head.iAPI import iAPI

class api(ApiBase, iAPI):
    r"""
    @summary: Holds all the top-level API objects for use by the Head/Neck.
    """
    def __init__(self, ns="", solicited=True, ipc=None, ignoreUnhandled=True, maxAsync=1):
        super(api, self).__init__("Head", ns=ns, solicited=solicited, ignoreUnhandled=ignoreUnhandled, maxAsync=maxAsync)
        if ipc != None:
            self.ipc = ipc
    """ CALLABLES-ACTIONS: """
    def status(self):
        r"""
        @attention: Triggers events basically a cache-dump in event form: (metadata, tests, peers, stats)
        """
        return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
    r""" FYI-HANDLEABLE-EVENTS: """
    def getEventsToHandle(self):
        return []



