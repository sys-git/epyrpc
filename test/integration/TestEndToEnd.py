from epyrpc.api.ApiFactory import ApiFactory
from epyrpc.api.eApiType import eApiType
from epyrpc.api.eSync import eSync
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.enums.eSignalFilterResponse import eSignalFilterResponse
from epyrpc.api.eo_v1.impl.common.tas.signalFilter.FilterId import FilterId
from epyrpc.api.eo_v1.impl.common.tas.signalFilter.Namespace import Namespace
from epyrpc.api.eo_v1.impl.common.tas.signalFilter.UnknownSignalFilter import \
    UnknownSignalFilter
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterId import \
    iFilterId
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterIdentifier import \
    iFilterIdentifier
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iNamespace import \
    iNamespace
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iSignalFilterStatus import \
    iSignalFilterStatus
from epyrpc.api.eo_v1.interfaces.head.tas.iTas import iTas
from epyrpc.core.transaction.TransactionManager import TransactionManager
from epyrpc.core.transport.details.QueueTransportDetails import \
    QueueTransportDetails
from epyrpc.core.transport.eIpcTransportState import eIpcTransportState
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportStateChangeListener
from epyrpc.core.transport.queue.QueueTransporter import QueueTransporter
from epyrpc.head.HeadQueueTransporter import HeadQueueTransporter
from epyrpc.synchronisation.generators.HeadTransactionIdGenerator import \
    HeadTransactionIdGenerator
from epyrpc.synchronisation.generators.NeckTransactionIdGenerator import \
    NeckTransactionIdGenerator
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
from multiprocessing.synchronize import Semaphore
import os
import sys
import unittest

#    Increase this value to allow for debugging.
SYNC_API_TIMEOUT = 1
r"""
When debugging, set the 'SYNC_API_TIMEOUT_FOR_DEBUGGING_ONLY' to whatever you want,
just put it back equal to 'SYNC_API_TIMEOUT' when done.
"""
SYNC_API_TIMEOUT_FOR_DEBUGGING_ONLY = SYNC_API_TIMEOUT

class Head(iIpcTransportStateChangeListener):
    def __init__(self, qTransport):
        self.signal = []
        self.signalReceived = Semaphore(0)
        self.tm = TransactionManager(HeadTransactionIdGenerator())
        self.logger = LogManager().getLogger(self.__class__.__name__)
        self.ipc = HeadQueueTransporter(qTransport, self.tm, self, logger=self.logger)
        self.api = ApiFactory.get(eApiType.EO_V1, ns="MyWay", solicited=True, ipc=self.ipc)
        #    Now register our listeners:
        self.api.tas.setHandler(iTas.EVENT__SIGNAL, self._signalHandler)
        self.ipc.connect()
    def teardown(self):
        try:    self.api.teardown()
        except: pass
        try:    self.ipc.close(ignoreErrors=True)
        except: pass
    def _signalHandler(self, *args, **kwargs):
        self.logger.debug("Signal received...args(%(A)s), kwargs(%(K)s)." % {"A":args, "K":kwargs})
        self.signal.append((args, kwargs))
        self.signalReceived.release()

class Neck(iIpcTransportStateChangeListener):
    def __init__(self, qTransport):
        self.stateChange = []
        self.tm = TransactionManager(NeckTransactionIdGenerator())
        self.logger = LogManager().getLogger(self.__class__.__name__)
        self.ipc = QueueTransporter(qTransport, self.tm, self, logger=self.logger)
        self.api = ApiFactory.get(eApiType.EO_V1__HANDLER, ns="MyWay", solicited=False, ipc=self.ipc)
        self.ipc.connect()
        #    Now register for SEH signals:
        self.seh = SignalExchangeHub()
        self.seh.addListener(FatalError.createListener(self._onSignal))
    def teardown(self):
        try:    self.api.teardown()
        except: pass
        try:    self.ipc.close(ignoreErrors=True)
        except: pass
    def transportStateChange(self, e_ipc_transport_state):
        self.stateChange.append(e_ipc_transport_state)
        self.logger.warn("Transport state: %(S)s" % {"S":eIpcTransportState.enumerateAttributes(e_ipc_transport_state)})
    def _onSignal(self, namespace, signal):
        #    Now call the api:
        self.logger.debug("Sending Signal over api...ns(%(A)s), signal(%(K)s)." % {"A":namespace, "K":signal})
        signalCount = 1
        filterId = None
        status = None
        api = self.api.tas.signal(signalCount, filterId, namespace, signal, status)
        #    Unsolicited's are fire-and-forget, hence no return value:
        api.sync = eSync.ASYNCHRONOUS
        api.solicited = False
        try:
            api()  # FIXME: wtf? this is lame.. Replace me
        except Exception: pass
        self.logger.debug("Sent Signal over api...ns(%(A)s), signal(%(K)s)." % {"A":namespace, "K":signal})

class TestSignalPropagation(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        print os.getcwd()
        path = os.path.realpath("config/ipc")
        ConfigurationManager(cwd=path)
        self.qTransport = QueueTransportDetails()
        self.head = Head(self.qTransport)
        self.neck = Neck(self.qTransport.invert())
    def tearDown(self):
        self.head.teardown()
        self.neck.teardown()
        try:    self.qTransport.del_qRx()
        except: pass
        try:    self.qTransport.del_qTx()
        except: pass
        SignalExchangeHub.destroySingleton()
    def tXXXest(self):
        #    Using the SignalExchangeHub, send an unsolicited Signal to the Head.
        self.neck.seh.propagateSignal(FatalError("i.am.a.fatal.error"))
        assert self.head.signalReceived.acquire(timeout=SYNC_API_TIMEOUT)
        assert len(self.head.signal) == 1

class MySignal(ISignal):
    def getNamespace(self):
        return self.ns
    def setNamespace(self, namespace):
        self.ns = namespace
    def getPayload(self):
        return ""
    def getPayloadType(self):
        return str

class TestSignalFilter(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        self._logger = LogManager().getLogger(self.__class__.__name__)
        print os.getcwd()
        path = os.path.realpath("config/ipc")
        ConfigurationManager.destroySingleton()
        ConfigurationManager(cwd=path)
        self.qTransport = QueueTransportDetails()
        self.head = Head(self.qTransport)
        self.neck = Neck(self.qTransport.invert())
        self.SignalExchangeHub = SignalExchangeHub()
        self._eo = ExecutionOrganiser()
        self._eo.bindInterface()
        sf = self._eo._signalFilters
        sf.init(self.SignalExchangeHub)
        sf.globalEnable(SignalFilters.DEFAULT__GLOBAL_ENABLE)
        sf.globalMute(SignalFilters.DEFAULT__GLOBAL_MUTE)
        sf._api = self.neck.api.tas.signal
    def tearDown(self):
        self.head.teardown()
        self.neck.teardown()
        try:    self.qTransport.del_qRx()
        except: pass
        try:    self.qTransport.del_qTx()
        except: pass
        ExecutionOrganiser()._signalFilters.globalEnable(SignalFilters.DEFAULT__GLOBAL_ENABLE)
        ExecutionOrganiser()._signalFilters.globalMute(SignalFilters.DEFAULT__GLOBAL_MUTE)
        ExecutionOrganiser()._signalFilters._filters = {}
        ExecutionOrganiser()._stageController._STAGES_TIMEOUT = 2
        ExecutionOrganiser.destroySingleton()
        SignalExchangeHub.destroySingleton()
    def testStatus(self, eE=SignalFilters.DEFAULT__GLOBAL_ENABLE, eM=SignalFilters.DEFAULT__GLOBAL_MUTE, count=0):
        api = self.head.api.tas.signalFilter.status()
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == eE
        assert result.globalMute() == eM
        return count
    def testGlobalEnable(self, count=0):
        eE = eGlobalEnable.ON
        api = self.head.api.tas.signalFilter.globalEnable(eE)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == eE
        assert result.globalMute() == SignalFilters.DEFAULT__GLOBAL_MUTE
        self.testStatus(eE, result.globalMute())
        return count
    def testMuteAll(self, count=0):
        eM = eMute.ON
        api = self.head.api.tas.signalFilter.muteAll(eM)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == SignalFilters.DEFAULT__GLOBAL_ENABLE
        assert result.globalMute() == eM
        self.testStatus(result.globalEnable(), eM)
        return count
    def testAddSingleNamespace(self, count=0):
        self.testStatus()
        ns = Namespace("a.ns.to.capture")
        nId = ns.id_()
        api = self.head.api.tas.signalFilter.add(ns)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result[0], dict)
        assert isinstance(result[1], iSignalFilterStatus)
        sfs = result[0]
        assert len(sfs.keys()) == 1
        assert nId in sfs.keys()
        assert isinstance(sfs[nId], iASignalFilter)
        assert sfs[nId].namespace().compare(ns)
        count = self._doSignalInjection([(ns.namespace(), eMute.OFF)], count=count, enableFilters=True, unmuteAll=True)
        count = self._doSignalInjection([(ns.namespace(), eMute.ON)], count=count, enableFilters=False, unmuteAll=True)
        return (ns, sfs[nId].fId(), count)
    def _doSignalInjection(self, ns, count=0, enableFilters=False, unmuteAll=False):
        api = self.head.api.tas.signalFilter.status()
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        originalStatus = api()
        assert isinstance(originalStatus, iSignalFilterStatus)
        #    Now fire a signal into the Neck which is guaranteed to be listened for by the Neck directly:
        self.neck.seh.propagateSignal(FatalError("i.am.a.fatal.error"))
        assert self.head.signalReceived.acquire(timeout=SYNC_API_TIMEOUT)
        count += 1
        es = self.head.signal
        assert len(es) == count, "Got: %(G)s" % {"G":count}
        #    Now fire OUR signal into the Neck and check that it is received!
        if enableFilters:
            enabler = eGlobalEnable.ON
        else:
            enabler = eGlobalEnable.OFF
        api = self.head.api.tas.signalFilter.globalEnable(enabler)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        assert api()
        if unmuteAll:
            enabler = eMute.OFF
        else:
            enabler = eMute.ON
        api = self.head.api.tas.signalFilter.muteAll(enabler)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        assert api()
        for (ns_, eM) in ns:
            ms = MySignal()
            ms.setNamespace(ns_)
            self._logger.warn("Lets play...")
            self.neck.seh.propagateSignal(ms)
            r = self.head.signalReceived.acquire(timeout=SYNC_API_TIMEOUT_FOR_DEBUGGING_ONLY)
            if eM == eMute.OFF:
                assert r
                count += 1
            else:
                assert not r
            assert len(self.head.signal) == count
        #    Now set the global mute status back to what it was:
        gM = originalStatus.globalMute()
        api = self.head.api.tas.signalFilter.muteAll(gM)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalMute() == gM
        #    Now set the global enable status back to what it was:
        gE = originalStatus.globalEnable()
        api = self.head.api.tas.signalFilter.globalEnable(gE)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.globalEnable() == gE
        return count
    def testAddManyNamespaces(self, count=0):
        self.testStatus()
        ns = [Namespace("ns.1"), Namespace("ns.2"), Namespace("ns.3")]
        nsIds = []
        for i in ns:
            nsIds.append(i.id_())
        api = self.head.api.tas.signalFilter.add(ns)
        api.sync = eSync.SYNCHRONOUS
        api.timeout = SYNC_API_TIMEOUT
        result = api()
        assert isinstance(result[0], dict)
        assert isinstance(result[1], iSignalFilterStatus)
        sfs = result[0]
        assert len(sfs.keys()) == 3
        for (fId, fltr) in sfs.items():
            assert fId in nsIds
            assert isinstance(fltr, iASignalFilter), "Got: %(R)s" % {"R":fltr}
            assert isinstance(fltr.fId(), iFilterId)
            assert fltr._mute == eMute.OFF
            foundNs = False
            for i in ns:
                if fltr.namespace().compare(i):
                    foundNs = True
                    break
            assert foundNs
        count = self._doSignalInjection([(n.namespace(), eMute.OFF) for n in ns], count=count, enableFilters=True, unmuteAll=True)
        count = self._doSignalInjection([(n.namespace(), eMute.ON) for n in ns], count=count, enableFilters=False, unmuteAll=True)
        return (ns, sfs, count)
    def testRemoveSingleNamespaceInamespace(self, count=0):
        (ns, _fId, count) = self.testAddSingleNamespace(count)
        #    Now remove it.
        api = self.head.api.tas.signalFilter.remove(ns)
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        fltrs = result[0]
        assert len(fltrs) == 1
        _id = ns.id_()
        assert _id == fltrs.keys()[0]
        assert eSignalFilterResponse.isValid(fltrs.values()[0][1])
        assert fltrs[_id][1] == eSignalFilterResponse.REMOVED
        status = result[1]
        assert isinstance(status, iSignalFilterStatus)
        assert status.globalMute() == SignalFilters.DEFAULT__GLOBAL_MUTE
        assert status.globalEnable() == SignalFilters.DEFAULT__GLOBAL_ENABLE
        return count
    def testRemoveSingleNamespaceIfilterid(self, count=0):
        (_ns, fId, count) = self.testAddSingleNamespace(count)
        #    Now remove it.
        api = self.head.api.tas.signalFilter.remove(fId)
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        fltrs = result[0]
        assert len(fltrs) == 1
        _id = fId.id_()
        assert _id == fltrs.keys()[0]
        assert eSignalFilterResponse.isValid(fltrs.values()[0][1])
        assert fltrs[_id][1] == eSignalFilterResponse.REMOVED
        status = result[1]
        assert isinstance(status, iSignalFilterStatus)
        assert status.globalMute() == SignalFilters.DEFAULT__GLOBAL_MUTE
        assert status.globalEnable() == SignalFilters.DEFAULT__GLOBAL_ENABLE
        return count
    def _doRemoveSingleNamespace(self, theList, count=0):
        for ns in theList:
            #    Now remove it.
            api = self.head.api.tas.signalFilter.remove(ns)
            api.timeout = SYNC_API_TIMEOUT
            api.sync = eSync.SYNCHRONOUS
            result = api()
            assert isinstance(result, tuple)
            assert isinstance(result[0], dict)
            fltrs = result[0]
            assert len(fltrs) == 1
            _id = ns.id_()
            assert _id == fltrs.keys()[0]
            assert eSignalFilterResponse.isValid(fltrs.values()[0][1])
            assert fltrs[_id][1] == eSignalFilterResponse.REMOVED
            status = result[1]
            assert isinstance(status, iSignalFilterStatus)
            assert status.globalMute() == SignalFilters.DEFAULT__GLOBAL_MUTE
            assert status.globalEnable() == SignalFilters.DEFAULT__GLOBAL_ENABLE
        #    Now check we have ZERO remaining filers registered:
        api = self.head.api.tas.signalFilter.status()
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.count() == 0
        assert len(ExecutionOrganiser()._signalFilters._filters) == 0
        return count
    def testRemoveSingleNamespaceInManyInamespace(self, count=0):
        (namespace, _sfs, count) = self.testAddManyNamespaces(count)
        self._doRemoveSingleNamespace(namespace, count)
        return count
    def testRemoveSingleNamespaceInManyIfilterid(self, count=0):
        (_namespace, sfs, count) = self.testAddManyNamespaces(count)
        theList = [x.fId() for x in sfs.values()]
        self._doRemoveSingleNamespace(theList, count)
        return count
    def testRemoveSingleNamespaceInManyMixture(self, count=0):
        (namespace, sfs, count) = self.testAddManyNamespaces(count)
        #    Create a list of 2:ns and 1:fId:
        theList = [namespace[2], sfs[namespace[1].id_()].fId(), namespace[0]]
        self._doRemoveSingleNamespace(theList, count)
        return count
    def testRemoveSomeMixture(self, count=0):
        (namespace, sfs, count) = self.testAddManyNamespaces(count)
        #    Create a list of 2:ns and 1:fId:
        theList = [namespace[2], sfs[namespace[1].id_()].fId(), namespace[0]]
        self._doRemoteSome(theList, count)
        return count
    def _doRemoteSome(self, theList, count=0):
        #    Now remove it.
        api = self.head.api.tas.signalFilter.remove(theList)
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        fltrs = result[0]
        assert len(fltrs) == 3
        status = result[1]
        assert isinstance(status, iSignalFilterStatus)
        assert status.globalMute() == SignalFilters.DEFAULT__GLOBAL_MUTE
        assert status.globalEnable() == SignalFilters.DEFAULT__GLOBAL_ENABLE
        for i in theList:
            _id = i.id_()
            assert _id in fltrs.keys()
            assert eSignalFilterResponse.isValid(fltrs[_id][1])
            assert fltrs[_id][1] == eSignalFilterResponse.REMOVED
        #    Now check we have ZERO remaining filers registered:
        api = self.head.api.tas.signalFilter.status()
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, iSignalFilterStatus)
        assert result.count() == 0
        assert len(ExecutionOrganiser()._signalFilters._filters) == 0
        return count
    def testRemoveSomeInamespace(self, count=0):
        (namespace, _sfs, count) = self.testAddManyNamespaces(count)
        #    Create a list of ALL iNamespaces:
        self._doRemoteSome(namespace, count)
        return count
    def testRemoveSomeIfilterid(self, count=0):
        (namespace, _sfs, count) = self.testAddManyNamespaces(count)
        #    Create a list of ALL iNamespaces:
        self._doRemoteSome(namespace, count)
        return count
    def _doMute(self, theList, count=0):
        #    Build up a cache of the namespaces wrt the filterIds.
        namespaceCache = {}
        #    A full mute-cycle:
        for i in theList:
            if isinstance(i, iFilterId):
                if isinstance(i, iFilterId):
                    #    Query the filter for this filterId and use it's namespace as '_ns'.
                    api = self.head.api.tas.signalFilter.query(i)
                    api.timeout = SYNC_API_TIMEOUT
                    api.sync = eSync.SYNCHRONOUS
                    result = api()
                    fltrs = result[0]
                    ns = fltrs.values()[0].namespace()
                    namespaceCache[i.id_()] = (i, Namespace(namespace=ns, _nId=i.id_()))
            elif isinstance(i, iNamespace):
                namespaceCache[i.id_()] = (i, i)
            else:
                assert not (isinstance(i, iNamespace) or isinstance(i, iFilterId))
        for i in theList:
            for eM in [eMute.ON, eMute.OFF, eMute.ON, eMute.OFF]:
                (ns, i_namespace) = namespaceCache[i.id_()]
                mute = (ns, eM)
                api = self.head.api.tas.signalFilter.mute(mute)
                api.timeout = SYNC_API_TIMEOUT
                api.sync = eSync.SYNCHRONOUS
                result = api()
                assert isinstance(result, tuple)
                fltrs = result[0]
                assert isinstance(fltrs, dict)
                assert len(fltrs.keys()) == 1
                #    Now check the global status hasn't changed:
                api = self.head.api.tas.signalFilter.status()
                api.timeout = SYNC_API_TIMEOUT
                api.sync = eSync.SYNCHRONOUS
                result = api()
                assert isinstance(result, iSignalFilterStatus)
                assert result.count() == 3
                assert result.globalEnable() == SignalFilters.DEFAULT__GLOBAL_ENABLE
                assert result.globalMute() == SignalFilters.DEFAULT__GLOBAL_MUTE
                #    Now check that the filter status is as desired:
                api = self.head.api.tas.signalFilter.query(ns)
                api.timeout = SYNC_API_TIMEOUT
                api.sync = eSync.SYNCHRONOUS
                result = api()
                assert isinstance(result, tuple)
                assert isinstance(result[0], dict)
                assert isinstance(result[1], iSignalFilterStatus)
                fltrs = result[0]
                assert len(fltrs.keys()) == 1
                f = fltrs.values()[0]
                assert isinstance(f, iASignalFilter)
                assert f.mute() == eM
                #    Now fire a signal to test the filter's mute is as desired.
                count = self._doSignalInjection([(i_namespace.namespace(), eM)], count=count, enableFilters=True, unmuteAll=True)
        #    Now set the mute status for each item en-masse (same mute value):
        mutes = []
        for ns in theList:  #    [eMute.ON, eMute.OFF, eMute.ON, eMute.OFF]
            mute = (ns, eM)
            mutes.append(mute)
        api = self.head.api.tas.signalFilter.mute(mutes)
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, tuple)
        fltrs = result[0]
        assert isinstance(fltrs, dict)
        assert len(fltrs.keys()) == len(namespaceCache.keys())
        return count
    def testMuteInamespace(self, count=0):
        #    Mute each filter in turn, checking between calls.
        (namespace, _sfs, count) = self.testAddManyNamespaces(count)
        count = self._doMute(namespace, count)
        return count
    def testMuteIfilterId(self, count=0):
        (namespace, sfs, count) = self.testAddManyNamespaces(count)
        a = sfs[namespace[1].id_()].namespace()
        b = sfs[namespace[0].id_()].namespace()
        c = sfs[namespace[2].id_()].namespace()
        theList = [a, b, c]
        count = self._doMute(theList, count)
        return count
    def testMuteMixture(self, count=0):
        (namespace, sfs, count) = self.testAddManyNamespaces(count)
        theList = [namespace[1], sfs[namespace[0].id_()].fId(), namespace[2]]
        return self._doMute(theList, count)
    def testQueryValidMixture(self, count=0):
        (namespace, sfs, count) = self.testAddManyNamespaces(count)
        #    Now query all combinations one at a time.
        invalidId = iFilterIdentifier.nId.next() 
        iFid = FilterId(invalidId)
        iFid._id = invalidId
        theList = [Namespace(namespace="hello.world!", _nId=invalidId), iFid, namespace[2], namespace[0], sfs[namespace[1].id_()].fId()]
        for ns in theList:
            #    Query the given filter:
            api = self.head.api.tas.signalFilter.query(ns)
            api.timeout = SYNC_API_TIMEOUT
            api.sync = eSync.SYNCHRONOUS
            result = api()
            assert isinstance(result, tuple)
            assert isinstance(result[0], dict)
            assert isinstance(result[1], iSignalFilterStatus)
            fltrs = result[0]
            assert len(fltrs.keys()) == 1
            (_, f) = fltrs.items()[0]
            if ns.id_() == invalidId:
                assert isinstance(f, UnknownSignalFilter)
                if isinstance(ns, iNamespace):
                    assert isinstance(f.message, iNamespace)
                    assert f.message.compare(ns)
                elif isinstance(ns, iFilterId):
                    assert isinstance(f.message, iFilterId)
                    assert f.message.id_() == ns.id_()
                else:
                    assert False
            else:
                assert isinstance(f, iASignalFilter)
                assert f.mute() == SignalFilters.DEFAULT__GLOBAL_MUTE
        return count
    def testQueryValidMixtureAllAtOnce(self, count=0):
        (namespace, sfs, count) = self.testAddManyNamespaces(count)
        #    Now query all combinations at once.
        invalidId = iFilterIdentifier.nId.next() 
        iFid = FilterId(invalidId)
        iFid._id = invalidId
        theList = [Namespace(namespace="hello.world!", _nId=invalidId), iFid, namespace[2], namespace[0], sfs[namespace[1].id_()].fId()]
        #    Query the given filter:
        api = self.head.api.tas.signalFilter.query(theList)
        api.timeout = SYNC_API_TIMEOUT
        api.sync = eSync.SYNCHRONOUS
        result = api()
        assert isinstance(result, tuple)
        assert isinstance(result[0], dict)
        assert isinstance(result[1], iSignalFilterStatus)
        fltrs = result[0]
        assert len(fltrs.keys()) == 4
        #    Now check the result for each filter:
        for (id_, f) in fltrs.items():
            count = self._checkQuery(theList, id_, f, invalidId, count)
        return count
    def _checkQuery(self, theList, id_, f, invalidId, count):
        for ns in theList:
            if ns.id_() == id_:
                if ns.id_() == invalidId:
                    assert isinstance(f, UnknownSignalFilter)
                    if isinstance(f.message, iNamespace):
                        assert f.message.compare(ns.id_())
                    elif isinstance(f.message, iFilterId):
                        assert f.message.id_() == ns.id_()
                    else:
                        assert False
                else:
                    assert isinstance(f, iASignalFilter)
                    assert f.mute() == SignalFilters.DEFAULT__GLOBAL_MUTE
        return count
#
# class TXXXestStateChangePropagation(unittest.TestCase):
#    def setUp(self):
#        sys.argv = sys.argv[:1]
#        self.stateChange = []
#        self._logger = LogManager().getLogger(self.__class__.__name__)
#        print os.getcwd()
#        path = os.path.realpath("config/ipc")
#        ConfigurationManager(cwd=path)
#        self.qTransport = QueueTransportDetails()
#        self.head = Head(self.qTransport)
#        self.neck = Neck(self.qTransport.invert())
#        self.SignalExchangeHub = SignalExchangeHub()
#        self.stateChange = []
#        self.stateChangeLock = Semaphore(0)
#    def tearDown(self):
#        self.head.teardown()
#        self.neck.teardown()
#        try:    self.qTransport.del_qRx()
#        except: pass
#        try:    self.qTransport.del_qTx()
#        except: pass
#        SignalExchangeHub.destroySingleton()
#    def test(self):
#        #    Setup the handler:
#        self.head.api.tas.setHandler(iTas.EVENT__ENGINE_STATE_CHANGE, self._onStateChangeEvent)
#        #    Now trigger a state-change:
#        eUid = 123
#        eNewState = 456
#        ePreviousState = 789
#        api = self.neck.api.tas.engineStateChange(eUid, eNewState, ePreviousState)
#        api.sync = eSync.ASYNCHRONOUS
#        api.solicited = False
#        api()
#        assert self.stateChangeLock.acquire(timeout=2)
#        assert len(self.stateChange)==1
#        assert self.stateChange[0][0]==eUid
#        assert self.stateChange[0][1]==eNewState
#        assert self.stateChange[0][2]==ePreviousState
#    def _onStateChangeEvent(self, tId, bSyncrhonous, uId, newState, previousState):
#        self.stateChangeLock.release()
#        self.stateChange.append((uId, newState, previousState))
#
# #class TestLoggingSynchronous(unittest.TestCase):
# #    def setUp(self):
# #        sys.argv = sys.argv[:1]
# #        print os.getcwd()
# #        path = os.path.realpath("config/ipc")
# #        ConfigurationManager(cwd=path)
# #        self.qTransport = QueueTransportDetails()
# #        self.head = Head(self.qTransport)
# #        self.neck = Neck(self.qTransport.invert())
# #    def tearDown(self):
# #        self.head.ipc.close(ignoreErrors=True)
# #        self.neck.ipc.close(ignoreErrors=True)
# #        try:    self.qTransport.del_qRx()
# #        except: pass
# #        try:    self.qTransport.del_qTx()
# #        except: pass
# #        SignalExchangeHub.destroySingleton()
# #    def test1On(self):
# #        self.on()
# #    def test2Off(self):
# #        self.off()
# #    def tXXXest3Cycle(self):
# #        if LogManager().isOn()==True:
# #            c = [self.off, self.on, self.off, self.on]
# #        else:
# #            c = [self.on, self.off, self.on, self.off]
# #        for i in c:
# #            i()
# #    def on(self, sync=eSync.SYNCHRONOUS, timeout=SYNC_API_TIMEOUT):
# #        api = self.head.api.tas.logging.turnOn()
# #        api.sync = sync
# #        api.timeout = timeout
# #        try:
# #            result = api()
# #        except Exception, _e:
# #            raise
# #        assert isinstance(result, iLoggingResult)
# #        assert result.location()==LogManager.FILENAME
# #        assert result.isOn()==eLoggingState.ON
# #    def off(self, sync=eSync.SYNCHRONOUS, timeout=SYNC_API_TIMEOUT):
# #        api = self.head.api.tas.logging.turnOff()
# #        api.sync = sync
# #        api.timeout = timeout
# #        try:
# #            result = api()
# #        except Exception, _e:
# #            raise
# #        assert isinstance(result, iLoggingResult)
# #        assert result.location()==LogManager.FILENAME
# #        assert result.isOn()==eLoggingState.OFF
#
# class TXXXestLoggingAsynchronous(unittest.TestCase):
#    def setUp(self):
#        sys.argv = sys.argv[:1]
#        print os.getcwd()
#        path = os.path.realpath("config/ipc")
#        ConfigurationManager(cwd=path)
#        self.qTransport = QueueTransportDetails()
#        self.head = Head(self.qTransport)
#        self.neck = Neck(self.qTransport.invert())
#    def tearDown(self):
#        self.head.teardown()
#        self.neck.teardown()
#        try:    self.qTransport.del_qRx()
#        except: pass
#        try:    self.qTransport.del_qTx()
#        except: pass
#        SignalExchangeHub.destroySingleton()
#    def test1On(self):
#        self.on()
#    def test2Off(self):
#        self.off()
#    def tXXXest3Cycle(self):
#        if LogManager().isOn()==True:
#            c = [self.off, self.on, self.off, self.on]
#        else:
#            c = [self.on, self.off, self.on, self.off]
#        for i in c:
#            i()
#    def on(self, sync=eSync.ASYNCHRONOUS, timeout=SYNC_API_TIMEOUT):
#        api = self.head.api.tas.logging.turnOn()
#        api.sync = sync
#        api.timeout = timeout
#        result = api()
#        try:
#            response = result.acquireNew(timeout=SYNC_API_TIMEOUT, purge=True)
#        except Exception, _e:
#            raise
#        assert isinstance(response, iLoggingResult)
#        assert response.location()==LogManager.FILENAME
#        assert response.isOn()==eLoggingState.ON
#    def off(self, sync=eSync.ASYNCHRONOUS, timeout=SYNC_API_TIMEOUT):
#        api = self.head.api.tas.logging.turnOff()
#        api.sync = sync
#        api.timeout = timeout
#        result = api()
#        try:
#            response = result.acquireNew(timeout=SYNC_API_TIMEOUT, purge=True)
#        except Exception, _e:
#            raise
#        assert isinstance(response, iLoggingResult)
#        assert response.location()==LogManager.FILENAME
#        assert response.isOn()==eLoggingState.OFF
#
# class TXXXestTestManagementTests(unittest.TestCase):
#    def testQuery(self):
#        pass
#    def testQueryTests(self):
#        pass
#    def testQueryTestPacks(self):
#        pass
#
# class TXXXestTestManagementStats(unittest.TestCase):
#    def testQuery(self):
#        pass
if __name__ == '__main__':
    unittest.main()
