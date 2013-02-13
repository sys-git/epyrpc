
from Queue import Empty
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.api.iApi import iApi
from epyrpc.api.iApiTransportItem import iApiTransportItem
from epyrpc.core.IpcExceptions import NoResponseRequired
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener
from epyrpc.utils.LogManager import LogManager
from multiprocessing.queues import Queue
from multiprocessing.synchronize import Semaphore
import itertools
import threading
import time

def _wrapHandler(handler, *args, **kwargs):
    r"""    This allows us to silently consume the async api handler raising 
    NoResponseRequired from within iApi._handleStandardCheck() - the async
    response has already been sent so no need to pollute the logger with an
    unexpected 'panic-time' exception stack-trace!
    """
    try:
        handler(*args, **kwargs)
    except NoResponseRequired, _e:  pass
    except: raise

class ApiBaseOld(iApi, iIpcTransportDataReceiveListener):
    def __init__(self, name, ns="", solicited=True, ignoreUnhandled=False, maxAsync=None):
        super(ApiBaseOld, self).__init__(ns=ns, solicited=solicited, name=name)
        self._setup(ns=self._getNamespace(), solicited=self.solicited, ipc=self.ipc)
        self._dataRxCount = itertools.count(0)
        self._ignoreUnhandled = ignoreUnhandled
    def _newIpc(self):
        super(ApiBaseOld, self)._newIpc()
        #    Now bind our data-receive listener to the IPC:
        self._epyrpc.setTransportDataReceiveListener(self)
    def transportDataReceive(self, tId, data):
        r"""
        @summary: Data is received that is NOT part of an existing transaction.
        We need to decide what to do with it...
        Recursively ask each of our sub-api's to decode the data and handle it.
        If no one can, then return UnsupportedApiError() (unless we consume it with:
        self._ignoreUnhandled==True).
        The handlers will have previously been set by the controlling entity, ie:
        ExecutionOrganiser, Head.
        Asynchronous calls return immediately with NoResponseRequired.
        @FIXME: Make the synchronous call actually handled asynchronously WRT to
        the receiver - The underlying IPC does has no concept of the difference
        between sync and async as long as we return NoResponseRequired() to make
        the call asynchronous.
        """
        try:
            count = self._dataRxCount.next()
            if isinstance(data, iApiTransportItem):
                ns = data.ns()
                if self._isInMyNamespace(ns):
                    handler = self._findHandler(ns)
                    args = data.args()
                    kwargs = data.kwargs()
                    synchronous = data.synchronous()
                    if synchronous:
                        r"""
                        FIXME: Make the synchronous call asynchronous by wrapping the call to the handler
                        in a method which handles the returning of the data.
                        """
                        return handler(tId, synchronous, *args, **kwargs)
                    else:
                        self._callHandler(ns, handler, tId, synchronous, count, *args, **kwargs)
                        raise NoResponseRequired(ns)
            else:
                #    Inform our listener about the data that we can't handle:
                l = self.transportDataReceiveListener
                if l != None:
                    return l(tId, data)
                raise NoResponseRequired(tId)
        except UnsupportedApiError, e:
            if self._ignoreUnhandled == False:
                #    Propagate exception directly as before.
                raise
            #    Consume silently:
            self._logger.debug("UnsupportedApiError: %(NS)s" % {"NS":e.message})
            raise NoResponseRequired(e.ns(), e)
    def _callHandler(self, ns, handler, tId, synchronous, count, *args, **kwargs):
        r"""
        @summary: Call the handler asynchronously, any immediate error is returned via the IPC.
        """
        newArgs = [handler, tId, synchronous]
        newArgs += args
        t = threading.Thread(target=_wrapHandler, args=newArgs, kwargs=kwargs)
        t.setName("ApiAsyncRxHdlr_%(C)s_%(NS)s" % {"C":count, "NS":ns})
        t.start()

class ApiAsyncWorker(threading.Thread):
    ID = itertools.count(1)
    @staticmethod
    def startAll(workers=[]):
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.waitUntilRunning()
    @staticmethod
    def create(q, parent, start=False):
        worker = ApiAsyncWorker(q, parent)
        if start:
            ApiAsyncWorker.startAll([worker])
        return worker
    def __init__(self, q, parent):
        super(ApiAsyncWorker, self).__init__()
        self._q = q
        self._parent = parent
        self._name = "ApiAsyncWorker_%(C)s" % {"C":ApiAsyncWorker.ID.next()}
        self._logger = LogManager().getLogger(self._name)
        self.setDaemon(True)
        self.setName(self._name)
        self._cancel = False
        self._runLock = Semaphore(0)
    def stop(self):
        self._cancel = True
    def waitUntilRunning(self, timeout=None):
        # Wait until we become running:
        return self._runLock.acquire(block=True, timeout=timeout)
    def run(self):
        self._logger.debug("Thread running...")
        self._runLock.release()
        #    Now do the work:
        try:
            self._work()
        except EOFError, _e:
            self._logger.warn("EOF in thread...")
        except Exception, _e:
            self._logger.exception("Unhandled error in thread:")
        self._logger.debug("Thread finished!")
    def _work(self):
        while self._cancel == False:
            try:
                data = self._q.get(block=True, timeout=1)
            except IOError, e:
                if e.errno == 9:
                    #    Queue has been remotely closed.
                    self._logger.debug("Closing due to queue closure...")
                    break
            except Empty, _e:
                continue
            else:
                if isinstance(data, STOP):
                    self._logger.debug("Told to close...")
                    break
                self._execute(data)
    def _execute(self, data):
        tId = data.tId()
        try:
            if isinstance(data, UNKNOWN):
                handler = self._parent.transportDataReceiveListener
                data_ = data.data()
                #    Call the TransportDataReceive listener:
                rtn = handler(tId, data_)
            elif isinstance(data, KNOWN):
                ns = data.ns()
                count = data.count()
                handler = self._parent._findHandler(ns)
                self._logger.debug("Executing api[%(C)s]: %(NS)s" % {"NS":ns, "C":count})
                synchronous = data.synchronous()  #    FIXME: Not required any more!
                args = data.args()
                kwargs = data.kwargs()
                #    Call the api handler:
                rtn = handler(tId, synchronous, *args, **kwargs)
        except NoResponseRequired, _e:
            self._logger.debug("NoResponseRequired, ignoring!")
            return
        except Exception, rtn:
            self._logger.exception("Exception on execute")
        if tId != None:
            try:
                self._parent.ipc.sendData(rtn, solicited=True, transactionId=tId)
            except Exception, _e:
                #    Honestly, we don't care!
                pass

class _Base(object):
    def __init__(self, tId):
        self._tId = tId
    def tId(self):
        return self._tId

class KNOWN(_Base):
    def __init__(self, ns, tId, synchronous, count, args, kwargs):
        super(KNOWN, self).__init__(tId)
        self._ns = ns
        self._synchronous = synchronous
        self._count = count
        self._args = args
        self._kwargs = kwargs
    def ns(self):
        return self._ns
    def count(self):
        return self._count
    def args(self):
        return self._args
    def kwargs(self):
        return self._kwargs
    def synchronous(self):
        return self._synchronous

class UNKNOWN(_Base):
    def __init__(self, tId, data):
        super(UNKNOWN, self).__init__(tId)
        self._data = data
    def data(self):
        return self._data

class STOP(object): pass

class ApiBase(iApi, iIpcTransportDataReceiveListener):
    r"""
    @summary: The base-class to the top-level api object ONLY, not sub-apis.
    """
    DEFAULT_MAX_ASYNC_HANDLERS = 1
    def __init__(self, name, ns="", solicited=True, ignoreUnhandled=False, maxAsync=None):
        super(ApiBase, self).__init__(ns=ns, solicited=solicited, name=name)
        self._setup(ns=self._getNamespace(), solicited=self.solicited, ipc=self.ipc)
        self._dataRxCount = itertools.count(0)
        self._ignoreUnhandled = ignoreUnhandled
        if (maxAsync == None) or (maxAsync < 1):
            maxAsync = ApiBase.DEFAULT_MAX_ASYNC_HANDLERS
        self._maxAsync = maxAsync
        self._q = Queue()
        self._workers = []
        self._createAsyncWorkers()
        self.isAlive = True
    def _createAsyncWorkers(self, start=True):
        #    Create the thread pool to handle the api calls.
        for _ in range(0, self._maxAsync):
            thread = ApiAsyncWorker.create(self._q, self, start=start)
            self._workers.append(thread)
        self._logger.debug("Created workers.")
    def __del__(self):
        self.teardown()
    def teardown(self):
        if self is threading.current_thread(): return 
        if not self.isAlive: return
        self.isAlive = False
        #    Unfortunately we require time to stop the workers.
        self._logger.debug("Stopping async workers...")
        for _ in range(0, self._maxAsync):
            self._q.put(STOP())
        time.sleep(1)
        for worker in self._workers:
            worker.stop()
        for worker in self._workers:
            if worker.isAlive(): worker.join()
        self._workers = []
        self._q.close()
        time.sleep(1)
        del self._q
        self._q = None
        self._logger.debug("Stopped async workers (all daemon anyway).")
        #    Now un-bind our data-receive listener from the IPC:
        if self._ipc != None:
            self._epyrpc.setTransportDataReceiveListener(self)
        self._ipc = None
    def _newIpc(self):
        super(ApiBase, self)._newIpc()
        #    Now bind our data-receive listener to the IPC:
        self._epyrpc.setTransportDataReceiveListener(self)
    def transportDataReceive(self, tId, data):
        r"""
        @summary: Data is received that is NOT part of an existing transaction.
        We need to decide what to do with it...
        Recursively ask each of our sub-api's to decode the data and handle it.
        If no one can, then return UnsupportedApiError() (unless we consume it with:
        self._ignoreUnhandled==True).
        The handlers will have previously been set by the controlling entity, ie:
        ExecutionOrganiser, Head.
        This method always returns NoResponseRequired, making the call asynchronous.
        """
        myNsPrefix = self._getNamespacePrefix()
        try:
            count = self._dataRxCount.next()
            if isinstance(data, iApiTransportItem):
                ns = data.ns()
                if self._isInMyNamespace(ns):
                    self._findHandler(ns)
                    args = data.args()
                    kwargs = data.kwargs()
                    synchronous = True
                    self._q.put(KNOWN(ns, tId, synchronous, count, args, kwargs))
                    raise NoResponseRequired(ns)
            else:
                #    Inform our listener about the data that we can't handle:
                handler = self.transportDataReceiveListener
                if handler != None:
                    self._q.put(UNKNOWN(tId, data))
                raise NoResponseRequired(myNsPrefix)
        except UnsupportedApiError, e:
            if self._ignoreUnhandled == False:
                #    Propagate exception directly as before.
                raise
            #    Consume silently:
            self._logger.debug("UnsupportedApiError: %(NS)s" % {"NS":e.ns()})
            raise NoResponseRequired(myNsPrefix, e)

