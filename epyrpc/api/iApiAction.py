
import itertools
from epyrpc.utils.Interfaces import Interface
from epyrpc.utils.LogManager import LogManager
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eSync import eSync
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iApiAction(Interface):
    r"""
    @summary: The interface that the ApiAction must implement.
    """
    DEFAULT_SYNC = eSync.SYNCHRONOUS
    DEFAULT_TIMEOUT = None
    DEFAULT_SOLICITED = True
    apiCall = itertools.count(0)
    def __init__(self, __ipc__, __namespace__, __solicited__, *args, **kwargs):
        self._logger = LogManager().getLogger("api:%(NS)s" % {"NS":__namespace__})
        self._ipc = __ipc__
        self.namespace = __namespace__
        self._args = args
        self._kwargs = kwargs
        self._cb = None
        self.sync = iApiAction.DEFAULT_SYNC
        self.timeout = iApiAction.DEFAULT_TIMEOUT
        self.solicited = __solicited__
        self.callback = None
        self._callbackTimer = None
    def __del__(self):
        try:    self._callbackTimer.cancel()
        except: pass
    def setNamespace(self, namespace):
        if not isinstance(namespace, basestring):
            raise ApiParamError(namespace, basestring)
        self._namespace = namespace
    def getNamespace(self):
        return self._namespace
    def args(self):
        return self._args
    def kwargs(self):
        return self._kwargs
    def getSolicited(self):
        return self._solicited
    def setSolicited(self, solicited=True):
        self._solicited = solicited
    def getSync(self):
        return self._sync
    def setSync(self, sync=eSync.SYNCHRONOUS):
        if not eSync.isValid(sync):
            raise ApiParamError(sync, eSync)
        self._sync = sync
    def getTimeout(self):
        return self._timeout
    def setTimeout(self, timeout=None):
        if timeout == 0:
            timeout = None
        if timeout != None:
            if not (isinstance(timeout, int) or isinstance(timeout, float)):
                raise ApiParamError(timeout, [int, float])
            if timeout < 0:
                raise ApiParamError(timeout, [int, float])
        self._timeout = timeout
    def setIpc(self, ipc):
        if ipc == None:
            return
        if not isinstance(ipc, iIpcTransport):
            raise ApiParamError(ipc, iIpcTransport)
        self._ipc = ipc
    def getIpc(self):
        return self._ipc
    def setCallback(self, cb):
        self._cb = cb
    def getCallback(self):
        return self._cb
    def destroy(self):
        raise NotImplementedException("iApiAction.destroy")

    namespace = property(getNamespace, setNamespace)
    sync = property(getSync, setSync)
    timeout = property(getTimeout, setTimeout)
    ipc = property(getIpc, setIpc)
    solicited = property(getSolicited, setSolicited)
    callback = property(getCallback, setCallback)
