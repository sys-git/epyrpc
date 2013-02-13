
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase
from epyrpc.api.eo_v1.impl.neck.peers.Peers import Peers
from epyrpc.api.eo_v1.impl.neck.tas.Tas import Tas
from epyrpc.api.eo_v1.impl.neck.testManagement.TestManagement import \
    TestManagement
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser

class api(ApiBase):
    r"""
    @summary: Used by the Neck to handle API requests.
    """
    def __init__(self, ns="", solicited=False, ipc=None, ignoreUnhandled=False, maxAsync=None):
        super(api, self).__init__("Body", ns=ns, solicited=solicited, ignoreUnhandled=ignoreUnhandled, maxAsync=maxAsync)
        if ipc != None:
            self.ipc = ipc
    def _setup(self, **kwargs):
        self.tas = Tas(**kwargs)
        self._apis.append(self.tas)
        self.testManagement = TestManagement(**kwargs)
        self._apis.append(self.testManagement)
        self.peers = Peers(**kwargs)
        self._apis.append(self.peers)
    r""" FYI-HANDLEABLE-EVENTS: """
    def getEventsToHandle(self):
        return []
    """ HANDLERS: """
    def _handler_status(self, tId, bSynchronous):
        def _status():
            return ExecutionOrganiser().getCache().snapshot()
        return self._handleStandardCall(tId, bSynchronous, _status)



