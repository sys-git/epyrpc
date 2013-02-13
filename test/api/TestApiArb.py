
from epyrpc.api.ApiTransportItem import ApiTransportItem
from epyrpc.api.ApiTransportResponse import ApiTransportResponse
from epyrpc.api.UnsupportedApiError import UnsupportedApiError
from epyrpc.api.eo_v1.impl.ApiBase import ApiBase
from epyrpc.core.TransportFactory import TransportFactory
from epyrpc.core.arbitor.ApiArb import ApiArb
from epyrpc.core.arbitor.MultipleApiResponseError import MultipleApiResponseError
from epyrpc.core.eHeadType import eHeadType
from epyrpc.core.transaction.TransactionManager import TransactionManager
from epyrpc.core.transport.IpcTransportFactory import IpcTransportDetailsFactory
from epyrpc.core.transport.eIpcTransportState import eIpcTransportState
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener
from epyrpc.synchronisation.generators.HeadTransactionIdGenerator import \
    HeadTransactionIdGenerator
from epyrpc.synchronisation.generators.NeckTransactionIdGenerator import \
    NeckTransactionIdGenerator
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
from random import Random
from threading import Semaphore
import inspect
import threading
import unittest

class _baseApi(ApiBase):
    def _setup(self, **kwargs):
        pass
    def __init__(self, name, ns="something", solicited=False, ipc=None, ignoreUnhandled=False, maxAsync=1):
        super(_baseApi, self).__init__(name, ns=ns, solicited=solicited, ignoreUnhandled=ignoreUnhandled, maxAsync=maxAsync)
        if ipc != None:
            self.ipc = ipc
        self._handler = {"aaa":[]}
    def _handler_aaa(self, tId, bSynchronous, expectedResponse=None):
        self._logger.debug("_handler_aaa: expectedResponse: %(K)s." % {"K":expectedResponse})
        def respond(expectedResponse):
            self._handler["aaa"].append(expectedResponse)
            if isinstance(expectedResponse, Exception):
                raise expectedResponse
            return expectedResponse
        return self._handleStandardCall(tId, bSynchronous, lambda(x): respond(x), expectedResponse)

class Api2(_baseApi):
    def __init__(self, ns="something", solicited=False, ipc=None, ignoreUnhandled=False, maxAsync=1):
        super(Api2, self).__init__("Neck_2", ns=ns, solicited=solicited, ipc=ipc, ignoreUnhandled=ignoreUnhandled, maxAsync=maxAsync)
        self._handler["bbb"] = []
    def _handler_bbb(self, tId, bSynchronous, expectedResponse=None):
        self._logger.debug("_handler_bbb: expectedResponse: %(K)s." % {"K":expectedResponse})
        def respond(expectedResponse):
            self._handler["bbb"].append(expectedResponse)
            if isinstance(expectedResponse, Exception):
                raise expectedResponse
            return expectedResponse
        return self._handleStandardCall(tId, bSynchronous, lambda(x): respond(x), expectedResponse)

class Api1(_baseApi):
    def __init__(self, ns="something", solicited=False, ipc=None, ignoreUnhandled=False, maxAsync=1):
        super(Api1, self).__init__("Neck_1", ns=ns, solicited=solicited, ipc=ipc, ignoreUnhandled=ignoreUnhandled, maxAsync=maxAsync)
        self._handler["ccc"] = []
    def _handler_ccc(self, tId, bSynchronous, expectedResponse=None):
        self._logger.debug("_handler_ccc: expectedResponse: %(K)s." % {"K":expectedResponse})
        def respond(expectedResponse):
            self._handler["ccc"].append(expectedResponse)
            if isinstance(expectedResponse, Exception):
                raise expectedResponse
            return expectedResponse
        return self._handleStandardCall(tId, bSynchronous, lambda(x): respond(x), expectedResponse)

class IpcListener(iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    def __init__(self, logger):
        self._logger = logger
        self._tdr = []
        self._tsc = []
    def transportStateChange(self, e_ipc_transport_state):
        r"""
        @summary: IPC callback - The status of the IPC transport has changed
        """
        self._logger.info("transportStateChange: %s" \
            % eIpcTransportState.enumerateAttributes(e_ipc_transport_state))
        self._tsc.append(e_ipc_transport_state)
    def transportDataReceive(self, tId, data):
        """
        @summary: IPC callback - Data is received which \
            self._api does NOT handle
        """
        self._logger.info("transportDataReceive: Unhandled "
            "API data for tId: %s - %s" % (tId, data))
        self._tdr.append((tId, data))

class TestIpcArbitor(unittest.TestCase):
    HAMMER_TIME = 10
    def _whoami(self):
        return inspect.stack()[1][3]
    def setUp(self):
        ApiArb._wrappedNames = []
        self._apis = []
        ConfigurationManager().destroySingleton()
        IpcTransportDetailsFactory.reset()
        self._config = ConfigurationManager(cwd="config/ipc_arb").getConfiguration("masterLauncher").configuration.Configurations
        self._neckTransactionManager = TransactionManager(NeckTransactionIdGenerator())
        self._headTransactionManager = TransactionManager(HeadTransactionIdGenerator())
        self._ipcDetailsNeck = IpcTransportDetailsFactory.get(self._config.api.ipc, eHeadType.NECK)
        self._ipcDetailsHead = self._ipcDetailsNeck.invert()
    def tearDown(self):
        try:    self._details.del_qRx()
        except: pass
        try:    self._details.del_qTx()
        except: pass
        try:    self._ipcNeck.close(ignoreErrors=True)
        except: pass
        try:    self._ipcHead.close(ignoreErrors=True)
        except: pass
        try:
            #    Kill the apis asynchronously because it is time-consuming per api.
            sems = []
            for api in self._apis:
                sem = Semaphore(0)
                sems.append(sem)
                def doTeardown(_api, _sem):
                    _api.teardown()
                    _sem.release()
                try:    threading.Timer(0, doTeardown, args=[api, sem]).start()
                except: pass
            for sem in sems:
                sem.acquire()
        except: pass
    def _resetHandlers(self, methodNames):
        #    Reset handlers:
        if not isinstance(methodNames, list):
            methodNames = [methodNames]
        for api in self._apis:
            for methodName in methodNames:
                try:    api._handler[methodName] = []
                except: pass
    def testCreation(self):
        class DummyIpc(object):
            def setTransportStateChangeListener(self, listener): pass
            def setTransportDataReceiveListener(self, listener): pass
        self._logger = LogManager().getLogger(self._whoami())
        self._ipcListener = IpcListener(self._logger)
        #    Create the ipc:
        self._ipcNeck = TransportFactory.get(eHeadType.NECK,
                                        self._ipcDetailsNeck,
                                        self._neckTransactionManager,
                                        logger=self._logger,
                                        i_ipc_transport_state_change_listener=self._ipcListener,
                                        i_ipc_transport_data_receive_listener=self._ipcListener)
        api = self._ipcNeck
        assert api
        assert len(ApiArb._wrappedNames) == 11
        assert len(ApiArb._nonWrappedNames) == 2
        return api
    def testWrappedNames(self):
        api = self.testCreation()
        for i in ApiArb._nonWrappedNames:
            c = getattr(api, i)
            try:
                c()
            except TypeError, _e:
                assert True
    def testMultipleApisKnownMethodHammer(self):
        self.testMultipleApisKnownMethod(maxIter=self.HAMMER_TIME)
    def testMultipleApisKnownMethod(self, maxIter=1):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        self._apis.append(Api1(ns="two", ipc=self._ipcNeck))
        api1 = self._apis[0]
        api2 = self._apis[1]
        timeout = None
        expectResponse = True
        expectedResponse = {1:234, 5:678}
        count = 0
        def work(_ns, eCount1, eCount2, toCheck):
            #    Perform the transaction:
            result = self._sendTestData(timeout, expectResponse, _ns, expectedResponse=expectedResponse)
            #    Check the result:
            assert result == expectedResponse
            #    Check that the correct api received the command:
            assert len(api2._handler["aaa"]) == eCount2
            assert len(api1._handler["aaa"]) == eCount1
            assert toCheck._handler["aaa"][0] == expectedResponse
        while count < maxIter:
            self._logger.debug("iter: %(C)s" % {"C":count})
            self._resetHandlers("aaa")
            #    Test known method on api1:
            methodName = "aaa"
            ns = "".join([api1._getNamespacePrefix(), methodName])
            work(ns, 1, 0, api1)
            self._resetHandlers("aaa")
            #    Test known method on api2:
            methodName = "aaa"
            ns = "".join([api2._getNamespacePrefix(), methodName])
            work(ns, 0, 1, api2)
            count += 1
    def testMultipleApiUnknownMethodHammer(self):
        self.testMultipleApiUnknownMethod(maxIter=self.HAMMER_TIME)
    def testMultipleApiUnknownMethod(self, maxIter=1):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        self._apis.append(Api1(ns="two", ipc=self._ipcNeck))
        api1 = self._apis[0]
        api2 = self._apis[1]
        timeout = None
        expectResponse = True
        count = 0
        def work(_ns):
            #    Perform the transaction:
            try:
                self._sendTestData(timeout, expectResponse, _ns)
            except UnsupportedApiError, e:
                assert e.who() == "various:2"
                assert e.ns() == _ns
            else:
                assert False
            #    Check that no apis received the command:
            assert len(api1._handler["aaa"]) == 0
            assert len(api2._handler["aaa"]) == 0
        while count < maxIter:
            self._logger.debug("iter: %(C)s" % {"C":count})
            self._resetHandlers("aaa")
            #    Test unknown method on api1:
            methodName = "unknownMethod"
            ns = "".join([api1._getNamespacePrefix(), methodName])
            work(ns)
            #    Test unknown method on api21:
            methodName = "unknownMethod"
            ns = "".join([api2._getNamespacePrefix(), methodName])
            work(ns)
            count += 1
    def testSingleApiKnownMethod(self):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        api1 = self._apis[0]
        timeout = None
        expectResponse = True
        expectedResponse = {1:234, 5:678}
        #    Test known method:
        methodName = "aaa"
        ns = "".join([api1._getNamespacePrefix(), methodName])
        #    Perform the transaction:
        result = self._sendTestData(timeout, expectResponse, ns, expectedResponse=expectedResponse)
        #    Check the result:
        assert result == expectedResponse
    def testSingleApiUnknownMethod(self):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        api1 = self._apis[0]
        timeout = None
        expectResponse = True
        #    Test unknown method:
        methodName = "unknownMethod"
        ns = "".join([api1._getNamespacePrefix(), methodName])
        #    Perform the transaction:
        try:
            self._sendTestData(timeout, expectResponse, ns)
        except UnsupportedApiError, e:
            assert e.who() == "various:1"
            assert e.ns() == ns
        else:
            assert False
    def _createIpcs(self, connectHead=True, connectNeck=True):
        #    Create the Neck ipc:
        ipcListenerNeck = IpcListener(LogManager().getLogger("ipcListenerNECK"))
        ipcNeck = TransportFactory.get(eHeadType.NECK,
                                        self._ipcDetailsNeck,
                                        self._neckTransactionManager,
                                        logger=LogManager().getLogger("NECK"),
                                        i_ipc_transport_state_change_listener=ipcListenerNeck,
                                        i_ipc_transport_data_receive_listener=ipcListenerNeck)
        #    Connect to the Neck ipc:
        if connectNeck:
            ipcNeck.connect()
        #    Create the Head ipc:
        ipcListenerHead = IpcListener(LogManager().getLogger("ipcListenerHEAD"))
        ipcHead = TransportFactory.get(eHeadType.HEAD,
                                        self._ipcDetailsHead,
                                        self._headTransactionManager,
                                        logger=LogManager().getLogger("HEAD"),
                                        i_ipc_transport_state_change_listener=ipcListenerHead,
                                        i_ipc_transport_data_receive_listener=ipcListenerHead)
        #    Connect to the Head ipc:
        if connectHead:
            ipcHead.connect()
        return ((ipcListenerNeck, ipcNeck), (ipcListenerHead, ipcHead))
    def _sendTestData(self, timeout, expectResponse, ns, *args, **kwargs):
        #   Send data to the apis via the ipc:
        data = ApiTransportItem(ns, args, kwargs, synchronous=True)
        tId = self._ipcHead.sendData(data, solicited=expectResponse)
        if expectResponse:
            #    Wait for the response from the other side:
            result = self._headTransactionManager.acquireNew(tId, timeout=timeout, purge=True)
            #    Decode the response:
            result = ApiTransportResponse.decode(result)
            if isinstance(result, Exception):
                raise result
            else:
                return result
    def testMultipleApisMethodMixtureHammer(self):
        self.testMultipleApisSameMethodName(maxIter=self.HAMMER_TIME)
    def testMultipleApisSameMethodName(self, maxIter=1):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis (different this time, but with the same method name):
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        self._apis.append(Api2(ns="one", ipc=self._ipcNeck))
        api1 = self._apis[0]
        api2 = self._apis[1]
        timeout = None
        expectResponse = True
        expectedResponse = {1:234, 5:678}
        count = 0
        def work(_ns, eCounts, eResponses):
            #    Perform the transaction:
            result = self._sendTestData(timeout, expectResponse, _ns, expectedResponse=expectedResponse)
            #    Check the result:
            assert result == expectedResponse
            #    Check that the correct api received the command:
            for apiIndex, (eCount, methodName) in eCounts.items():
                assert len(self._apis[apiIndex]._handler[methodName]) == eCount
            for apiIndex, (eCount, methodName, eResponse) in eResponses.items():
                assert self._apis[apiIndex]._handler["aaa"][0] == eResponse
        while count < maxIter:
            self._logger.debug("iter: %(C)s" % {"C":count})
            self._resetHandlers("aaa")
            #    Test known method on api1:
            methodName = "aaa"
            ns = "".join([api1._getNamespacePrefix(), methodName])
            work(ns, {0:(1, "aaa"), 1:(0, "aaa")}, {0:(0, "aaa", expectedResponse)})
            self._resetHandlers("aaa")
            #    Test known method on api2:
            methodName = "aaa"
            ns = "".join([api2._getNamespacePrefix(), methodName])
            work(ns, {0:(0, "aaa"), 1:(1, "aaa")}, {1:(0, "aaa", expectedResponse)})
            count += 1
    def testMultipleApisMethodMixturesIterHammer(self, numApi1s=1, numApi2s=1, logger=None):
        self.testMultipleApisMethodMixtures(maxIter=self.HAMMER_TIME, numApi1s=numApi1s, numApi2s=numApi2s, logger=logger)
    def testMultipleApisMethodMixturesApi1Hammer(self, numApi1s=10, numApi2s=1, logger=None):
        self.testMultipleApisMethodMixtures(maxIter=self.HAMMER_TIME, numApi1s=numApi1s, numApi2s=numApi2s, logger=logger)
    def testMultipleApisMethodMixturesApi2Hammer(self, numApi1s=0, numApi2s=10, logger=None):
        self.testMultipleApisMethodMixtures(maxIter=self.HAMMER_TIME, numApi1s=numApi1s, numApi2s=numApi2s, logger=logger)
    def testMultipleApisMethodMixturesApi1And2Hammer(self, numApi1s=10, numApi2s=10, logger=None):
        self.testMultipleApisMethodMixtures(maxIter=self.HAMMER_TIME, numApi1s=numApi1s, numApi2s=numApi2s, logger=logger)
    def testMultipleApisMethodMixtures(self, maxIter=1, numApi1s=1, numApi2s=1, logger=None):
        if not logger:
            logger = LogManager().getLogger("%(W)s_%(I)s_api1_%(O)s_api2_%(T)s" % {"O":numApi1s, "T":numApi2s, "I":maxIter, "W":self._whoami()})
        self._logger = logger
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        api1s = []
        api2s = []
        #    Create the apis1:
        for i in range(0, numApi1s):
            api = Api1(ns="%(I)s" % {"I":i}, ipc=self._ipcNeck)
            api1s.append(api)
            self._apis.append(api)
        #    Create the apis2:
        for i in range(0, numApi2s):
            api = Api2(ns="%(I)s" % {"I":i}, ipc=self._ipcNeck)
            api2s.append(api)
            self._apis.append(api)
        timeout = None
        expectResponse = True
        expectedResponse = {1:234, 5:678}
        allMethodNames = ["aaa", "bbb", "ccc", "ddd", "eee", "fff"]
        count = 0
        def workKnown(ns, api, methodName, eResponse):
            #    FYI - Only the given api should have processed the command.
            #    Perform the transaction:
            result = self._sendTestData(timeout, expectResponse, ns, expectedResponse=expectedResponse)
            #    Check the result:
            assert result == expectedResponse
            #    Check that the correct api received the command:
            for a in self._apis:
                if a == api:
                    #    We expect the command:
                    eCount = 1
                else:
                    #    We don't expect the command:
                    eCount = 0
                try:
                    assert len(a._handler[methodName]) == eCount
                except:
                    pass
        def workUnknown(ns, api, methodName, eCount):
            #    Perform the transaction:
            timeout = None
            try:
                self._sendTestData(timeout, True, ns)
            except UnsupportedApiError, e:
                assert e.ns() == ns
                assert e.who() == "various:%(E)s" % {"E":eCount}
            else:
                assert False
        while count < maxIter:
            self._logger.debug("iter: %(C)s" % {"C":count})
            #    Reset handlers:
            self._resetHandlers(allMethodNames)
            #    Test known method on api1s:
            methodNames = ["aaa", "ccc"]
            for api in api1s:
                for methodName in methodNames:
                    #    Create the eNamespace:
                    ns = "".join([api._getNamespacePrefix(), methodName])
                    workKnown(ns, api, methodName, expectedResponse)
                    #    Reset handlers:
                    self._resetHandlers(allMethodNames)
            #    Reset handlers:
            self._resetHandlers(allMethodNames)
            #    Test known method on api2s:
            methodNames = ["aaa", "bbb"]
            for api in api2s:
                for methodName in methodNames:
                    #    Create the eNamespace:
                    ns = "".join([api._getNamespacePrefix(), methodName])
                    workKnown(ns, api, methodName, expectedResponse)
                    #    Reset handlers:
                    self._resetHandlers(allMethodNames)
            #    Reset handlers:
            self._resetHandlers(allMethodNames)
            #    Test unknown method on api1s:
            methodNames = ["ddd", "eee", "fff"]
            eCount = len(api1s) + len(api2s)
            for api in api1s:
                for methodName in methodNames:
                    #    Create the eNamespace:
                    ns = "".join([api._getNamespacePrefix(), methodName])
                    workUnknown(ns, api, methodName, eCount)
                    #    Reset handlers:
                    self._resetHandlers(allMethodNames)
            #    Reset handlers:
            self._resetHandlers(allMethodNames)
            #    Test unknown method on api2s:
            methodNames = ["ddd", "eee", "fff"]
            for api in api2s:
                for methodName in methodNames:
                    #    Create the eNamespace:
                    ns = "".join([api._getNamespacePrefix(), methodName])
                    workUnknown(ns, api, methodName, eCount)
                    #    Reset handlers:
                    self._resetHandlers(allMethodNames)
            #    Reset handlers:
            self._resetHandlers(allMethodNames)
            count += 1
    def testDynamicApiRemoval(self):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis (x2) with identical namespaces:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        self._apis.append(Api2(ns="one", ipc=self._ipcNeck))
        api1 = self._apis[0]
        api2 = self._apis[1]
        allMethodNames = ["aaa", "bbb", "ccc", "ddd", "eee", "fff"]
        #    Check the positive case:
        methodName = "aaa"
        timeout = None
        expectResponse = "hello.world"
        ns = "".join([api1._getNamespacePrefix(), methodName])
        namespaceMethod1 = ns
        self._sendTestData(timeout, expectResponse, namespaceMethod1)
        self._resetHandlers(allMethodNames)

        ns = "".join([api2._getNamespacePrefix(), methodName])
        namespaceMethod2 = ns
        self._sendTestData(timeout, expectResponse, namespaceMethod2)
        self._resetHandlers(allMethodNames)

        #    teardown the first api:
        api1.teardown()
        #    and remove it from our cache:
        self._apis.remove(api1)
        eCount = len(self._apis)
        assert eCount == 1

        #    Send some test data to the remaining api:
        self._sendTestData(timeout, expectResponse, namespaceMethod2)
        self._resetHandlers(allMethodNames)
    
        #    Send some test data to the torn-down api:
        ns = namespaceMethod1
        try:
            self._sendTestData(timeout, expectResponse, ns)
        except UnsupportedApiError, e:
            assert e.ns() == ns
            assert e.who() == "various:%(E)s" % {"E":eCount}
        else:
            assert False
        self._resetHandlers(allMethodNames)
        
        #    teardown the second api:
        api2.teardown()
        #    and remove it from our cache:
        self._apis.remove(api2)
        eCount = len(self._apis)
        assert eCount == 0

        #    Send some test data to the apis:
        for ns in [namespaceMethod1, namespaceMethod2]:
            try:
                self._sendTestData(timeout, expectResponse, ns)
            except UnsupportedApiError, e:
                assert e.ns() == ns
                assert e.who() == "various:%(E)s" % {"E":eCount}
            else:
                assert False
            self._resetHandlers(allMethodNames)
    def testDynamicApiInsertion(self):
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis (x2) with identical namespaces:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        api1 = self._apis[0]
        allMethodNames = ["aaa", "bbb", "ccc", "ddd", "eee", "fff"]
        #    Check the positive case:
        methodName = "aaa"
        timeout = None
        expectResponse = "hello.world"
        ns = "".join([api1._getNamespacePrefix(), methodName])
        namespaceMethod1 = ns
        self._sendTestData(timeout, expectResponse, namespaceMethod1)
        self._resetHandlers(allMethodNames)

        #    Create the new api:
        self._apis.append(Api2(ns="one", ipc=self._ipcNeck))
        api2 = self._apis[1]
        #    Send it some data:
        ns = "".join([api2._getNamespacePrefix(), methodName])
        namespaceMethod2 = ns
        self._sendTestData(timeout, expectResponse, namespaceMethod2)
        self._resetHandlers(allMethodNames)
        #    Send the first api some data:
        self._sendTestData(timeout, expectResponse, namespaceMethod1)
        self._resetHandlers(allMethodNames)
        
        #    teardown the apis:
        api1.teardown()
        api2.teardown()
        #    and remove it from our cache:
        self._apis.remove(api1)
        self._apis.remove(api2)
        eCount = len(self._apis)
        assert eCount == 0

        #    Send some test data to the apis:
        for ns in [namespaceMethod1, namespaceMethod2]:
            try:
                self._sendTestData(timeout, expectResponse, ns)
            except UnsupportedApiError, e:
                assert e.ns() == ns
                assert e.who() == "various:%(E)s" % {"E":eCount}
            else:
                assert False
            self._resetHandlers(allMethodNames)
    def testApisWithOverlappingNamespaces(self):
        #    Test >1 api handling the same namespace (a given api call)
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        #    Create the apis (x2) with identical namespaces:
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        self._apis.append(Api1(ns="one", ipc=self._ipcNeck))
        api1 = self._apis[0]
        api2 = self._apis[1]
        assert api1._getNamespacePrefix() == api2._getNamespacePrefix()
        #    Test unknown method:
        methodName = "unknownMethod"
        timeout = None
        expectResponse = "hello.world"
        ns = "".join([api1._getNamespacePrefix(), methodName])
        eCount = len(self._apis)
        #    Check the negative case:
        try:
            self._sendTestData(timeout, expectResponse, ns)
        except UnsupportedApiError, e:
            assert e.who() == "various:%(E)s" % {"E":eCount}
            assert e.ns() == ns
        else:
            assert False
        #    Check the positive exception case:
        methodName = "ccc"
        timeout = None
        expectResponse = "hello.world"
        ns = "".join([api1._getNamespacePrefix(), methodName])
        #    Check the negative case:
        try:
            self._sendTestData(timeout, expectResponse, ns)
        except MultipleApiResponseError, e:
            assert e.ns() == ns
            assert e.count() == 2
            self._logger.debug(e)
        else:
            assert False
    def testDynamicApiInsertionAndRemovalHammer(self):
        self.testDynamicApiInsertionAndRemoval(maxIter=self.HAMMER_TIME)
    def testDynamicApiInsertionAndRemoval(self, numApis=10, maxIter=1):
        r"""
        for c in range(maxIter):
            for n in range(numApis):
                Insert(n) where n in random.range(Api1, Api2)
                send in range(n)
                if n%3==0:
                    Remove(m) where m in random.range(n-1)
                    send(M), expect Unhandled.
                    send in range(n)
        for m in range(n_remaining):
            Remove(m)
        """
        self._logger = LogManager().getLogger(self._whoami())
        ((self._ipcListenerNeck, self._ipcNeck), (self._ipcListenerHead, self._ipcHead)) = self._createIpcs()
        allMethodNames = ["aaa", "bbb", "ccc", "ddd", "eee", "fff"]
        if numApis < 10:
            numApis = 10
        if maxIter < 1:
            maxIter = 1
        namespaces = []
        methodName = "aaa"
        timeout = None
        expectResponse = "hello.world"
        self.random = Random()
        def checkAll():
            #    Send data to all the existing apis:
            for ns_ in namespaces:
                methodNamespace = "".join([ns_, methodName])
                self._sendTestData(timeout, expectResponse, methodNamespace)
        def removeAndCheck(api):
            #    Remove the namespace
            namespace = namespaces.pop(self._apis.index(api))
            #    teardown the apis:
            api.teardown()
            #    and remove it from our cache:
            self._apis.remove(api)
            eCount = len(self._apis)
            #    Try sending data to it:
            try:
                self._sendTestData(timeout, expectResponse, namespace)
            except UnsupportedApiError, e:
                assert e.ns() == namespace
                assert e.who() == "various:%(E)s" % {"E":eCount}
            else:
                assert False
            self._resetHandlers(allMethodNames)
        def removeOneCheckAll():
            l = len(self._apis)
            if l > 0:
                if l > 1:
                    #    Remove a random api:
                    removeMe = self.random.choice(self._apis[:-1])
                else:
                    #    Remove the remaining api:
                    removeMe = self._apis[0]
                removeAndCheck(removeMe)
                #    Send data to all the others:
                checkAll()
        for count in range(maxIter):
            for i in range(numApis):
                self._logger.debug("iteration: %(C)s of %(TI)s, api %(N)s of %(T)s" % {"N":(i + 1), "T":numApis, "C":(count + 1), "TI":maxIter})
                #    Create the new api:
                namespace = "one_%(I)s" % {"I":i}
                what = self.random.choice([Api1, Api2])
                api = what(ns=namespace, ipc=self._ipcNeck)
                namespaces.append(api._getNamespacePrefix())
                self._apis.append(api)
                #    Send data to it:
                ns = "".join([api._getNamespacePrefix(), methodName])
                self._sendTestData(timeout, expectResponse, ns)
                self._resetHandlers(allMethodNames)
                #    Send data to all the others:
                checkAll()
                if i % 3 == 0:
                    removeOneCheckAll()
            self._logger.debug("Removing remaining %(N)s apis:" % {"N":len(self._apis)})
            while len(self._apis) > 0:
                removeOneCheckAll()

if __name__ == '__main__':
    unittest.main()
