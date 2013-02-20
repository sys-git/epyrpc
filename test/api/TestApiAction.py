
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.AsyncResult import AsyncResult
from epyrpc.api.eSync import eSync
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase
from epyrpc.api.iApi import iApi
from epyrpc.api.iApiAction import iApiAction
from epyrpc.api.iAsyncResult import iAsyncResult
from epyrpc.core.transaction.TransactionManager import TransactionManager
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.synchronisation.StandardTransactionIdGenerator import \
    StandardTransactionGenerator
from epyrpc.utils.synchronisation.TransactionFailed import TransactionFailed
from multiprocessing.synchronize import Semaphore
import threading
import time
import unittest

class MyTransactionManager(TransactionManager):
    def __init__(self):
        super(MyTransactionManager, self).__init__(StandardTransactionGenerator())
        self.lastTid = None
        self.sem = Semaphore(0)
        self.result = []
    def next(self):
        self.lastTid = super(MyTransactionManager, self).next()
        return self.lastTid
    def release(self, tId, result):
        self.sem.release()
        self.result.append((tId, result))
        super(MyTransactionManager, self).release(tId, result)

class MyIpc(iIpcTransport):
    def __init__(self, *args, **kwargs):
        self.tm = MyTransactionManager()
        self.trani = None
    def getTransactionManager(self):
        return self.tm
    def sendData(self, *args, **kwargs):
        self.trani = self.tm.create()
        return self.trani
    def setTransportDataReceiveListener(self, listener):
        pass

class Result(object):
    pass

class TestApiActionNoParams(unittest.TestCase):
    def setUp(self):
        self.threads = []
        self.ipc = MyIpc()
        self.api = XXX(ns="api", ipc=self.ipc)
        setattr(self.api, "ipc", self.ipc)
    def tearDown(self):
        for t in self.threads:
            try:
                t.cancel()
            except: pass
        try:    self.api.teardown()
        except: pass
    def testCallSyncTimeoutIsZero(self):
        #    Test a synchronous call with timeout=0
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.SYNCHRONOUS
        api.timeout = 0
        assert api.sync == eSync.SYNCHRONOUS
        assert api.timeout == None
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(1, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        #    Make that call:
        result = api()
        assert result == eResult
    def testCallAsyncTimeoutIsZero(self):
        #    Test an asynchronous call with timeout=0
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.ASYNCHRONOUS
        api.timeout = 0
        assert api.sync == eSync.ASYNCHRONOUS
        assert api.timeout == None
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(1, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        #    Make that call:
        asyncResult = api()
        assert isinstance(asyncResult, AsyncResult)
        result = asyncResult.acquireNew()
        assert result == eResult
    def testCallSyncTimeoutIsZeroUnsolicited(self):
        #    Test a synchronous call with timeout=0
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.SYNCHRONOUS
        api.timeout = 0
        api.solicited = False
        assert api.sync == eSync.SYNCHRONOUS
        assert api.timeout == None
        assert api.solicited == False
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(1, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        asyncResult = api()
        assert asyncResult == None
    def testCallAsyncTimeoutIsZeroUnsolicited(self):
        #    Test a synchronous call with timeout=0
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.ASYNCHRONOUS
        api.timeout = 0
        api.solicited = False
        assert api.sync == eSync.ASYNCHRONOUS
        assert api.timeout == None
        assert api.solicited == False
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(1, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        asyncResult = api()
        assert isinstance(asyncResult, AsyncResult)
        result = asyncResult.acquireNew()
        assert result == eResult
    def _release(self, eResult):
        tId = self.ipc.trani
        self.ipc.getTransactionManager().release(tId, eResult)
    def testCallSyncTimesOut(self):
        #    Test a synchronous call with a 5 second timeout.
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.SYNCHRONOUS
        api.timeout = 1
        assert api.sync == eSync.SYNCHRONOUS
        assert api.timeout == 1
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(2, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        #    Make that call:
        try:
            api()
        except TransactionFailed, e:
            tId = self.ipc.trani
            assert e.message == tId
        else:
            assert False
    def testCallAsyncTimesOut(self):
        #    Test a synchronous call with a 5 second timeout.
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.ASYNCHRONOUS
        api.timeout = 1
        assert api.sync == eSync.ASYNCHRONOUS
        assert api.timeout == 1
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(2, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        #    Make that call:
        asyncResult = api()
        assert isinstance(asyncResult, AsyncResult)
        try:
            asyncResult.acquireNew()
        except TransactionFailed, e:
            tId = self.ipc.trani
            assert e.message == tId
        else:
            assert False
    def testCallSyncDoesNotTimeout(self):
        #    Test a synchronous call with a 5 second timeout.
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.SYNCHRONOUS
        api.timeout = 2
        assert api.sync == eSync.SYNCHRONOUS
        assert api.timeout == 2
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(1, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        #    Make that solicited call:
        result = api()
        assert result == eResult
    def testCallAsyncDoesNotTimeout(self):
        #    Test a synchronous call with a 5 second timeout.
        api = self.api.signalFilter.status()
        assert api.sync == iApiAction.DEFAULT_SYNC == eSync.SYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.sync = eSync.ASYNCHRONOUS
        api.timeout = 2
        assert api.sync == eSync.ASYNCHRONOUS
        assert api.timeout == 2
        #    Now do the business.....
        eResult = Result()
        self.tid = None
        t = threading.Timer(1, self._release, args=[eResult])
        self.threads.append(t)
        t.start()
        #    Make that solicited call:
        asyncResult = api()
        assert isinstance(asyncResult, AsyncResult)
        result = asyncResult.acquireNew()
        assert result == eResult
    def testCallAsyncCallbackTimesOut(self, **kwargs):
        #    Test an asynchronous call where the callback times-out.
        self.api = MyApi("test", ns="api")
        setattr(self.api, "ipc", self.ipc)
        api = self.api.parent.method_a(1, 2, 3, four=4, five=5)
        api.sync = eSync.ASYNCHRONOUS
        assert api.sync == eSync.ASYNCHRONOUS
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT == None
        api.timeout = 1
        assert api.timeout == 1
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        assert asyncResult
        tId = asyncResult.tId()
        assert tId
        try:
            #    Acquire with the default timeout:
            asyncResult.acquireNew(**kwargs)
        except TransactionFailed, e:
            assert e.message == tId
        else:
            assert False
    def testCallAsyncCallbackTimesOutCustomTimeout(self):
        self.testCallAsyncCallbackTimesOut(timeout=3)
    def testTimer(self):
        aa = ApiAction(self.ipc, "api", True)
        tm = MyTransactionManager()
        aa.timeout = 1
        aa._startCallbackTimeoutTimer(None, 123, tm)
        assert not tm.sem.acquire(block=False)
        assert tm.sem.acquire(timeout=2)
        assert len(tm.result) == 1
        assert isinstance(tm.result[0][1], TransactionFailed)
    def testTimerIsNone(self):
        aa = ApiAction(self.ipc, "api", True)
        tm = MyTransactionManager()
        aa.timeout = None
        aa._startCallbackTimeoutTimer(None, 123, tm)
        assert not tm.sem.acquire(timeout=1)

class Parent(iApi):
    logger = LogManager().getLogger("Parent")
    def __init__(self, ns="", solicited=True, ipc=None):
        super(Parent, self).__init__(ns, solicited)
    def method_a(self, *args, **kwargs):
        #    Call a method which times-out:
        Parent.logger.debug("method_a")
        #    Return the ApiAction object, the caller can then change the sync/timeout for it - then call it.
        api = ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *args, **kwargs)
        return api
    def _handler_method_a(self, tId, synchronous, *args, **kwargs):
        time.sleep(5)

class MyApi(ApiBase):
    logger = LogManager().getLogger("MyApi")
    def _setup(self, **kwargs):
        self.parent = Parent(**kwargs)
        self._apis.append(self.parent)
    def transportDataReceive(self, tId, data):
        return super(MyApi, self).transportDataReceive(tId, data)

class TestCallParamPassing(unittest.TestCase):
    def executeAction(self):
        self.called = True
    def cb(self):
        pass
    def setUp(self):
        self.api = ApiAction(None, "", True)
        self.api._executeAction = self.executeAction
    def testSync(self):
        #    Now call the api with override params:
        esync = [eSync.ASYNCHRONOUS, eSync.SYNCHRONOUS, eSync.ASYNCHRONOUS, eSync.SYNCHRONOUS]
        for i in esync:
            self.called = False
            self.api(sync=i)
            assert self.api.sync == i
            assert self.called == True
    def testCallback(self):
        #    Now call the api with override params:
        cb = [None, self.cb, None]
        for i in cb:
            self.api(callback=i)
            assert self.api.callback == i
    def testSolicited(self):
        #    Now call the api with override params:
        sol = [True, False, True, False]
        for i in sol:
            self.api(solicited=i)
            assert self.api.solicited == i
    def testTimeout(self):
        #    Now call the api with override params:
        tout = [None, 1, 2, 3]
        for i in tout:
            self.api(timeout=i)
            assert self.api.timeout == i

if __name__ == '__main__':
    unittest.main()
