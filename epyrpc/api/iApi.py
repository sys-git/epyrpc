
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.core.IpcExceptions import NoResponseRequired
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener
from epyrpc.utils.Interfaces import Interface
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.synchronisation.IpcTransportPartialResponse import \
    IpcTransportPartialResponse
import inspect

class iApi(Interface):
    """ The super-class for all APIs """
    CATCHALL = u"*"
    HANDLER_PREFIX = u"_handler_"
    EVENT_PREFIX = u"EVENT__"
    def __init__(self, ns="", solicited=True, ipc=None, name=None):
        clazzName = self.__class__.__name__
        self.__setNamespace(self._createNamespace([ns, clazzName]))
        loggerName = self._getNamespace()
        if name != None:
            loggerName = name + "." + loggerName
        self._logger = LogManager().getLogger(loggerName)
        self._ipc = ipc
        self.solicited = solicited
        self._transportDataReceiveListener = None
        self._transportStateChangeListener = None
        self._apis = []
        self._apiHandlers = {}

        self.__actions = []
        self.__actionNamespaces = {}

        # Find all callable methods
        for attr in dir(self):
            method = getattr(self, attr)
            if attr[0] < 'a' or not callable(method): continue
            self.__actions.append(method)

        # Collect all method namespaces
        globalNamespace = self._getNamespace()
        for action in self.__actions:
            namespace = "%s.%s" % (globalNamespace, action.im_func.func_name)
            self.__actionNamespaces[namespace] = action

    def getSolicited(self):
        return self._solicited

    def setSolicited(self, solicited=True):
        if not type(solicited) == bool:
            raise ApiParamError(solicited, bool)
        self._solicited = solicited

    def __setNamespace(self, namespace):
        if not isinstance(namespace, basestring):
            raise ApiParamError(namespace, basestring)
        self._namespace = namespace.lower()

    def _getNamespace(self):
        return self._namespace.lower()

    def _makeNamespace(self, name):
        newNamespace = self._createNamespace([self._getNamespace(), name])
        return newNamespace

    @staticmethod
    def _createNamespace(ns=[]):
        if not isinstance(ns, list):
            ns = [ns]
        for i in ns:
            if not isinstance(i, basestring):
                raise ApiParamError(i, [basestring, list])
        return ".".join(ns).lstrip(".").lower()

    def _whoami(self):
        return inspect.stack()[1][3]

    def getIpc(self):
        return self._ipc

    def setIpc(self, ipc):
        if not isinstance(ipc, iIpcTransport):
            raise ApiParamError(ipc, iIpcTransport)

        if self._ipc != None:
            raise ValueError("Ipc already set!")

        self._ipc = ipc
        self._newIpc()

    def _newIpc(self):
        # Propagate the IPC down to all sub-apis
        for api in self._apis:
            api.ipc = self.ipc

        # Now auto-register our api-handlers
        if hasattr(self, "_registerHandlers"):
            self._registerHandlers()

    def _registerHandlers(self):
        """ Register the handlers to decode the API that are received """
        for handler in dir(self):
            if not handler.startswith(iApi.HANDLER_PREFIX): continue
            _, _, post = handler.partition(iApi.HANDLER_PREFIX)
            self.setHandler(post, getattr(self, handler))

    def _setTransportDataReceiveListener(self, listener):
        if not isinstance(listener, iIpcTransportDataReceiveListener):
            raise ApiParamError(listener, iIpcTransportDataReceiveListener)
        self._transportDataReceiveListener = listener

    def _getTransportDataReceiveListener(self):
        return self._transportDataReceiveListener

    def _setTransportStateChangeListener(self, listener):
        if not isinstance(listener, iIpcTransportStateChangeListener):
            raise ApiParamError(listener, iIpcTransportStateChangeListener)
        self._transportStateChangeListener = listener

    def _getTransportStateChangeListener(self):
        return self._transportStateChangeListener

    def setHandler(self, ns, handler):
        """
        @param handler: callable(tId, *args, **kwargs) specific to the API call
        """
        if not isinstance(ns, basestring):
            raise ApiParamError(ns, basestring)

        ns = ns.lower()
        if handler == None and ns in self._apiHandlers.keys():
            del self._apiHandlers[ns]
        else:
            self._apiHandlers[ns] = handler

    def getHandler(self, ns):
        if ns == None:
            raise ApiParamError(ns, basestring)

        if ns not in self._apiHandlers:
            if iApi.CATCHALL not in self._apiHandlers:
                raise UnsupportedApiError(self._getNamespace(), ns)
            return self._apiHandlers[iApi.CATCHALL]
        return self._apiHandlers[ns]

    def _findHandler(self, ns):
        # Can we process this ns?
        ns = ns.lower()
        handler = None
        if not self._isInMyNamespace(ns):
            raise UnsupportedApiError(self._getNamespace(), ns)

        try:
            _, _, handlerName = ns.partition(self._getNamespacePrefix())
            handler = self.getHandler(handlerName)
        except ApiParamError, _e: raise
        except UnsupportedApiError, _e:
            handler = self.__propagateAPICall(ns)

        if handler == None:
            raise UnsupportedApiError(self._getNamespace(), ns)
        return handler

    def __propagateAPICall(self, ns):
        """ Attempt to propagate a API call to a lower entity within the API """
        for api in self._apis:
            try:
                handler = api._findHandler(ns)
                return handler
            except ApiParamError, _e: raise
            except UnsupportedApiError, _e: pass

    def isInMyNamespace(self, ns):
        try:
            self._isInMyNamespace(ns)
        except UnsupportedApiError:
            return False
        return True

    def handlerExists(self, ns):
        try:
            self._findHandler(ns)
        except UnsupportedApiError:
            return False
        return True

    def _isInMyNamespace(self, ns):
        if ns.startswith(self._getNamespacePrefix()):
            return True
        else: raise UnsupportedApiError(self._getNamespace(), ns)

    def _getNamespacePrefix(self):
        prefix = '%s.' % self._getNamespace()
        return prefix

    def sendAsyncResponse(self, tId, data):
        """ Asynchronously send data back to the opposite API """
        msg = ApiTransportResponse(data)
        # We ignore the tId that sendData returns because we don't care
        self._epyrpc.sendData(msg, transactionId=tId)

    def sendAsyncPartialResponse(self, tId, combinerMethod, index, numChunks, firstChunk):
        """
        @summary: Asynchronously send data back to the opposite API in multiple-chunks.
        @attention: This is the first chunk.
        """
        msg = IpcTransportPartialResponse(tId, combinerMethod, index, numChunks, firstChunk)
        self._epyrpc.sendData(msg, transactionId=tId)

    def _returnChunks(self, tId, chunks, combinerMethod, formatResult):
        #    First send the start-of-extended-transaction:
        index = 0
        result = formatResult(chunks, index)
        self._logger.debug("Sending part [%(I)s] (initial) of partial async response" % {"I":index})
        self.sendAsyncPartialResponse(tId, combinerMethod, index, len(chunks), result)
        if len(chunks) > 2:
            for index in range(1, (len(chunks) - 1)):
                result = formatResult(chunks, index)
                #    Send the next chunk:
                self._logger.debug("Sending part [%(I)s] (intermediate) of partial async response" % {"I":index})
                self.sendAsyncPartialResponse(tId, combinerMethod, index, len(chunks), result)
        if len(chunks) > 1:
            index = (len(chunks) - 1)
            #    Send the terminating chunk:
            result = formatResult(chunks, index)
            self._logger.debug("Sending part [%(I)s] (final) of partial async response" % {"I":index})
            self.sendAsyncPartialResponse(tId, combinerMethod, (len(chunks) - 1), len(chunks), result)
        raise NoResponseRequired(tId)

    def _handleStandardCall(self, tId, bSynchronous, fn, *args, **kwargs):
        """
        @summary: Handle a call that does not perform delayed processing. \
        If the call is synchronous,  return the result from the function \
        directly. If the call is asynchronous, call the function and return \
        the result asynchronously
        @attention: This should be called from the '_handler_*' function \
        directly (probably in 99% of cases)
        """
        if bSynchronous:
            return ApiTransportResponse(fn(*args, **kwargs))
        try:  # We're already in another thread
            result = fn(*args, **kwargs)
        except Exception, result:
            self._logger.exception("Error!")
        self.sendAsyncResponse(tId, result)

    def _handleStandardCheck(self, tId, bSynchronous, checker, *args, **kwargs):
        """
        Check the params, and return the appropriate Exception in the \
        appropriate manor
        @param args: The args to pass to the checker
        @param checker: Method to call to check the params
        @param tId: TransactionId
        @param bSynchronous: True - Call is synchronous, False - otherwise
        @return: The result of the checker
        @raise Exception: The exception from the checker (if applicable in \
        this bSynchronous mode)
        """
        try:
            return checker(*args, **kwargs)
        except Exception, result:
            if bSynchronous: raise
            self.sendAsyncResponse(tId, result)
            r"""    Async method needs to exit the Timer callback immediately 
            without processing the remaining '_handler_*'. ApiBase._wrapHandler will
            catch NoResponseRequired.
            """
            raise NoResponseRequired(tId, result)
        return result

    def getEventsToHandle(self):
        """
        @summary: Obtain this class's list of events which can have handlers \
        set on them
        @note: All events begin: 'EVENT__'
        @not: Works with single and derived classes \
        (single/multiple inheritance).
        @attention: Override for enhanced/simpler behaviour
        """
        events = []
        for attr in dir(self):
            if attr.isupper() and attr.startswith(iApi.EVENT_PREFIX):
                value = getattr(self, attr)
                events.append(value)
        return events

    def getAPIMap(self):
        # Collect all APIs from the lower levels
        apiMap = {}
        apiMap.update(self.__actionNamespaces)

        for api in self._apis:
            apiMap.update(api.getAPIMap())
        return apiMap

    transportDataReceiveListener = property(_getTransportDataReceiveListener,
        _setTransportDataReceiveListener)
    transportStateChangeListener = property(_getTransportStateChangeListener,
        _setTransportStateChangeListener)
    ipc = property(getIpc, setIpc)
