
from epyrpc.api.ApiAction import ApiAction
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.api.iApi import iApi
from epyrpc.api.iApiTransportResponse import iApiTransportResponse
from epyrpc.core.IpcExceptions import NoResponseRequired
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener
from epyrpc.utils.synchronisation.IpcTransportPartialResponse import \
    IpcTransportPartialResponse
from multiprocessing.synchronize import Semaphore
import unittest

def setup_module():
    r"""
    @TODO: Disable exception printing when running on Jenkins.
    """
    pass

class TestIApi(unittest.TestCase):
    class voo(iApi):
        pass
    def testSolicited(self):
        api = TestIApi.voo("parentNs")
        assert api.solicited == True
        api.solicited = False
        assert api.solicited == False
        api.solicited = True
        assert api.solicited == True
    def testNamespaceCreationString(self):
        api = TestIApi.voo("parentNs")
        print api._whoami()
    def testNamespaceCreationUnicode(self):
        api = TestIApi.voo(u"parentNs")
        print api._whoami()
    def testNamespaceCreationNone(self):
        try:
            TestIApi.voo(None)
        except Exception, _e:
            assert True
        else:
            assert False
    def testNamespaceCreationEmptyNs(self):
        api = TestIApi.voo("")
        assert api._namespace == "voo", "Got: %(NS)s" % {"NS":api._namespace}
    def testWhoami(self):
        api = TestIApi.voo("parentNs")
        assert api._whoami() == "testWhoami"
    def testCreateNamespaceValid(self):
        iApi._createNamespace("")
        iApi._createNamespace([""])
        iApi._createNamespace(["1", "2"])
    def testCreateNamespaceProduceslowercase(self):
        assert iApi._createNamespace("AbCdEf").islower()
        assert iApi._createNamespace(["ABCDEF"]).islower()
        assert iApi._createNamespace(["1aB", "2cD"]).islower()
    def testCreateNamespaceInvalid(self):
        iApi._createNamespace()
        iApi._createNamespace([])
        eErr = 1
        try:
            iApi._createNamespace([eErr])
        except ApiParamError, e:
            assert e.item == eErr
            assert basestring in e.allowedTypes
            assert list in e.allowedTypes
        try:
            iApi._createNamespace(eErr)
        except ApiParamError, e:
            assert e.item == eErr
            assert basestring in e.allowedTypes
            assert list in e.allowedTypes
    def testValidIpc(self):
        ipc = MyTransport()
        api = iApi()
        api.ipc = ipc
        assert api.ipc == ipc
    def testInvalidIpc(self):
        ipc = object()
        api = iApi()
        try:
            api.ipc = ipc
        except ApiParamError, e:
            assert e.item == ipc
            assert iIpcTransport in e.allowedTypes
            assert len(e.allowedTypes) == 1
    def testSetTransportDataReceiveListener(self):
        api = iApi()
        myListener = MyTransportListener()
        api.transportDataReceiveListener = myListener
        assert api.transportDataReceiveListener == myListener
    def testSetInvalidTransportDataReceiveListener(self):
        api = iApi()
        myListener = object()
        try:
            api.transportDataReceiveListener = myListener
        except ApiParamError, e:
            assert e.item == myListener
            assert iIpcTransportDataReceiveListener in e.allowedTypes
    def testSetTransportStateChangeListener(self):
        api = iApi()
        myListener = MyTransportListener()
        api.transportStateChangeListener = myListener
        assert api.transportStateChangeListener == myListener
    def testSetInvalidTransportStateChangeListener(self):
        api = iApi()
        myListener = object()
        try:
            api.transportStateChangeListener = myListener
        except ApiParamError, e:
            assert e.item == myListener
            assert iIpcTransportStateChangeListener in e.allowedTypes
    def testGetEventsToHandle(self, api=iApi()):
        api = iApi()
        events = api.getEventsToHandle()
        assert isinstance(events, list)
        assert len(events) == 0
    def testGetEventsToHandleOnSubclass(self):
        class voo(iApi):
            pass
        v = voo()
        self.testGetEventsToHandle(api=v)
        eA = u"a"
        eB = u"b"
        class boo(iApi):
            EVENT__A = eA
            EVENT_B = eB
        api = boo()
        events = api.getEventsToHandle()
        assert isinstance(events, list)
        assert len(events) == 1
        assert events[0] == eA
        eC = u"c"
        eD = u"d"
        class coo(boo):
            EVENT__C = eC
            EVENT_D = eD
        api = coo()
        events = api.getEventsToHandle()
        assert isinstance(events, list)
        assert len(events) == 2
        assert eA in events
        assert eC in events

class CustomException(Exception):
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        if isinstance(other, CustomException):
            return other.value == self.value

class MyResult(object):
    def __init__(self, data, index):
        self.data = data
        self.index = index

class TestReturnChunks(unittest.TestCase):
    def setUp(self):
        self.myIpc = MyTransport()
        self.args = (345, "hello", "world!")
        self.kwargs = {"i.am":"an.arg"}
        self.funcData = {}
    def testSingleChunk(self):
        self._checkNChunks(1)
    def testTwoChunks(self):
        self._checkNChunks(2)
    def testThreeChunks(self):
        self._checkNChunks(3)
    def testOneHundredChunks(self):
        self._checkNChunks(100)
    def _checkNChunks(self, count):
        api = iApi(ipc=self.myIpc)
        eResult = CustomException(123)
        def func(*args, **kwargs):
            self.funcData["args"] = args
            self.funcData["kwargs"] = kwargs
            raise eResult
        tId = 123
        chunks = []
        for i in range(1, count + 1):
            chunks.append([i for i in range(1, i + 1)])
        combinerMethod = ("hello", "world!")
        try:
            api._returnChunks(tId, chunks, combinerMethod, lambda x, index: MyResult(x[index], index))
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
        assert self.myIpc.dataSentLock.acquire(timeout=1)
        assert len(self.myIpc.dataSent) == count
        for ii in range(0, count):
#            print "Checking: ", ii
            r = self.myIpc.dataSent[ii]
            (_tId_, result) = r
            assert tId == tId
            assert isinstance(result, IpcTransportPartialResponse)
            assert result.tId() == tId
            assert result.index() == ii
            assert result.numChunks() == count
            response = result.response().data
            assert result.response().index == ii
            assert isinstance(response, list)
            assert response == chunks[ii]

class TestHandleStandardCall(unittest.TestCase):
    def setUp(self):
        self.myIpc = MyTransport()
        self.args = (345, "hello", "world!")
        self.kwargs = {"i.am":"an.arg"}
        self.funcData = {}
    def testSyncFuncRaisesNoResponseRequired(self):
        api = iApi(ipc=self.myIpc)
        tId = 1
        def func(*args, **kwargs):
            raise NoResponseRequired(tId)
        sync = True
        try:
            api._handleStandardCall(tId, sync, func)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
    def testAsyncFuncRaisesCustomException(self):
        api = iApi(ipc=self.myIpc)
        eResult = CustomException(123)
        def func(*args, **kwargs):
            self.funcData["args"] = args
            self.funcData["kwargs"] = kwargs
            raise eResult
        tId = 1
        sync = False
        api._handleStandardCall(tId, sync, func, *self.args, **self.kwargs)
        assert self.myIpc.dataSentLock.acquire(timeout=1)
        assert len(self.myIpc.dataSent) == 1
        assert self.myIpc.dataSent[0][0] == tId
        d = self.myIpc.dataSent[0][1]
        assert isinstance(d, ApiTransportResponse)
        assert d.response() == eResult
        assert self.funcData["args"] == self.args
        assert self.funcData["kwargs"] == self.kwargs
    def testSyncFuncRaisesCustomException(self):
        api = iApi(ipc=self.myIpc)
        eResult = CustomException(123)
        def func(*args, **kwargs):
            self.funcData["args"] = args
            self.funcData["kwargs"] = kwargs
            raise eResult
        tId = 1
        sync = True
        try:
            api._handleStandardCall(tId, sync, func, *self.args, **self.kwargs)
        except CustomException, e:
            assert e == eResult
        assert self.funcData["args"] == self.args
        assert self.funcData["kwargs"] == self.kwargs
    def testSyncFuncReturnsCustomData(self):
        api = iApi(ipc=self.myIpc)
        eResult = 123
        def func(*args, **kwargs):
            self.funcData["args"] = args
            self.funcData["kwargs"] = kwargs
            return eResult
        tId = 1
        sync = True
        r = api._handleStandardCall(tId, sync, func, *self.args, **self.kwargs)
        assert isinstance(r, iApiTransportResponse)
        assert r.response() == eResult
        assert self.funcData["args"] == self.args
        assert self.funcData["kwargs"] == self.kwargs
    def testAsyncFuncReturnsCustomData(self):
        api = iApi(ipc=self.myIpc)
        eResult = 123
        def func(*args, **kwargs):
            self.funcData["args"] = args
            self.funcData["kwargs"] = kwargs
            return eResult
        tId = 1
        sync = False
        api._handleStandardCall(tId, sync, func, *self.args, **self.kwargs)
        assert self.myIpc.dataSentLock.acquire(timeout=1)
        assert len(self.myIpc.dataSent) == 1
        assert self.myIpc.dataSent[0][0] == tId
        d = self.myIpc.dataSent[0][1]
        assert isinstance(d, ApiTransportResponse)
        assert d.response() == eResult
        assert self.funcData["args"] == self.args
        assert self.funcData["kwargs"] == self.kwargs

class TestSetHandlersBasic(unittest.TestCase):
    def testSetInvalidHandler(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        def myHandler(): pass
        try:
            api.setHandler(None, myHandler)
        except ApiParamError, e:
            assert e.item == None
            assert basestring in e.allowedTypes
            assert len(e.allowedTypes) == 1
    def testSetHandlerIsNone(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = "namespace"
        def myHandler(): pass
        api.setHandler(NS, myHandler)
        assert NS in api._apiHandlers
        assert len(api._apiHandlers) == 1
        api.setHandler(NS, None)
        assert NS not in api._apiHandlers
        assert len(api._apiHandlers) == 0
    def testSetHandler(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = "namespace"
        def myHandler(): pass
        api.setHandler(NS, myHandler)
        assert NS in api._apiHandlers
        assert len(api._apiHandlers) == 1

class TestSetHandlersAdvanced(unittest.TestCase):
    class MyApi(iApi):
        class A(iApi):
            class B(iApi):
                def __init__(self, ns="", solicited=True, ipc=None):
                    super(TestSetHandlersAdvanced.MyApi.A.B, self).__init__(ns=ns, solicited=solicited)
                def c(self):
                    return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited)
            def __init__(self, ns="", solicited=True, ipc=None):
                super(TestSetHandlersAdvanced.MyApi.A, self).__init__(ns=ns, solicited=solicited)
                self._setup()
            def _setup(self):
                self.b = TestSetHandlersAdvanced.MyApi.A.B(ns=self._getNamespace(), solicited=self.solicited)
                self._apis.append(self.b)
        def __init__(self, ns="", solicited=True, ipc=None):
            super(TestSetHandlersAdvanced.MyApi, self).__init__(ns=ns, solicited=solicited)
            self._setup()
        def _setup(self):
            self.a = TestSetHandlersAdvanced.MyApi.A(ns=self._getNamespace(), solicited=self.solicited)
            self._apis.append(self.a)
    def setUp(self):
        self.ns = "helloworld"
    def testSetHandler1(self):
        api = TestSetHandlersAdvanced.MyApi(ns=self.ns)
        assert len(api._apiHandlers) == 0
        NS = "a.b.c"
        def myHandler(): pass
        theApi = api
        theApi.setHandler(NS, myHandler)
        assert NS in theApi._apiHandlers
        assert len(theApi._apiHandlers) == 1
    def testSetHandler2(self):
        api = TestSetHandlersAdvanced.MyApi(ns=self.ns)
        assert len(api._apiHandlers) == 0
        NS = "b.c"
        def myHandler(): pass
        theApi = api.a
        theApi.setHandler(NS, myHandler)
        assert NS in theApi._apiHandlers
        assert len(theApi._apiHandlers) == 1
    def testSetHandler3(self):
        api = TestSetHandlersAdvanced.MyApi(ns=self.ns)
        assert len(api._apiHandlers) == 0
        NS = "c"
        def myHandler(): pass
        theApi = api.a.b
        theApi.setHandler(NS, myHandler)
        assert NS in theApi._apiHandlers
        assert len(theApi._apiHandlers) == 1

class TestGetHandlers(unittest.TestCase):
    def testGetHandlerNsIsNone(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = None
        def myHandler(): pass
        try:
            api.getHandler(NS)
        except ApiParamError, e:
            assert e.item == NS
            assert basestring in e.allowedTypes
            assert len(e.allowedTypes) == 1
    def testGetHandlerWhenNoneSet(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = "namespace"
        try:
            api.getHandler(NS)
        except UnsupportedApiError, e:
            assert e.ns() == NS
    def testGethandler(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = "namespace"
        def myHandler(): pass
        api.setHandler(NS, myHandler)
        assert len(api._apiHandlers) == 1
        handler = api.getHandler(NS)
        assert handler == myHandler
    def testGetCatchallHandlerAsFallback(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = iApi.CATCHALL
        def myHandler(): pass
        api.setHandler(NS, myHandler)
        assert len(api._apiHandlers) == 1
        dNS = "some.namespace"
        handler = api.getHandler(dNS)
        assert handler == myHandler
    def testGetHandlerWithCatchallHandlerAsFallback(self):
        api = iApi()
        assert len(api._apiHandlers) == 0
        NS = iApi.CATCHALL
        def myHandler(): pass
        def myOtherHandler(): pass
        api.setHandler(NS, myHandler)
        assert len(api._apiHandlers) == 1
        eNS = "hello.world!"
        api.setHandler(eNS, myOtherHandler)
        assert len(api._apiHandlers) == 2
        handler = api.getHandler(eNS)
        assert handler == myOtherHandler
class MyTransportListener(iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener):
    def transportStateChange(self, e_ipc_transport_state):
        pass
    def transportDataReceive(self, tId, synchronous, data):
        pass
class MyTransport(iIpcTransport):
    def __init__(self, *args, **kwargs):
        self.dataSent = []
        self.dataSentLock = Semaphore(0)
    def sendData(self, result, transactionId):
        self.dataSent.append((transactionId, result))
        self.dataSentLock.release()

class myApi(iApi):
    def _handler_iAmAHandler1(self): pass
    def _handler_iAmAHandler2(self): pass
    def _handler_iAmAHandler3(self): pass
    def __handler_iAmAHandler4(self): pass
    def handler_iAmAHandler5(self): pass

class TestHandlerRegistration(unittest.TestCase):
    def testRegisterDirectly(self):
        a = myApi()
        assert len(a._apiHandlers) == 0
        a._registerHandlers()
        assert len(a._apiHandlers) == 3
    def testFromNewIpc(self):
        a = myApi()
        assert len(a._apiHandlers) == 0
        a._newIpc()
        assert len(a._apiHandlers) == 3

class TestHandleStandardCheck(unittest.TestCase):
    def setUp(self):
        self.myIpc = MyTransport()
        self.args = (345, "hello", "world!")
        self.kwargs = {"i.am":"an.arg"}
        self.funcData = {}
        self.myApi = iApi(ipc=self.myIpc)
    def _checker(self, eResult):
        if isinstance(eResult, Exception):
            raise eResult
        return eResult
    def testSyncCheckRaisesException(self):
        tId = 123
        bSync = True
        eResult = ApiParamError(None)
        try:
            self.myApi._handleStandardCheck(tId, bSync, self._checker, eResult)
        except ApiParamError, _e:
            assert True
        else:
            assert False
    def testAsyncCheckSendsException(self):
        tId = 123
        bSync = False
        eResult = ApiParamError(None)
        try:
            self.myApi._handleStandardCheck(tId, bSync, self._checker, eResult)
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
        assert self.myIpc.dataSentLock.acquire(timeout=2)
        assert self.myIpc.dataSent[0][0] == tId
        result = self.myIpc.dataSent[0][1]
        assert isinstance(result, iApiTransportResponse)
        assert isinstance(result.response(), ApiParamError)
    def testSyncCheckReturnsResult(self):
        tId = 123
        bSync = True
        eResult = 456
        assert self.myApi._handleStandardCheck(tId, bSync, self._checker, eResult) == eResult
    def testAsyncCheckSendsResult(self):
        tId = 123
        bSync = False
        eResult = 456
        result = self.myApi._handleStandardCheck(tId, bSync, self._checker, eResult)
        assert result == eResult

if __name__ == '__main__':
    unittest.main()
