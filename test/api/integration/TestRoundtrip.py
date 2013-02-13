from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.AsyncResult import AsyncResult
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.api.eSync import eSync
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase
from epyrpc.api.iApi import iApi
from epyrpc.api.iAsyncResult import iAsyncResult
from epyrpc.core.transaction.TransactionManager import TransactionManager
from epyrpc.core.transport.details.QueueTransportDetails import \
    QueueTransportDetails
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener
from epyrpc.core.transport.queue.QueueTransporter import QueueTransporter
from epyrpc.synchronisation.generators.HeadTransactionIdGenerator import \
    HeadTransactionIdGenerator
from epyrpc.synchronisation.generators.NeckTransactionIdGenerator import \
    NeckTransactionIdGenerator
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.synchronisation.TransactionFailed import TransactionFailed
from multiprocessing.synchronize import Semaphore
import time
import unittest

class CustomException(Exception): pass

class Api(ApiBase):
    logger = LogManager().getLogger("Api")
    def _setup(self, **kwargs):
        self.parent = Parent(**kwargs)
        self._apis.append(self.parent)
    def transportDataReceive(self, tId, data):
        return super(Api, self).transportDataReceive(tId, data)

class Parent(iApi):
    logger = LogManager().getLogger("Parent")
    def __init__(self, ns="", solicited=True, ipc=None):
        super(Parent, self).__init__(ns, solicited)
        self.eResult = None
    def method_a(self, *args, **kwargs):
        #    Request a PING back of the exact data:
        Parent.logger.debug("method_a")
        #    Return the ApiAction object, the caller can then change the sync/timeout for it - then call it.
        api = ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *args, **kwargs)
        return api
    def _handler_method_a(self, tId, synchronous, *args, **kwargs):
        #    Action a PING back of the exact data:
        Parent.logger.debug("_handler_method_a")
        if self.eResult.returnExact:
            result = (args, kwargs)
        else:
            result = self.eResult.altResult
        if synchronous:
            return result
        else:
            self.sendAsyncResponse(tId, result)
    def method_b(self, *args, **kwargs):
        #    Raises NoResponseRequired
        Parent.logger.debug("method_b")
        #    Return the ApiAction object, the caller can then change the sync/timeout for it - then call it.
        api = ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *args, **kwargs)
        return api
    def method_c(self, *args, **kwargs):
        #    Times-out
        Parent.logger.debug("method_c")
        #    Return the ApiAction object, the caller can then change the sync/timeout for it - then call it.
        api = ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *args, **kwargs)
        return api
    def _handler_method_c(self, tId, synchronous, *args, **kwargs):
        Parent.logger.debug("_handler_method_c")
        time.sleep(5)

class My1Listener(iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener):
    def transportStateChange(self, e_ipc_transport_state):
        pass

class MyResult(object):
    def __init__(self):
        self.returnExact = False
        self.altResult = None

class Result(object):
    def __init__(self):
        self.args = 123

class ExceptionResult(Exception): pass

class TestRoundTripSynchronous(unittest.TestCase):
    def setUp(self):
        self.logger = LogManager().getLogger("test")
        self.mr = MyResult()
        #    Create the IPC:
        tmHead = TransactionManager(HeadTransactionIdGenerator())
        tmNeck = TransactionManager(NeckTransactionIdGenerator())
        self.hl = My1Listener()
        self.nl = My1Listener()
        self.qTransport = QueueTransportDetails()
        self.ipcHead = QueueTransporter(self.qTransport, tmHead, self.hl, logger=LogManager().getLogger("Head"))
        self.ipcNeck = QueueTransporter(self.qTransport.invert(), tmNeck, self.nl, logger=LogManager().getLogger("Neck"))
        #    Symmetrical api:
        self.apiHead = Api("test")
        self.apiHead.ipc = self.ipcHead
        self.apiNeck = Api("test", solicited=True)
        self.apiNeck.ipc = self.ipcNeck
        #    Set the expected result object:
        self.apiNeck.parent.eResult = self.mr
    def tearDown(self):
        self.ipcHead.close(ignoreErrors=True)
        self.ipcNeck.close(ignoreErrors=True)
        try:    self.apiHead.teardown()
        except: pass
        try:    self.apiNeck.teardown()
        except: pass
    def test(self):
        r"""
        Create a single 2 layer symmetrical api with
        simple cause-and-effect.
        """ 
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        self.mr.returnExact = True
        result = api()
        assert result[0] == args
        assert result[1] == kwargs
    def testCustomResult(self):
        r"""
        Create a single 2 layer symmetrical api with
        simple cause-and-effect.
        """ 
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        self.mr.returnExact = False
        self.mr.altResult = eResult
        result = api()
        assert result.args == eResult.args, "Got: %(R)s" % {"R":result}
    def testCustomExceptionResult(self):
        eResult = ExceptionResult()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        self.mr.returnExact = False
        self.mr.altResult = eResult
        try:
            api()
        except ExceptionResult, _e:
            assert True
        else:
            assert False
    def testUnsupportedApiError(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_b(*args, **kwargs)
        try:
            api()
        except UnsupportedApiError, e:
            assert e.ns().lower() == u"api.parent.method_b"
        else:
            assert False
    def testApiTimesOut(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_c(*args, **kwargs)
        api.timeout = 1
        try:
            api()
        except TransactionFailed, _e:
            assert True
        else:
            assert False
    def testHeadCatchallUnsolicitedEvent(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiNeck.parent.method_b(*args, **kwargs)
        #    Test the API is unsupported first:
        try:
            _result = api()
        except UnsupportedApiError, _e:
            assert True
        else:
            assert False
        #    Now test the api is supported after we add out catchall handler:
        self.logger.warn("let's play...")
        eResult = "hello.world!"
        caught = Semaphore(0)
        def headCatchallHandler(tId, *args, **kwargs):
            caught.release()
        self.apiHead.parent.setHandler(iApi.CATCHALL, headCatchallHandler)
        api = self.apiNeck.parent.method_b(*args, **kwargs)
        api.solicited = False
        assert api() == None
        assert caught.acquire(timeout=5)
    def testCallbackOnApiResponse(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        self.mr.returnExact = True
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        cbData = []
        cbReceived = Semaphore(0)
        def cb(tId, data):
            cbData.append((tId, data))
            cbReceived.release()
        api.sync = eSync.SYNCHRONOUS
        api.callback = cb
        api.solicited = True
        asyncResult = api()
        assert isinstance(asyncResult, AsyncResult)
        tId = asyncResult.tId()
        #    Now wait for the callback to have been called:
        assert cbReceived.acquire(timeout=5)
        assert cbData[0][0] == tId
        assert cbData[0][1] == (args, kwargs)
        #    The semaphore should NOT be acquirable:
        try:
            self.ipcHead.getTransactionManager().acquireNew(tId)
        except TypeError, _e:
            assert True
        else:
            assert False

class TestRoundTripAsynchronous(unittest.TestCase):
    def setUp(self):
        self.logger = LogManager().getLogger("test")
        self.mr = MyResult()
        #    Create the IPC:
        tmHead = TransactionManager(HeadTransactionIdGenerator())
        tmNeck = TransactionManager(NeckTransactionIdGenerator())
        self.hl = My1Listener()
        self.nl = My1Listener()
        self.qTransport = QueueTransportDetails()
        self.ipcHead = QueueTransporter(self.qTransport, tmHead, self.hl, logger=LogManager().getLogger("Head"))
        self.ipcNeck = QueueTransporter(self.qTransport.invert(), tmNeck, self.nl, logger=LogManager().getLogger("Neck"))
        #    Symmetrical api:
        self.apiHead = Api("test")
        self.apiHead.ipc = self.ipcHead
        self.apiNeck = Api("test", solicited=True)
        self.apiNeck.ipc = self.ipcNeck
        #    Set the expected result object:
        self.apiNeck.parent.eResult = self.mr
    def tearDown(self):
        self.ipcHead.close(ignoreErrors=True)
        self.ipcNeck.close(ignoreErrors=True)
        try:    self.apiHead.teardown()
        except: pass
        try:    self.apiNeck.teardown()
        except: pass
    def test(self):
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        self.mr.returnExact = True
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        #    Now wait on the asynchronous result:
        result = asyncResult.acquireNew()
        assert result == (args, kwargs)
        #    Check that the tId is NOT purged.
        assert asyncResult.tId() in self.ipcHead.getTransactionManager()._items
    def testWithPurge(self):
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        self.mr.returnExact = True
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        #    Now wait on the asynchronous result:
        result = asyncResult.acquireNew(purge=True)
        assert result == (args, kwargs)
        #    Check that the tId IS purged.
        assert asyncResult.tId() not in self.ipcHead.getTransactionManager()._items
    def testCustomResult(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        self.mr.returnExact = False
        self.mr.altResult = eResult
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        #    Now wait on the asynchronous result:
        result = asyncResult.acquireNew()
        assert result.args == eResult.args, "Got: %(R)s" % {"R":result}
    def testCustomExceptionResult(self):
        eResult = ExceptionResult()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        self.mr.returnExact = False
        self.mr.altResult = eResult
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        try:
            #    Now wait on the asynchronous result:
            asyncResult.acquireNew()
        except ExceptionResult, _result:
            assert True
        else:
            assert False
    def testUnsupportedApiError(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_b(*args, **kwargs)
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        try:
            asyncResult.acquireNew()
        except UnsupportedApiError, e:
            assert e.ns().lower() == u"api.parent.method_b"
        else:
            assert False
    def testApiTimesOut(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_c(*args, **kwargs)
        api.timeout = 1
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        try:
            asyncResult.acquireNew()
        except TransactionFailed, _e:
            assert True
        else:
            assert False
    def testCallbackOnApiResponse(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        self.mr.returnExact = True
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_a(*args, **kwargs)
        cbData = []
        cbReceived = Semaphore(0)
        def cb(tId, data):
            cbData.append((tId, data))
            cbReceived.release()
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        api.callback = cb
        api.solicited = True
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        assert asyncResult
        tId = asyncResult.tId()
        assert tId
        #    Now wait for the callback to have been called:
        assert cbReceived.acquire(timeout=5)
        assert cbData[0][0] == tId
        assert cbData[0][1] == (args, kwargs)
        #    The semaphore should NOT be acquirable:
        try:
            self.ipcHead.getTransactionManager().acquireNew(tId)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testCallbackOnApiTimeout(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        self.mr.returnExact = True
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiHead.parent.method_c(*args, **kwargs)
        cbData = []
        cbReceived = Semaphore(0)
        def cb(tId, data):
            cbData.append((tId, data))
            cbReceived.release()
        #    Make the call asynchronous:
        api.sync = eSync.ASYNCHRONOUS
        api.callback = cb
        api.solicited = True
        api.timeout = 1
        asyncResult = api()
        assert isinstance(asyncResult, iAsyncResult)
        assert asyncResult
        tId = asyncResult.tId()
        assert tId
        #    Now wait for the callback to have been called:
        assert cbReceived.acquire(timeout=5)
        assert cbData[0][0] == tId
        assert isinstance(cbData[0][1], TransactionFailed)
        #    The semaphore should NOT be acquirable:
        try:
            self.ipcHead.getTransactionManager().acquireNew(tId)
        except TypeError, _e:
            assert True
        else:
            assert False

class TestRoundTripSynchronousUnsolicitedNeck(unittest.TestCase):
    def setUp(self):
        self.logger = LogManager().getLogger("test")
        self.mr = MyResult()
        #    Create the IPC:
        tmHead = TransactionManager(HeadTransactionIdGenerator())
        tmNeck = TransactionManager(NeckTransactionIdGenerator())
        self.hl = My1Listener()
        self.nl = My1Listener()
        self.qTransport = QueueTransportDetails()
        self.ipcHead = QueueTransporter(self.qTransport, tmHead, self.hl, logger=LogManager().getLogger("Head"))
        self.ipcNeck = QueueTransporter(self.qTransport.invert(), tmNeck, self.nl, logger=LogManager().getLogger("Neck"))
        #    Symmetrical api:
        self.apiHead = Api("test")
        self.apiHead.ipc = self.ipcHead
        self.apiNeck = Api("test", solicited=False)
        self.apiNeck.ipc = self.ipcNeck
        #    Set the expected result object:
        self.apiNeck.parent.eResult = self.mr
    def tearDown(self):
        self.ipcHead.close(ignoreErrors=True)
        self.ipcNeck.close(ignoreErrors=True)
        try:    self.apiHead.teardown()
        except: pass
        try:    self.apiNeck.teardown()
        except: pass
    def testHeadCatchallUnsolicitedEvent(self):
        eResult = Result()
        self.apiHead.parent.eResult = eResult
        self.ipcHead.connect()
        self.ipcNeck.connect()
        args = (0, 1, 2, 3)
        kwargs = {"four":4, "five":5}
        api = self.apiNeck.parent.method_b(*args, **kwargs)
        #    Test the API is unsupported first:
        #    Make it solicited so we can test that it's not supported:
        api.solicited = True
        try:
            api()
        except UnsupportedApiError, e:
            assert e.ns().lower() == u"api.parent.method_b"
        else:
            assert False
        #    Now test the api is supported after we add out catchall handler:
        self.logger.warn("let's play...")
        eResult = "hello.world!"
        caught = Semaphore(0)
        def headCatchallHandler(tId, *args, **kwargs):
            caught.release()
            return eResult
        self.apiHead.parent.setHandler(iApi.CATCHALL, headCatchallHandler)
        api = self.apiNeck.parent.method_b(*args, **kwargs)
        result = api()
        assert result == None
        assert caught.acquire(timeout=5), "Catchall handler not called!"

if __name__ == '__main__':
    unittest.main()
