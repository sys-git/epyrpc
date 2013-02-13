
from Queue import Empty
from epyrpc.core.IpcExceptions import NoResponseRequired, TransportFinishedError, \
    TransportDisconnectedError
from epyrpc.core.transaction.TransactionManager import TransactionManager
from epyrpc.core.transport.algos.compression.ZlibCompressor import ZlibCompressor
from epyrpc.core.transport.algos.encryption.NoEncryption import NoEncryption
from epyrpc.core.transport.algos.iAlgoImpl import iAlgoImpl
from epyrpc.core.transport.algos.iCompressor import iCompressor
from epyrpc.core.transport.algos.iEncryptor import iEncryptor
from epyrpc.core.transport.details.QueueTransportDetails import \
    QueueTransportDetails
from epyrpc.core.transport.eIpcTransportState import eIpcTransportState
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener
from epyrpc.core.transport.messages.IpcDataMessage import IpcDataMessage
from epyrpc.core.transport.messages.IpcTransportMessage import \
    IpcTransportMessage
from epyrpc.core.transport.messages.eIpcTransportCommand import \
    eIpcTransportCommand
from epyrpc.core.transport.queue.QueueObject import QueueObject
from epyrpc.core.transport.queue.QueueTransporter import QueueTransporter
from epyrpc.head.HeadQueueTransporter import HeadQueueTransporter
from epyrpc.synchronisation.generators.HeadTransactionIdGenerator import \
    HeadTransactionIdGenerator
from epyrpc.synchronisation.generators.NeckTransactionIdGenerator import \
    NeckTransactionIdGenerator
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
from multiprocessing.synchronize import RLock, Semaphore
from random import Random
import multiprocessing
import pickle
import threading
import time
import unittest

class TestQueueTransporterWithQueues(unittest.TestCase, iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    def setUp(self):
        self._logger = LogManager().getLogger(self.__class__.__name__)
        self.qTransport = QueueTransportDetails()
        self.data = []
        self.state = []
        self.disconnect = []
        self.stateChange = multiprocessing.Semaphore(0)
        self.dataReceive = multiprocessing.Semaphore(0)
        self.disconnectReceive = multiprocessing.Semaphore(0)
        self.dataResponse = None
        self.tm = TransactionManager()
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
    def tearDown(self):
        self.data = []
        self.state = []
        time.sleep(1)
        self.tm = None
        self.qt.close(ignoreErrors=True)
        time.sleep(2)
        self.qTransport.del_qRx()
        self.qTransport.del_qTx()
    def transportStateChange(self, state):
        self.state.append(state)
        self.stateChange.release()
    def transportDataReceive(self, tId, data):
        self.data.append((tId, data))
        self.dataReceive.release()
        rtn = self.dataResponse
        if isinstance(rtn, Exception):
            raise rtn
        if rtn:
            return rtn
        raise NoResponseRequired(tId)
    def _respondToDisconnect(self):
        data = self.qTransport.qTx().get().data()
        data = pickle.loads(data)
        self.disconnect.append(data)
        self.disconnectReceive.release()
        self.qt.sendRaw(IpcTransportMessage(eIpcTransportCommand.DISCONNECTED))
    def testIsConnected(self):
        self.qt.connect()
        assert self.qt.isConnected()
        assert not self.qt.isFinished()
    def testDisconnectWhenRemoteSideUnresponsive(self):
        self.qt.connect()
        assert len(self.state) == 0
        solicited = True
        timeStart = time.time()
        tOut = 3  # 000 #    FIXME: 3
        self.qt.disconnect(tOut, solicited)
        timeEnd = time.time()
        timeDelta = timeEnd - timeStart
        assert timeDelta > (tOut - 2)
        assert timeDelta < (tOut + 2)
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
        assert len(self.state) == 0
    def testReceiveDisconnectRequest(self):
        self.qt.connect()
        self.stateChange.acquire(timeout=5)
        assert len(self.state) == 0
        msg = IpcTransportMessage(eIpcTransportCommand.DISCONNECT)
        msg = QueueObject(pickle.dumps(msg), "")
        self.qTransport.qRx().put(msg)
        assert self.stateChange.acquire(timeout=5)
        assert self.state[0] == eIpcTransportState.DISCONNECTED
        assert self.stateChange.acquire(timeout=5)
        assert self.state[1] == eIpcTransportState.CLOSED
        time.sleep(1)
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
    def testReceiveTransactionResponse(self):
        self.qt.connect()
        tId = self.tm.create()
        eResult = "hello world!"
        msg = QueueObject(pickle.dumps(IpcDataMessage(eResult, tId=tId)), "")
        self.qTransport.qRx().put(msg)
        #    Now wait for the result:
        result = self.tm.acquireNew(tId, 5)
        assert len(self.data) == 0
        assert result == eResult
    def testReceiveNoResponseTidIsNone(self):
        self.qt.connect()
        eResult = "hello world!"
        msg = IpcDataMessage(eResult)
        self.dataResponse = None
        msg = QueueObject(pickle.dumps(msg), "")
        self.qTransport.qRx().put(msg)
        self.dataReceive.acquire(timeout=5)
        time.sleep(1)
        l = len(self.data)
        assert l == 1, "got: %(D)s" % {"D":l}
        self._logger.debug("data: %(D)s" % {"D":self.data})
        assert self.data[0][0] == None, "got: %(D)s" % {"D":self.data[0][0]}
        assert self.data[0][1] == eResult, "got: %(D)s" % {"D":self.data[0][1]}
    def testSendDataSolicited(self):
        self.qt.connect()
        eResult = "hello world!"
        try:
            result = self.qTransport.qTx().get(block=False)
        except Empty:
            assert True
        else:
            assert False, "Got: %(F)s" % {"F":result}
        tId = self.qt.sendData(eResult, solicited=True)
        data = self.qTransport.qTx().get(timeout=5)
        data = pickle.loads(data.data())
        assert isinstance(data, IpcDataMessage), "got data: %(M)s" % {"M":data}
        assert data.tId == tId
        msg = data.message()
        assert msg == eResult, "got msg: %(M)s" % {"M":msg}
    def testSendDataUnsolicited(self):
        self.qt.connect()
        eResult = "hello world!"
        tId = self.qt.sendData(eResult, solicited=False)
        assert tId == None
        data = self.qTransport.qTx().get(timeout=5)
        data = pickle.loads(data.data())
        assert isinstance(data, IpcDataMessage), "got data: %(M)s" % {"M":data}
        assert data.tId == tId
        msg = data.message()
        assert msg == eResult, "got msg: %(M)s" % {"M":msg}
    def testSendRaw(self):
        self.qt.connect()
        eResult = "hello world!"
        self.qt.sendRaw(eResult)
        data = self.qTransport.qTx().get(timeout=5)
        data = pickle.loads(data.data())
        assert data == eResult, "got data: %(M)s" % {"M":data}
    def testSendRawPostClose(self):
        self.qt.connect()
        eResult = "hello world!"
        self.qt.close()
        try:
            self.qt.sendRaw(eResult)
        except TransportFinishedError, _e:
            assert True
        else:
            assert False
    def testSendDataPostClose(self):
        self.qt.connect()
        eResult = "hello world!"
        self.qt.close()
        try:
            self.qt.sendData(eResult)
        except TransportFinishedError, _e:
            assert True
        else:
            assert False
    def testConnectPostClose(self):
        self.qt.connect()
        self.qt.close()
        try:
            self.qt.connect()
        except TransportFinishedError, _e:
            assert True
        else:
            assert False
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
    def testDisconnectPostClose(self):
        self.qt.connect()
        self.qt.close()
        try:
            self.qt.disconnect()
        except TransportFinishedError, _e:
            assert True
        else:
            assert False
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
    def testDisconnect(self):
        self.qt.connect()
        t = threading.Timer(0, self._respondToDisconnect)
        t.start()
        time.sleep(1)
        self.qt.disconnect(noCallback=True)
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
        assert self.disconnectReceive.acquire(timeout=5)
        data = self.disconnect[0]
        assert isinstance(data, IpcTransportMessage), "data: %(D)s" % {"D":data}
        assert data.command() == eIpcTransportCommand.DISCONNECT
        l = len(self.state)
        assert l == 0, "Got: %(D)s" % {"D":l}
    def testDisconnectWithCallback(self):
        self.qt.connect()
        t = threading.Timer(0, self._respondToDisconnect)
        t.start()
        time.sleep(1)
        self.qt.disconnect(noCallback=False)
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
        assert self.disconnectReceive.acquire(timeout=5)
        data = self.disconnect[0]
        assert isinstance(data, IpcTransportMessage), "data: %(D)s" % {"D":data}
        cmd = data.command()
        assert cmd == eIpcTransportCommand.DISCONNECT
        l = len(self.state)
        assert l == 2, "Got: %(D)s" % {"D":l}
class NoResult(object): pass

unknownException = Exception("unknown")
noresponseException = NoResponseRequired("ns")
noResult = NoResult()

class MyReceiver(iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    commands = {"a"}
    cmdResultMapping = {
                        #    Commands:
                        "a":"aa",  # Head::eResult = "aa", Neck::eResult = catch: Exception("Error processing result")
                        #    Results:
                        "aa":None,
                        }
    def __init__(self, transporter, qTransport, generator, logger):
        self._logger = logger
        self.data = []
        self.state = []
        self.stateChange = multiprocessing.Semaphore(0)
        self.dataReceive = multiprocessing.Semaphore(0)
        self.tm = TransactionManager(generator)
        self.qt = transporter(qTransport, self.tm, self, self, self._logger)
    def transportStateChange(self, state):
        self._logger.debug("StateChange RX: %(S)s" % {"S":state})
        self.state.append(state)
        self.stateChange.release()
    def transportDataReceive(self, tId, d):
        self._logger.debug("Data RX: %(T)s - %(D)s" % {"T":tId, "D":d})
        self.data.append((tId, d))
        self.dataReceive.release()
        try:
            rtn = MyReceiver.cmdResultMapping[d]
        except Exception, _e:
            rtn = unknownException
        if isinstance(rtn, Exception):
            raise rtn
        if rtn:
            return rtn

class TestQueueTransporterAtEachEnd(unittest.TestCase):
    def setUp(self):
        self._logger = LogManager().getLogger(self.__class__.__name__)
        self.qTransport = QueueTransportDetails()
        invertedTransport = self.qTransport.invert()
        self.neck = MyReceiver(QueueTransporter, self.qTransport, NeckTransactionIdGenerator(), logger=LogManager().getLogger("Neck"))
        self.head = MyReceiver(HeadQueueTransporter, invertedTransport, HeadTransactionIdGenerator(), logger=LogManager().getLogger("Head"))
    def tearDown(self):
        self._logger.debug("teardown...")
        self.data = []
        self.state = []
        time.sleep(1)
        self.tm = None
        self.neck.qt.close(ignoreErrors=True)
        self.head.qt.close(ignoreErrors=True)
        self.qTransport.del_qRx()
        self.qTransport.del_qTx()
    def testRoundTripSolicited(self):
        self.head.qt.connect()
        self.neck.qt.connect()
        tIds = []
        for i in range(0, 10):
            k = (i + 1)
            COMMAND = "a"
            tId = self.head.qt.sendData(COMMAND, solicited=True)
            assert tId
            assert tId not in tIds
            tIds.append(tId)
            #    Now check NO data received by listener:
            l = len(self.head.data)
            assert l == 0, "Got: %(L)s" % {"L":l}
            #    Now check the transaction data:
            data = self.head.tm.acquireNew(tId, 5)
            eData = MyReceiver.cmdResultMapping[COMMAND]
            assert data == eData, "Got: %(D)s" % {"D":data}
            #    Now check data received by Neck:
            l = len(self.neck.data)
            assert l == k, "Got: %(L)s" % {"L":l}
            assert self.neck.data[i][0] == tId, "Got: %(D)s" % {"D":self.neck.data[i][0]}
            assert self.neck.data[i][1] == COMMAND, "Got: %(D)s" % {"D":self.neck.data[i][1]}
    def testRoundTripUnsolicited(self):
        self.head.qt.connect()
        self.neck.qt.connect()
        for i in range(0, 10):
            k = i + 1
            for COMMAND in MyReceiver.commands:
                self._logger.debug("COMMAND( %(I)s ): %(C)s" % {"C":COMMAND, "I":i})
                tId = self.head.qt.sendData(COMMAND, solicited=False)
                assert not tId
                #    Now check the transaction data has arrives:
                try:
                    self.head.tm.acquireNew(tId, 5)
                except KeyError, _e:
                    assert True
                self.neck.dataReceive.acquire(timeout=5)
                #    Now check data IS received by listener:
                data = self.neck.data
                l = len(data)
                assert l == k, "Got: %(L)s" % {"L":len(data)}
                assert data[i][0] == None, "Got: %(D)s" % {"D":data[i][0]}
                assert data[i][1] == COMMAND, "Got: %(D)s" % {"D":data[i][1]}
    def testHeadClosesNoStateChangeEvent(self):
        self.head.qt.connect()
        l = len(self.head.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
        self.neck.qt.connect()
        l = len(self.neck.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
        self.head.qt.close()
        #    Now check head disconnected, neck auto-disconnection is not guaranteed.
        l = len(self.head.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
    def testHeadClosesWithStateChangeEvent(self):
        self.head.qt.connect()
        l = len(self.head.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
        self.neck.qt.connect()
        l = len(self.neck.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
        self.head.qt.close(noCallback=False)
        #    Now check head disconnected, neck auto-disconnection is not guaranteed.
        l = len(self.head.state)
        assert l == 2, "Got: %(L)s" % {"L":l}
        assert self.head.state[0] == eIpcTransportState.DISCONNECTED
        assert self.head.state[1] == eIpcTransportState.CLOSED
        #    Now check if neck disconnects (optional!):
        if self.neck.stateChange.acquire(timeout=5):
            l = len(self.neck.state)
            assert l == 2, "Got: %(L)s" % {"L":l}
    def testNeckClosesWithStateChangeEvent(self):
        self.head.qt.connect()
        l = len(self.head.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
        self.neck.qt.connect()
        l = len(self.neck.state)
        assert l == 0, "Got: %(L)s" % {"L":l}
        self.neck.qt.close(noCallback=False)
        assert self.head.stateChange.acquire(timeout=5)
        assert self.neck.stateChange.acquire(timeout=5)
        #    Now check neck disconnected, head auto-disconnection is not guaranteed.
        l = len(self.neck.state)
        assert l == 2, "Got: %(L)s" % {"L":l}
        assert self.neck.state[0] == eIpcTransportState.DISCONNECTED
        assert self.neck.state[1] == eIpcTransportState.CLOSED
        #    Now check if head disconnects (optional!):
        if self.head.stateChange.acquire(timeout=5):
            l = len(self.head.state)
            assert l == 2, "Got: %(L)s" % {"L":l}
    def testNeckInitiatedUnsolicitedEvents(self):
        self.head.qt.connect()
        self.neck.qt.connect()
        for i in range(0, 10):
            k = (i + 1)
            eResult = "a"
            tId = self.neck.qt.sendData(eResult, solicited=False)
            assert self.head.dataReceive.acquire(timeout=5)
            assert len(self.head.data) == k
            data = self.head.data[i]
            assert data[0] == tId, "Got: %(D)s" % {"D":data[0]}
            assert data[1] == eResult
    def testSendDataWithCallback(self):
        self.head.qt.connect()
        self.neck.qt.connect()
        self.dataReceived = [] 
        self.dataReceivedLock = Semaphore(0)
        def cb(tId, data):
            self._logger.debug("CB !")
            self.dataReceived.append((tId, data))
            self.dataReceivedLock.release()
        COMMAND = "a"
        eResult = MyReceiver.cmdResultMapping[COMMAND]
        tId = self.head.qt.sendData(COMMAND, solicited=True, callback=cb)
        assert tId
        assert not self.head.dataReceive.acquire(timeout=2)
        assert self.dataReceivedLock.acquire(timeout=5)
        assert len(self.dataReceived) == 1
        assert self.dataReceived[0][0] == tId
        assert self.dataReceived[0][1] == eResult


class ConcurrentPayload(object):
    def __init__(self, command, solicited=True, timeout=None, result=noResult):
        self.timeout = timeout
        self.result = result
        self.command = command
        self.solicited = solicited
    def isCommand(self):
        return self.command
    def __eq__(self, other):
        return self.timeout == other.timeout and self.result == other.result and self.command == other.command and self.solicited == other.solicited

class TimerArgs(object):
    def __init__(self, tId=None, result=None, timer=None, solicited=True):
        self.tId = tId
        self.result = result
        self.timer = timer
        self.solicited = solicited

class MyConcurrentReceiver(iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    commands = {"a"}
    def __init__(self, qTransport, generator, logger):
        self._logger = logger
        self.data = []
        self.state = []
        self.stateChange = multiprocessing.Semaphore(0)
        self.dataReceive = multiprocessing.Semaphore(0)
        self.tm = TransactionManager(generator)
        self.threads = []
        self.qTransport = qTransport
        self.qt = HeadQueueTransporter(self.qTransport, self.tm, self, self, self._logger)
    def transportStateChange(self, state):
        self._logger.debug("StateChange RX: %(S)s" % {"S":state})
        self.state.append(state)
        self.stateChange.release()
    def transportDataReceive(self, tId, d):
        self._logger.debug("Data RX: %(T)s - %(D)s" % {"T":tId, "D":d})
        assert isinstance(d, ConcurrentPayload), "Got: %(D)s" % {"D":d}
        if d.isCommand():
            #    Set the async response going:
            result = d.result
            args = TimerArgs(tId=tId, result=result, solicited=result.solicited)
            t = threading.Timer(d.timeout, self._respond, args=[args])
            self.threads.append(t)
            args.timer = t
            t.start()
        self.data.append((tId, d))
        self.dataReceive.release()
        raise noresponseException
    def _respond(self, timerArgs):
        tId = timerArgs.tId
        timer = timerArgs.timer
        if not timer.isAlive():
            self._logger.warn("Timer cancelled: '%(T)s'" % {"T":tId})
        else:
            self._logger.warn("Timer fired!")
            result = timerArgs.result
            if isinstance(result, NoResult):
                return
            solicited = timerArgs.solicited
            if not solicited:
                tId = None
            self.qt.sendData(result, solicited, tId)

class TestConcurrentSynchronisationUsingQueueTransporterAtEachEndAndAsyncCommandsOnly(unittest.TestCase):
    def setUp(self):
        self._logger = LogManager().getLogger(self.__class__.__name__)
        self.qTransport = QueueTransportDetails()
        self.threads = []
        self.finished = False
        self.threadLock = RLock()
        self.head = MyConcurrentReceiver(self.qTransport, HeadTransactionIdGenerator(), LogManager().getLogger("Head"))
        self.neck = MyConcurrentReceiver(self.qTransport.invert(), NeckTransactionIdGenerator(), LogManager().getLogger("Neck"))
    def tearDown(self):
        self._logger.debug("teardown...")
        self.finished = True
        self.data = []
        self.state = []
        time.sleep(1)
        self.tm = None
        self.neck.qt.close(ignoreErrors=True)
        self.head.qt.close(ignoreErrors=True)
        for t in self.neck.threads:
            try:
                t.cancel()
            except:
                pass
        for t in self.head.threads:
            try:
                t.cancel()
            except:
                pass
        for t in self.threads:
            try:
                t.cancel()
            except:
                pass
        self.qTransport.del_qRx()
        self.qTransport.del_qTx()
    def testSingleTransaction(self):
        self.neck.qt.connect()
        self.head.qt.connect()
        i = 0
        k = (i + 1)
        eData = "hello world!"
        timeout = 1
        resultSolicited = True
        requestSolicited = True
        eResult = ConcurrentPayload(False, resultSolicited, result=eData)
        payload = ConcurrentPayload(True, requestSolicited, timeout=timeout, result=eResult)
        tId = self.head.qt.sendData(payload, solicited=requestSolicited)
        assert tId
        assert self.neck.dataReceive.acquire(5)
        #    Did the neck receive the data?
        l = len(self.neck.data)
        assert l == k, "Got: %(L)s" % {"L":l}
        assert self.neck.data[i][0] == tId, "Got: %(R)s" % {"R":self.neck.data[i][0]}
        data = self.neck.data[i][1]
        assert data == payload, "Got: %(R)s" % {"R":data}
        #    Did the head receive the response?
        eTimeout = (timeout + 5)
        result = self.head.tm.acquireNew(tId, eTimeout)
        assert result == eResult, "Got: %(R)s" % {"R":result}
        self._logger.debug("done!")
    def testMultipleSimultaneousTransactionsOnlySolicitedCommandsAndTheirRandomTimeoutResponsesSameThread(self):
        self.neck.qt.connect()
        self.head.qt.connect()
        (eResultMap, maxTimeout) = self._createTestVectors(0)
        #    Now begin all the transactions one after the other.
        for i, (_, item, _) in eResultMap.items():
            tId = self.head.qt.sendData(item, item.solicited)
            eResultMap[i] = (item, tId)
        #    Now wait for all the transactions to complete.
        for i, (item, tId) in eResultMap.items():
            data = self.head.tm.acquireNew(tId, maxTimeout)
            assert isinstance(data, ConcurrentPayload), "Got: %(G)s" % {"G":data}
            eResult = item.result
            assert data == eResult, "Got: %(G)s" % {"G":data}
        self._logger.debug("done!")
    def testMultipleSimultaneousTransactionsOnlySolicitedCommandsAndTheirRandomTimeoutResponsesDifferentThreads(self):
        self._do1(1)
    def testMultipleSimultaneousTransactionsOnlySolicitedCommandsAndTheirRandomTimeoutResponsesDifferentThreadsHammer(self):
        self._do1(2)
    def _do1(self, ref):
        self.neck.qt.connect()
        self.head.qt.connect()
        (eResultMap, maxTimeout) = self._createTestVectors(ref)
        #    Now begin all the transactions one after the other.
        for i, (_, item, _) in eResultMap.items():
            tId = self.head.qt.sendData(item, item.solicited)
            assert tId
            #    Create the thread listener:
            eResultMap[i] = (item, tId)
            self._createListener(eResultMap, i, maxTimeout)
        #    Now check all transactions after maxTimeout:
        time.sleep(maxTimeout + 5)
        for i, (item, result, timeDelta) in eResultMap.items():
            eResult = item.result
            if not isinstance(result, ConcurrentPayload):
                overshoot = (timeDelta - maxTimeout)
                assert False, "[%(I)s] Overshot by %(O)s - Got: %(G)s" % {"G":result, "I":i, "O":overshoot}
            try:
                assert result == eResult, "[%(I)s] Got: %(G)s" % {"G":result, "I":i}
            except Exception, _e:
                pass
        self._logger.debug("done!")
    def _createListener(self, eResultMap, i, maxTimeout):
        t = threading.Thread(target=self._checkTransaction, args=[eResultMap, i, maxTimeout])
        with self.threadLock:
            self.threads.append(t)
        t.start()
    def _checkTransaction(self, eResultMap, i, maxTimeout):
        (item, tId) = eResultMap[i]
        timeStart = time.time()
        try:
            result = self.head.tm.acquireNew(tId, maxTimeout)
        except Exception, e:
            #    Oops!
            result = e
        timeEnd = time.time()
        eResultMap[i] = (item, result, (timeEnd - timeStart))
    def _createTestVectors(self, ref):
        #    Generate some test vectors:
        eResultMap = {}
        if ref == 0:
            maxTimeout = 5
            size = 10
            r = Random()
            for i in range(0, size):
                requestSolicited = True
                responseSolicited = True
                timeout = r.randrange(0, maxTimeout * 10, 1) / float(10)
                eResultMap[i] = (None, ConcurrentPayload(True, requestSolicited, timeout=timeout, result=ConcurrentPayload(False, responseSolicited, result=i)), None)
                return (eResultMap, maxTimeout)
        elif ref == 1:
            maxTimeout = 5
            size = 50
            r = Random()
            for i in range(0, size):
                requestSolicited = True
                responseSolicited = True
                timeout = r.randrange(0, maxTimeout * 10, 1) / float(10)
                eResultMap[i] = (None, ConcurrentPayload(True, requestSolicited, timeout=timeout, result=ConcurrentPayload(False, responseSolicited, result=i)), None)
                return (eResultMap, maxTimeout)
        elif ref == 2:
            maxTimeout = 10
            size = 100
            r = Random()
            for i in range(0, size):
                requestSolicited = True
                responseSolicited = True
                timeout = r.randrange(0, maxTimeout * 10, 1) / float(10)
                eResultMap[i] = (None, ConcurrentPayload(True, requestSolicited, timeout=timeout, result=ConcurrentPayload(False, responseSolicited, result=i)), None)
                return (eResultMap, maxTimeout)
        elif ref == 3:
            maxTimeout = 5
            size = 50
            r = Random()
            maxOffset = 5
            offsets = r.sample(xrange(maxOffset * 10), size)
            offsets.sort()
            for i, o in enumerate(offsets):
                offsets[i] = o / float(10)
            for i in range(0, size):
                requestSolicited = True
                responseSolicited = True
                timeout = r.randrange(0, maxTimeout * 10, 1) / float(10)
                offset = offsets[i]
                eResultMap[i] = (offset, ConcurrentPayload(True, requestSolicited, timeout=timeout, result=ConcurrentPayload(False, responseSolicited, result=i)), None)
            return (eResultMap, maxTimeout, maxOffset)
        elif ref == 4:
            maxTimeout = 10
            size = 25
            r = Random()
            maxOffset = 10
            offsets = r.sample(xrange(maxOffset * 10), size)
            offsets.sort()
            for i, o in enumerate(offsets):
                offsets[i] = o / float(10)
            for i in range(0, size):
                requestSolicited = True
                responseSolicited = True
                timeout = r.randrange(0, maxTimeout * 10, 1) / float(10)
                offset = offsets[i]
                eResultMap[i] = (offset, ConcurrentPayload(True, requestSolicited, timeout=timeout, result=ConcurrentPayload(False, responseSolicited, result=i)), None)
            #    Now configure the spontaneous neck events:
            numHeadEvents = 25
            offsets = r.sample(xrange(maxOffset * 10), numHeadEvents)
            offsets.sort()
            offsetMax = offsets[-1]
            headEvents = []
            for i, o in enumerate(offsets):
                ooo = (o / float(offsetMax))
                ooo = ooo * maxOffset
                eResult = r.choice(range(0, 1000, 1))
                headEvents.append((i, ooo, ConcurrentPayload(False, eResult)))
            return ((eResultMap, maxTimeout, maxOffset), headEvents)
        assert False, "invalid ref: %(R)s" % {"R":ref}
    def testRandomlyStartedTransactionsOnlySolicitedCommandsAndTheirRandomTimeoutResponsesDifferentThreads(self):
        self.neck.qt.connect()
        self.head.qt.connect()
        (eResultMap, maxTimeout, maxOffset) = self._createTestVectors(3)
        #    Now begin all the transactions one after the other.
        for i, (offset, item, _) in eResultMap.items():
            self._startTimer(offset, i, item, eResultMap, maxTimeout)
        #    Now check all transactions after maxTimeout:
        time.sleep(maxTimeout + maxOffset + 5)
        for i, (item, result, timeDelta) in eResultMap.items():
            eResult = item.result
            if not isinstance(result, ConcurrentPayload):
                overshoot = (timeDelta - maxTimeout)
                assert False, "[%(I)s] Overshot by %(O)s - Got: %(G)s" % {"G":result, "I":i, "O":overshoot}
            try:
                assert result == eResult, "[%(I)s] Got: %(G)s" % {"G":result, "I":i}
            except Exception, _e:
                pass
    def _startTimer(self, offset, i, item, eResultMap, maxTimeout):
        t = threading.Timer(offset, self._timerHandler, args=[i, item, eResultMap, maxTimeout])
        with self.threadLock:
            self.threads.append(t)
        t.start()
    def _timerHandler(self, i, item, eResultMap, maxTimeout):
        self._logger.debug("SOLICITED_DATA: %(I)s" % {"I":i})
        tId = self.head.qt.sendData(item, item.solicited)
        self._logger.debug("SOLICITED_DATA: %(I)s, tid: %(T)s" % {"T":tId, "I":i})
        assert tId
        #    Create the thread listener:
        eResultMap[i] = (item, tId)
        self._createListener(eResultMap, i, maxTimeout)
    def testRandomlyStartedTransactionsSolicitedAndUnsolicitedCommandsDifferentThreads(self):
        self.neck.qt.connect()
        self.head.qt.connect()
        ((eResultMap, maxTimeout, maxOffset), headEvents) = self._createTestVectors(4)
        #    Now begin all the unsolicited Neck events:
        self._startNeckEvents(headEvents)
        #    Now begin all the transactions one after the other.
        for i, (offset, item, _) in eResultMap.items():
            self._startTimer(offset, i, item, eResultMap, maxTimeout)
        #    Now check all transactions after maxTimeout:
        time.sleep(maxTimeout + maxOffset + 5)
        for i, (item, result, timeDelta) in eResultMap.items():
            eResult = item.result
            if not isinstance(result, ConcurrentPayload):
                overshoot = (timeDelta - maxTimeout)
                assert False, "[%(I)s] Overshot by %(O)s - Got: %(G)s" % {"G":result, "I":i, "O":overshoot}
            try:
                assert result == eResult, "[%(I)s] Got: %(G)s" % {"G":result, "I":i}
            except Exception, _e:
                pass
    def _startNeckEvents(self, headEvents):
        sem = threading.Semaphore(0)
        t = threading.Timer(0, self._initNeckEvents, args=[sem, headEvents])
        with self.threadLock:
            self.threads.append(t)
        t.start()
        sem.acquire()
    def _initNeckEvents(self, sem, headEvents):
        for i in headEvents:
            (index, offset, result) = i
            t = threading.Timer(offset, self._sendNeckEvent, args=[index, result])
            with self.threadLock:
                self.threads.append(t)
            t.start()
        sem.release()
    def _sendNeckEvent(self, index, result):
        if not self.finished:
            self._logger.debug("EVENT_DATA: %(I)s" % {"I":index})
            tId = self.neck.qt.sendData(result, solicited=False)
            self._logger.debug("EVENT_DATA: %(I)s, tid: %(T)s" % {"T":tId, "I":index})

class TestQueueTransporterNoQueues(unittest.TestCase, iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    def setUp(self):
        self._logger = LogManager().getLogger(self.__class__.__name__)
        self.data = []
        self.state = []
        self.qt = None
        self.tm = TransactionManager()
        self.stateChangeResult = None
        self.dataReceiveResult = None
        self.qTransport = QueueTransportDetails()
    def tearDown(self):
        self.data = []
        self.state = []
        self.qt = None
        self.tm = None
        self.qTransport.del_qRx()
        self.qTransport.del_qTx()
    def transportStateChange(self, state):
        self.state.append(state)
        result = self.stateChangeResult
        if isinstance(result, Exception):
            raise result
        return result
    def transportDataReceive(self, tId, data):
        self.data.append((tId, data))
        result = self.dataReceiveResult
        if isinstance(result, Exception):
            raise result
        return result
    def testSendDataNoConnect(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        try:
            self.qt.sendData("hello world!")
        except TransportDisconnectedError, _e:
            assert True
        else:
            assert False
    def testSendRawNoConnect(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        try:
            self.qt.sendRaw("hello world!")
        except TransportDisconnectedError, _e:
            assert True
        else:
            assert False
    def testPrivateReceiveRawPostFinished(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        self.qt.close()
        try:
            self.qt._receiveRaw()
        except TransportFinishedError:
            assert True
        else:
            assert False
    def testSendDataPostFinished(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        self.qt.close()
        try:
            self.qt.sendData("hello world!")
        except TransportFinishedError:
            assert True
        else:
            assert False
    def testSendRawPostFinished(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        self.qt.close()
        try:
            self.qt.sendRaw("hello world!")
        except TransportFinishedError:
            assert True
        else:
            assert False
    def testConnectPostFinished(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        self.qt.close()
        try:
            self.qt.connect()
        except TransportFinishedError:
            assert True
        else:
            assert False
    def testPrivateDoConnectRunsReceiveThread(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        self.qt._doConnect()
        assert isinstance(self.qt._receiver, threading.Thread)
        self.qt.close()
    def testCloseYieldsNoCallback(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        self.qt.close()
        assert not self.qt.isConnected()
        assert self.qt.isFinished()
        assert len(self.state) == 0
    def testProtectedCloseYieldsErrorToClients(self):
        self.qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        tId = self.tm.create()
        sem = threading.Semaphore(0)
        semEnd = threading.Semaphore(0)
        noCallback = False
        t = threading.Timer(1, self._client, args=[sem, semEnd, self.qt, noCallback])
        t.start()
        sem.acquire()
        result = self.tm.acquireNew(tId, 5)
        assert len(self.state) == 2
        assert self.state[0] == eIpcTransportState.DISCONNECTED
        assert self.state[1] == eIpcTransportState.CLOSED
        assert isinstance(result, TransportFinishedError)
    def _client(self, sem, semEnd, qt, noCallback):
        sem.release()
        time.sleep(1)
        qt._close(noCallback=noCallback)
        semEnd.release()
    def testInit(self):
        QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
    def testInitBadTransport(self):
        try:
            QueueTransporter(None, self.tm, self, self, self._logger)
        except AssertionError, _e:
            assert True
        else:
            assert False
    def testInitBadTransactionManager(self):
        try:
            QueueTransporter(self.qTransport, None, self, self, self._logger)
        except AssertionError, _e:
            assert True
        else:
            assert False
    def testTransportStateChangeEmitExceptionHandlerCorrectly(self):
        class MyException(Exception): pass
        self.stateChangeResult = MyException("d'oh!")
        qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        try:
            qt._emitTransportStateChange("hello world!")
        except MyException, _e:
            assert True
        else:
            assert False
    def testTransportStateChangeEmitExceptionHandlerCorrectlyNoListener(self):
        class MyException(Exception): pass
        eMsg = "d'oh!"
        eResult = MyException(eMsg)
        self.stateChangeResult = eResult
        qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        try:
            qt._emitTransportStateChange("hello world!")
        except MyException, e:
            assert e.message == eMsg
        else:
            assert False
    def testTransportDataReceiveEmitExceptionHandlerCorrectly(self):
        class MyException(Exception): pass
        self.dataReceiveResult = MyException("d'oh!")
        qt = QueueTransporter(self.qTransport, self.tm, self, self, self._logger)
        try:
            qt._emitTransportDataReceive(123, "hello world!")
        except MyException, _e:
            assert True
        else:
            assert False
    def testTransportDataReceiveEmitExceptionHandlerCorrectlyNoListener(self):
        class MyException(Exception): pass
        self.dataReceiveResult = MyException("d'oh!")
        qt = QueueTransporter(self.qTransport, self.tm)
        try:
            qt._emitTransportDataReceive(123, "hello world!")
        except NoResponseRequired, _e:
            assert True
        else:
            assert False

class TestHeadQueueTransporter(unittest.TestCase, iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener):
    def setUp(self):
        self._logger = LogManager().getLogger(self.__class__.__name__)
        self.qTransport = QueueTransportDetails()
        self.tm = TransactionManager()
        self.qt = HeadQueueTransporter(self.qTransport, self.tm, i_ipc_transport_state_change_listener=self, i_ipc_transport_data_receive_listener=self)
        self.result = None
    def tearDown(self):
        try:    self.qt.close()
        except: pass
    def transportStateChange(self, e_ipc_transport_state):
        pass
    def transportDataReceive(self, tId, data):
        result = self.result
        if isinstance(result, Exception):
            raise result
        return result
    def testExceptionHandledCorrectly(self):
        eMessage = "hello world!"
        self.result = Exception(eMessage)
        try:
            self.qt._emitTransportDataReceive(123, "data")
        except NoResponseRequired, _e:
            assert True
        else:
            assert False
    def testReturnHandledCorrectly(self):
        self.result = "hello world!"
        try:
            self.qt._emitTransportDataReceive(123, "data")
        except NoResponseRequired, _e:
            assert True
        else:
            assert False

class TestAQueueTransporterAtEachEndWithAlgo(unittest.TestCase):
    def setUp(self):
        self._logger = LogManager().getLogger(self.__class__.__name__)
        self.eFormats = {}
        eF = []
        eF.append(iAlgoImpl.FORMAT_ID__ALGO)
        eF.append(iEncryptor.FORMAT_ID__ENCRYPTOR)
        eF.append(NoEncryption.FORMAT_ID__PASSTHROUGH_ENCRYPTION)
        eF.append(iAlgoImpl.FORMAT_ID__ALGO)
        eF.append(iCompressor.FORMAT_ID__COMPRESSOR)
        eF.append(ZlibCompressor.FORMAT_ID__ZLIB_COMPRESSOR)
        self.eFormats["None"] = ".".join(eF)
        ConfigurationManager.destroySingleton()
        config = ConfigurationManager(cwd="config/ipc_algo").getConfiguration("b").configuration.ipc
        compression = config.compression
        encryption = config.encryption
        self.qTransport = QueueTransportDetails(compression, encryption)
        invertedTransport = self.qTransport.invert()
        self.neck = MyReceiver(QueueTransporter, self.qTransport, NeckTransactionIdGenerator(), logger=LogManager().getLogger("Neck"))
        self.head = MyReceiver(HeadQueueTransporter, invertedTransport, HeadTransactionIdGenerator(), logger=LogManager().getLogger("Head"))
        f = self.neck.qt._algo.getFormat()
        assert f == self.eFormats["None"]
    def tearDown(self):
        self._logger.debug("teardown...")
        self.data = []
        self.state = []
        time.sleep(1)
        self.tm = None
        self.neck.qt.close(ignoreErrors=True)
        self.head.qt.close(ignoreErrors=True)
        self.qTransport.del_qRx()
        self.qTransport.del_qTx()
    def testRoundTripSolicited(self):
        self.head.qt.connect()
        self.neck.qt.connect()
        tIds = []
        for i in range(0, 10):
            k = (i + 1)
            COMMAND = "a"
            tId = self.head.qt.sendData(COMMAND, solicited=True)
            assert tId
            assert tId not in tIds
            tIds.append(tId)
            #    Now check NO data received by listener:
            l = len(self.head.data)
            assert l == 0, "Got: %(L)s" % {"L":l}
            #    Now check the transaction data:
            data = self.head.tm.acquireNew(tId, 5)
            eData = MyReceiver.cmdResultMapping[COMMAND]
            assert data == eData, "Got: %(D)s" % {"D":data}
            #    Now check data received by Neck:
            l = len(self.neck.data)
            assert l == k, "Got: %(L)s" % {"L":l}
            assert self.neck.data[i][0] == tId, "Got: %(D)s" % {"D":self.neck.data[i][0]}
            assert self.neck.data[i][1] == COMMAND, "Got: %(D)s" % {"D":self.neck.data[i][1]}

if __name__ == '__main__':
    unittest.main()
