
from epyrpc.api.ApiTransportItem import ApiTransportItem
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase, KNOWN, UNKNOWN
from epyrpc.core.IpcExceptions import NoResponseRequired
from epyrpc.utils.LogManager import LogManager
from multiprocessing.synchronize import Semaphore
import copy
import itertools
import random
import time
import unittest

def setup_module():
    r"""
    @TODO: Disable exception printing when running on Jenkins.
    """
    pass

class CustomException(Exception):
    def __init__(self, value=None):
        super(CustomException, self).__init__()
        self.value = value
    def __eq__(self, other):
        if isinstance(other, CustomException):
            return other.value == self.value

class MyApi(ApiBase):
    def _setup(self, *args, **kwargs):
        pass

class MyApi1(MyApi):
    def __init__(self, *args, **kwargs):
        super(MyApi1, self).__init__(*args, **kwargs)
        self._parent = SupportedApiParent()
    def _createAsyncWorkers(self, start=True):
        pass
    def transportDataReceiveListener(self, tId, data):
        pass

class MyApi2(MyApi):
    def __init__(self, *args, **kwargs):
        super(MyApi2, self).__init__(*args, **kwargs)
        self.handled = None
        self.handledLock = Semaphore(0)
        self._parent = SupportedApiParent()
    def transportDataReceiveListener(self, tId, data):
        self.handled = (tId, data)
        self.handledLock.release()

class TestThreadPool(unittest.TestCase):
    def setUp(self):
        self.api = None
        self._logger = LogManager().getLogger("TestThreadPool")
    def tearDown(self):
        if self.api:
            self.api.teardown()
    def testMaxAsyncIsNone(self):
        self._logger.warn("testMaxAsyncIsNone")
        self.api = MyApi("test", ns="Test.YouView", ignoreUnhandled=True, maxAsync=None)
        assert len(self.api._workers) == 1
    def testMaxAsyncIsOne(self, count=1):
        self._logger.warn("testMaxAsyncIsOne")
        self.api = MyApi("test", ns="Test.YouView", ignoreUnhandled=True, maxAsync=count)
        assert len(self.api._workers) == count
    def testMaxAsyncIsTen(self):
        self._logger.warn("testMaxAsyncIsTen")
        self.testMaxAsyncIsOne(count=10)
    def testKnownOnQueue(self):
        self._logger.warn("testKnownOnQueue")
        ns = "Test.YouView"
        self.api = MyApi1("test", ns=ns, ignoreUnhandled=True, maxAsync=1)
        self.api.setHandler("voo", self._handler)
        tNs = ns + ".myapi1.voo"
        tNs = tNs.lower()
        d = ApiTransportItem(tNs, [], {}, True)
        tId = (1, 123)
        try:
            self.api.transportDataReceive(tId, d)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
        #    Now check that the q contains the KNOWN object.
        data = self.api._q.get(timeout=1)
        assert isinstance(data, KNOWN)
        assert data.tId() == tId
        assert data.ns() == tNs
        assert data.synchronous() == True
    def _handler(self, *args, **kwargs):
        pass
    def testUnknownOnQueue(self):
        self._logger.warn("testUnknownOnQueue")
        ns = "Test.YouView"
        self.api = MyApi1("test", ns=ns, ignoreUnhandled=True, maxAsync=1)
        d = CustomException(456)
        tId = (1, 123)
        try:
            self.api.transportDataReceive(tId, d)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
        #    Now check that the q contains the UNKNOWN object.
        data = self.api._q.get(timeout=1)
        assert isinstance(data, UNKNOWN)
        assert data.tId() == tId
    def testKnownHandled(self):
        self._logger.warn("testKnownHandled")
        ns = "Test.YouView"
        self.api = MyApi2("test", ns=ns, ignoreUnhandled=True, maxAsync=1)
        self.api.setHandler("voo", self._handler2)
        tNs = ns + ".myapi2.voo"
        tNs = tNs.lower()
        d = ApiTransportItem(tNs, [], {}, True)
        tId = (1, 123)
        self._handler2 = None
        self._handler2Lock = Semaphore(0)
        try:
            self.api.transportDataReceive(tId, d)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
        #    Now check that the handler was called:
        assert self._handler2Lock.acquire(timeout=1)
        assert self._handler2 != None
        (tId_, synchronous_, args_, kwargs_) = self._handler2
        assert tId_ == tId
        assert synchronous_ == True
        assert args_ == tuple([])
        assert kwargs_ == {}
    def testUnknownHandled(self):
        self._logger.warn("testUnknownHandled")
        ns = "Test.YouView"
        self.api = MyApi2("test", ns=ns, ignoreUnhandled=True, maxAsync=1)
        self.api.setHandler("voo", self._handler2)
        tNs = ns + ".myapi2.voo"
        tNs = tNs.lower()
        d = CustomException(456)
        tId = (1, 123)
        try:
            self.api.transportDataReceive(tId, d)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
        #    Now check that the handler was called:
        assert self.api.handledLock.acquire(timeout=1)
        assert self.api.handled != None
        (tId_, data_) = self.api.handled
        assert tId_ == tId
        assert data_ == d
    def _handler2(self, tId, synchronous, *args, **kwargs):
        self._handler2 = (tId, synchronous, args, kwargs)
        self._handler2Lock.release()
    def _handler3(self, tId, synchronous, *args, **kwargs):
        time.sleep(self._handler3AsyncBlockingTimeout)
        self._logger.debug("Handler complete: [%(T)s]!" % {"T":tId})
        self._handler3Result[tId] = (synchronous, args, kwargs)
        self._handler3Lock.release()
    def testMultipleHandledSimultaneously(self, count=10, numCalls=10, asyncBlockingTimeout=4):
        self._logger.warn("testMultipleHandledSimultaneously")
        ns = "Test.YouView"
        self.api = MyApi3("test", ns=ns, ignoreUnhandled=True, maxAsync=count)
        self.api.setHandler("voo", self._handler3)
        tNs = ns + ".myapi3.voo"
        tNs = tNs.lower()
        self._handler3Result = {}
        self._handler3Lock = Semaphore(0)
        self._handler3AsyncBlockingTimeout = asyncBlockingTimeout
        #    Now make the simultaneous calls:
        _tId = itertools.count(0)
        eResult = {}
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for _ in range(0, numCalls):
            tId = (123, _tId.next())
            i = copy.copy(items)
            random.shuffle(i)
            args = i
            j = copy.copy(i)
            random.shuffle(j)
            kwargs = {"a":j}
            data = ApiTransportItem(tNs, args, kwargs, True)
            eResult[tId] = data
            try:
                self.api.transportDataReceive(tId, data)
            except NoResponseRequired, _e:
                assert True
            else:
                assert False
        #    Calculate the max theoretical timeout:
        mos = 5
        eTimeout = ((float(numCalls) / float(count)) * asyncBlockingTimeout) + mos
        for _ in range(0, numCalls):
            self._logger.debug("Waiting for %(T)s seconds..." % {"T":eTimeout})
            self._handler3Lock.acquire(timeout=eTimeout)
        #    Now check results:
        hr = self._handler3Result
        for key, value in eResult.items():
            assert key in hr.keys()
            (synchronous_, args, kwargs) = hr[key]
            assert synchronous_ == True
            args_ = tuple(value.args())
            assert args == args_
            kwargs_ = value.kwargs()
            assert kwargs == kwargs_
        pass
    def testMultipleHandledSimultaneouslyHammer(self):
        self._logger.warn("testMultipleHandledSimultaneouslyHammer")
        self.testMultipleHandledSimultaneously(count=10, numCalls=100, asyncBlockingTimeout=1)
    def testMultipleHandledSimultaneouslyHammerLots(self):
        self._logger.warn("testMultipleHandledSimultaneouslyHammerLots")
        self.testMultipleHandledSimultaneously(count=50, numCalls=1000, asyncBlockingTimeout=1)
    def testMultipleHandledSimultaneouslyHammerOneHandler(self):
        self._logger.warn("testMultipleHandledSimultaneouslyHammerOneHandler")
        self.testMultipleHandledSimultaneously(count=1, numCalls=100, asyncBlockingTimeout=0.1)
    def testUnhandledApiWhenNotIgnoreUnhandled(self):
        self._logger.warn("testUnhandledApiWhenNotIgnoreUnhandled")
        ns = "Test.YouView"
        self.api = MyApi4("test", ns=ns, ignoreUnhandled=True, maxAsync=1)
        tNs = ns + ".myapi4.voo"
        tNs = tNs.lower()
        _tId = itertools.count(0)
        tId = (123, _tId.next())
        d = ApiTransportItem(tNs, [], {}, True)
        self.api._ignoreUnhandled = False
        try:
            self.api.transportDataReceive(tId, d)
        except UnsupportedApiError, _e:
            assert True
        else:
            assert False
    def testUnhandledApiWhenIgnoreUnhandled(self):
        self._logger.warn("testUnhandledApiWhenIgnoreUnhandled")
        ns = "Test.YouView"
        self.api = MyApi4("test", ns=ns, ignoreUnhandled=True, maxAsync=1)
        tNs = ns + ".myapi4.voo"
        tNs = tNs.lower()
        _tId = itertools.count(0)
        tId = (123, _tId.next())
        d = ApiTransportItem(tNs, [], {}, True)
        self.api._ignoreUnhandled = True
        try:
            self.api.transportDataReceive(tId, d)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False

class UnsupportedApiParent(object):
    def _findHandler(self, ns):
        raise UnsupportedApiError("me", ns)

class SupportedApiParent(object):
    def _findHandler(self, ns):
        return self.handler
    def handler(self, *args, **kwargs):
        pass

class MyApi3(MyApi):
    def __init__(self, *args, **kwargs):
        super(MyApi3, self).__init__(*args, **kwargs)
        self.handled = {}
        self.handledLock = Semaphore(0)
        self._parent = SupportedApiParent()

class MyApi4(MyApi3):
    def __init__(self, *args, **kwargs):
        super(MyApi4, self).__init__(*args, **kwargs)
        self._parent = UnsupportedApiParent()

if __name__ == '__main__':
    unittest.main()
