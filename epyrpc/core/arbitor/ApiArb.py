
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.api.iApiTransportItem import iApiTransportItem
from epyrpc.core.IpcExceptions import NoResponseRequired
from epyrpc.core.arbitor.MultipleApiResponseError import MultipleApiResponseError
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener
from epyrpc.utils.LogManager import LogManager
from multiprocessing.synchronize import RLock
import os

class ApiArb(iIpcTransport, iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    r"""
    @summary: This class arbitrates between many IPC listeners.
    This will allow multiple APIs to hook into this IPC wrapper (via
    setTransportStateChangeListener and setTransportDataReceiveListener,
    each having different namespaces - it is up to the api writer to make sure
    that there is no conflicting namespace hit in their api with any existing
    apis attached to this IPC. If a conflict arises, MultipleApiResponseError
    will be raised.
    Each api is a conceptual 'channel' over which predefined api calls are made.
    There is nothing to stop the apis being dynamic wrt their handled namespaces.
    
    Typical example usage:
    ( HEAD                     ) -------------------------( BODY                     )
    ['1' handler workers]-api1-\                          /-api1-['x' handler workers]
    ['1' handler workers]-api2-ApiArb--IPC-wire-IPC--ApiArb-api2-['y' handler workers]
    ['1' handler workers]-api3-/                          \-api3-['z' handler workers]
    """
    _cache = {}
    _wrappedNames = []
    _nonWrappedNames = ["setTransportStateChangeListener", "setTransportDataReceiveListener"]
    @classmethod
    def __new__(cls, ipc, *args, **kwargs):
        for i in dir(iIpcTransport):
            if not i.startswith("_"):
                cls._wrappedNames.append(i)
        for name in cls._nonWrappedNames:
            cls._wrappedNames.remove(name)
        return super(ApiArb, cls).__new__(cls, ipc, *args, **kwargs)
    def __init__(self, ipc, *args, **kwargs):
        self._logger = LogManager().getLogger("ApiArb")
        self._listeners = {"dataReceive":[], "stateChange":[]}
        self._lock = RLock()
        #    Hook the IPC into us.
        self._ipc = ipc
        self._ipc.setTransportStateChangeListener(self)
        self._ipc.setTransportDataReceiveListener(self)
    def setTransportStateChangeListener(self, listener):
        if listener != None:
            if not isinstance(listener, iIpcTransportStateChangeListener):
                raise ValueError(listener)
        self._updateListener(listener, self._listeners["stateChange"])
    def setTransportDataReceiveListener(self, listener):
        if listener != None:
            if not isinstance(listener, iIpcTransportDataReceiveListener):
                raise ValueError(listener)
        self._updateListener(listener, self._listeners["dataReceive"])
    def _updateListener(self, listener, what):
        with self._lock:
            if listener in what:
                #    Remove the existing listener:
                what.remove(listener)
            else:
                #    Add the new listener:
                what.append(listener)
    @classmethod
    def create(cls, ipc, *args, **kwargs):
        pid = os.getpid()
        id_ = "%s.%s" % (pid, id(ipc))
        if id_ in cls._cache.keys():
            return cls._cache[id_]  #    One arbitor per ipc per process.
        ipcArb = ApiArb(ipc, *args, **kwargs)
        cls._cache[id_] = ipcArb
        return ipcArb
    def transportDataReceive(self, tId, data):
        #    Data is received!
        #    Propagate to the api's to see which one will handle it:
        results = []
        with self._lock:
            listeners = self._listeners["dataReceive"][:]
        numListeners = len(listeners)
        try:
            namespace = data.ns()
        except Exception, _e:
            namespace = ""
        if len(listeners) == 0:
            #    Do nothing!
            raise UnsupportedApiError("various:%(C)s" % {"C":numListeners}, namespace)
        #    Check for multiple potential handlers (asynchronous handler check done below also):
        if isinstance(data, iApiTransportItem):
            hCount = 0
            for listener in listeners:
                ns = data.ns()
                hCount += (listener.isInMyNamespace(ns) and listener.handlerExists(ns))  #    Got to love int+boolean
            if hCount > 1:
                raise MultipleApiResponseError(ns=ns, count=hCount)
        for listener in listeners:
            r"""
            All listeners are asynchronous anyway except the ns matching and handler finding
            which is all we care about here!
            """
            try:
                result = listener.transportDataReceive(tId, data)
            except UnsupportedApiError, result:
                pass
            except NoResponseRequired, result:
                pass
            results.append(result)
        #    Now check the results to see if we've not handled it:
        # #    If result==UnsupportedApiError, this means that the ns is not for this api, so if all are
        # #    ==UnsupportedApiError then the api wasn't handled at all!
        #
        #    If all are NoResponseRequired, then do nothing.
        #    If all are UnsupportedApiError, then raise UnsupportedApiError.
        allUnsupportedApiError = True
        for result in results:
            if not isinstance(result, UnsupportedApiError):
                allUnsupportedApiError = False
                break
        if allUnsupportedApiError:
            #    By definition, data is of type: iApiTransportItem.
            raise UnsupportedApiError("various:%(C)s" % {"C":numListeners}, namespace)
        allNoResponseRequired = True
        for result in results:
            if not isinstance(result, NoResponseRequired):
                allNoResponseRequired = False
                break
        if allNoResponseRequired:
            raise NoResponseRequired(tId)
        #    Return the actual result:
        uId = "0"
        oneTrueResult = {}
        for result in results:
            if not isinstance(result, UnsupportedApiError) and not isinstance(result, NoResponseRequired):
                #    Found the one true response - now check that it is the 'one':
                if len(oneTrueResult.keys()) == 0:
                    oneTrueResult[uId] = [result]
                else:
                    #    Oh dear - it is not unique!
                    self._logger.error("Multiple APIs handled this transaction: %(T)s" % {"T":tId})
                    oneTrueResult[uId].append(result)
        if len(oneTrueResult.keys()) > 0:
            if len(oneTrueResult[uId]) == 0:
                result = oneTrueResult[uId][0]
                return result
            else:
                raise MultipleApiResponseError(results=oneTrueResult[uId])
        #    No result, then we need to raise the fact:
        raise NoResponseRequired(tId)
    def transportStateChange(self, state):
        #    State has changed!
        #    Propagate to all apis - synchronously for now:
        with self._lock:
            listeners = self._listeners["stateChange"][:]
        for listener in listeners:
            listener.transportStateChange(state)
    def __getattribute__(self, name):
        #    Make some api methods pass-through to the raw IPC:
        if (name in ApiArb._wrappedNames) and (name not in ApiArb._nonWrappedNames):
            return getattr(self._ipc, name)
        else:
            return object.__getattribute__(self, name)

