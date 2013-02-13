
from Queue import Full, Empty
from epyrpc.core.IpcExceptions import NoResponseRequired, TransportFinishedError, \
    TransportDisconnectedError, NoData
from epyrpc.core.transport.algos.TransportDataAlgoFactory import \
    TransportDataAlgoFactory
from epyrpc.core.transport.eIpcTransportState import eIpcTransportState
from epyrpc.core.transport.iIpcTransport import iIpcTransport
from epyrpc.core.transport.iIpcTransportListener import \
    iIpcTransportStateChangeListener, iIpcTransportDataReceiveListener
from epyrpc.core.transport.messages.IpcDataMessage import IpcDataMessage
from epyrpc.core.transport.messages.IpcTransportMessage import \
    IpcTransportMessage
from epyrpc.core.transport.messages.eIpcTransportCommand import \
    eIpcTransportCommand
from epyrpc.core.transport.queue.QueueObject import QueueObject
from epyrpc.utils.ErrorUtils import getCurrentThreads
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.synchronisation.TransactionFailed import TransactionFailed
from multiprocessing import Value
from threading import Semaphore
import pickle
import sys
import threading
import time
# import pydevd

def teardown_module():
    sys.stderr.write(getCurrentThreads() + "\r\n")

class TransportFinished(Exception):
    def __init__(self, connectedState, finishedState):
        self.connectedState = connectedState
        self.finishedState = finishedState

class QueueTransporter(iIpcTransport):
    def __init__(self, transportDetails, transactionManager, i_ipc_transport_state_change_listener=None, i_ipc_transport_data_receive_listener=None, logger=None):
        assert transportDetails
        assert transactionManager
        self._receiver = None
        self.setTransportStateChangeListener(i_ipc_transport_state_change_listener)
        self.setTransportDataReceiveListener(i_ipc_transport_data_receive_listener)
        self._transportDetails = transportDetails
        self._algo = TransportDataAlgoFactory.get(self._transportDetails.packager())
        self._connected = Value('d', 0)
        self._finished = Value('d', 0)
        if logger == None:
            logger = LogManager().getLogger(self.__class__.__name__)
        self._logger = logger
        self._transactionManager = transactionManager
        self.setDebugHandler()
    def setDebugHandler(self, handler=None):
        self._debugHandler = handler
    def getTransactionManager(self):
        return self._transactionManager
    def setTransportStateChangeListener(self, listener):
        if listener != None:
            if not isinstance(listener, iIpcTransportStateChangeListener):
                raise ValueError(listener)
        if hasattr(self, "_stateChangeListener") and self._stateChangeListener == listener:
            self._stateChangeListener = None
        else:
            self._stateChangeListener = listener
    def getTransportStateChangeListener(self):
        return self._stateChangeListener
    def setTransportDataReceiveListener(self, listener):
        if listener != None:
            if not isinstance(listener, iIpcTransportDataReceiveListener):
                raise ValueError(listener)
        if hasattr(self, "_dataReceiveListener") and self._dataReceiveListener == listener:
            self._dataReceiveListener = None
        else:
            self._dataReceiveListener = listener
    def getTransportDataReceiveListener(self):
        return self._dataReceiveListener
    def _onClosed(self):
        return self._emitTransportStateChange(eIpcTransportState.CLOSED)
    def _onConnected(self):
        return self._emitTransportStateChange(eIpcTransportState.OPEN)
    def _onDisconnected(self):
        return self._emitTransportStateChange(eIpcTransportState.DISCONNECTED)
    def _onReceive(self, tId, data):
        return self._emitTransportDataReceive(tId, data)
    def _emitTransportStateChange(self, state):
        if self._stateChangeListener != None:
            try:
                return self._stateChangeListener.transportStateChange(state)
            except Exception, _e:
                cmd = eIpcTransportState.enumerateAttributes(state, catchall=True)
                self._logger.exception("listener exception when handling transportStateChange(%(C)s)" % {"C":cmd})
                raise
    def _emitTransportDataReceive(self, tId, data):
        if self._dataReceiveListener != None:
            try:
                return self._dataReceiveListener.transportDataReceive(tId, data)
            except NoResponseRequired, _e:
                raise
            except Exception, _e:
                self._logger.debug("listener exception when handling transportDataReceive(%(C)s)." % {"C":(tId, data)})
                raise
        #    If no listener then no response is required because it cannot be actioned!
        raise NoResponseRequired(tId)
    def close(self, ignoreErrors=False, noCallback=True):
        try:
            self.disconnect(solicited=False, noCallback=noCallback)
            if self._receiver:
                self._logger.warn("Joining with receiver thread...")
                self._receiver.join()
        except Exception, _e:
            if ignoreErrors == False:
                raise
        self._logger.warn("closed!")
        return True
    def _close(self, noCallback=False, local=True):
        self._logger.warn("_close...")
        self._connected.value = 0
        self._finished.value = 1
        self._logger.warn("_close 1...")
        self._transportDetails.del_qTx()
        self._logger.warn("_close 2...")
        self._transportDetails.del_qRx()
        self._logger.warn("_close 3...")
        if not noCallback:
            self._onDisconnected()
        #    Now trigger any synchronised callers:
        self._transactionManager.releaseAll(TransportFinishedError())
        if not noCallback:
            self._onClosed()
        self._logger.warn("_close 4...")
    def disconnect(self, timeout=None, solicited=False, noCallback=True):
        self._logger.warn("disconnect 1...")
        if self.isFinished():
            raise TransportFinishedError()
        #    Tell the other side about the disconnection request.
        transactionId = None
        if solicited:
            transactionId = self._transactionManager.create()
        data = IpcTransportMessage(eIpcTransportCommand.DISCONNECT, tId=transactionId)
        self._logger.warn("disconnect 2...")
        try:
            self.sendRaw(data)
        except (TransportFinishedError, TransportDisconnectedError), _e:
            #    Disconnected.
            pass
        else:
            #    Wait for the disconnection response (if solicited).
            if transactionId != None:
                try:
                    result = self._transactionManager.acquireNew(transactionId, timeout=timeout, purge=True)
                except TransactionFailed, _e:
                    #    Disconnect failed in the given timeout, close from this side.
                    pass
                else:
                    if result.command == eIpcTransportCommand.DISCONNECTED:
                        #    Successful disconnection.
                        pass
                    else:
                        #    Failed graceful disconnection
                        pass
        self._logger.warn("disconnect 3...")
        self._close(noCallback=noCallback, local=True)
        self._logger.warn("disconnect 4...")
    def isFinished(self):
        return self._finished.value == 1
    def isConnected(self):
        if (self._connected.value == 1):
            try:
                return (not self._transportDetails.isqTxClosed()) and (not self._transportDetails.isqRxClosed())
            except:
                #    Queues have been deleted!
                return False
        return False
    def connect(self, timeout=None, noCallback=True):
        return self._connect(timeout=timeout, noCallback=noCallback)
    def _connect(self, timeout=None, noCallback=False):
        if self.isFinished():
            raise TransportFinishedError()
        try:
            isDisconnected = (self._transportDetails.isqRxClosed()) or (self._transportDetails.isqTxClosed())
        except:
            isDisconnected = True
        if isDisconnected:
            #   Queue(s) have been closed - this means finished for a Queue!
            self._close(noCallback=True, local=True)
            raise TransportDisconnectedError("connect() check")
        self._doConnect()
        if noCallback == False:
            self._onConnected()
    def _doConnect(self):
        lck = Semaphore(0)
        t = threading.Thread(target=self._doReceive, args=[lck])
        t.setDaemon(True)
        t.setName(self.__class__.__name__ + "_Rx")
        t.start()
        lck.acquire()
        self._receiver = t
    def sendData(self, data, solicited=True, transactionId=None, callback=None):
        self._logger.debug("SendData: ('%(T)s' - '%(D)s')" % {"T":transactionId, "D":data})
        if self.isFinished():
            raise TransportFinishedError()
        if not self.isConnected():
            raise TransportDisconnectedError()
        #    Send a non-transport message, either solicited or unsolicited:
        cmd = IpcDataMessage(data)
        if solicited:
            if transactionId == None:
                transactionId = self._transactionManager.create(callback=callback)
        #    Set the transactionId into the packet:
        cmd.tId = transactionId
        self.sendRaw(cmd)
        return transactionId
    def sendRaw(self, data):
        if self.isFinished():
            raise TransportFinishedError()
        if not self.isConnected():
            raise TransportDisconnectedError()
        self._logger.debug("sendRaw: '%(D)s'" % {"D":data})
        #    Attempt to pickle the object, fail immediately if not possible:
        data = iIpcTransport.testPickleability(data, self._logger)
        #    Now package the data ready for the channel:
        data = QueueObject(self._algo.package(data), self._algo.getFormat())
        try:
            #    Send the packet:
            self._transportDetails.qTx().put(data, block=False)
        except (Full, AssertionError, AttributeError), e:
            #   Queue has been closed - this means finished for a Queue!
            self._close(noCallback=True, local=True)
            raise TransportDisconnectedError(e)
    def _receiveRaw(self, block=True, timeout=None):
        if self.isFinished():
            raise TransportFinishedError()
        if not self.isConnected():
            raise TransportDisconnectedError()
        try:
            data = self._transportDetails.qRx().get(block=block, timeout=timeout)
        except (EOFError, AttributeError), _e:
            self._logger.warn("queue has been deleted!")
            raise TransportDisconnectedError("_receiveRaw - AttributeError")
        except IOError, e:
            if e.errno == 9:
                #    Queue has been remotely closed.
                self._logger.warn("queue has been remotely closed!")
                raise TransportDisconnectedError("_receiveRaw - IOError #9")
            if e.errno == 4:
                self._logger.exception("InterruptedSystemCall exception when _receiveRaw - ignoring!")
        except Empty, _e:
#            self._logger.warn("No data!")
            raise NoData(_e)
        except Exception, e:
            self._logger.exception("Unknown error when _receiveRaw.")
        else:
            self._logger.debug("_receiveRaw: '%(D)s'" % {"D":data})
            hint = data.getFormat()
            data = data.data()
            #    Now extract the data from the channel:
            data = self._algo.extract(data, hint=hint)
            #    Now unpickle the data:
            data = pickle.loads(data)
            return data
    def _checkIsFinished(self):
        connected = self.isConnected()
        finished = self.isFinished()
        if ((not connected) or (finished)):
            raise TransportFinished(connected, finished)
    def _doReceive(self, lck):
        self._connected.value = 1
        lck.release()
        self._logger.debug("thread running...")
        try:
            #    Receiver now running:
            while True:
                try:
                    data = self._receiveRaw(timeout=1)
                except (TransportFinishedError, TransportDisconnectedError), e:
                    #    Disconnected, exit receiver loop.
                    self._logger.warn("transport disconnected...")
                    break
                except NoData, _e:
                    self._checkIsFinished()
                else:
                    if data == None:
                        self._checkIsFinished()
                        continue
#                    pydevd.settrace(stdoutToServer = True, stderrToServer = True)
                    self._logger.debug("received raw message: '%(D)s'" % {"D":data})
                    tId = data.tId
                    self._logger.debug("received msg for tId: '%(T)s'" % {"T":tId})
                    if isinstance(data, IpcTransportMessage):
                        cmd = data.command()
                        self._logger.debug("received command: '%(D)s'" % {"D":cmd})
                        if cmd == eIpcTransportCommand.DISCONNECT:
                            self._logger.debug("disconnect requested.")
                            #    Remote disconnection required.
                            if tId != None:
                                self._logger.debug("disconnect requested from 'other' side...")
                                #    Remote disconnection requires a response!
                                rtn = IpcTransportMessage(eIpcTransportCommand.DISCONNECTED, tId=tId)
                                self.sendRaw(rtn)
                                #    Allow the response to get back to the caller.
                                time.sleep(1)
                                self._logger.debug("disconnect response sent.")
                            self._close(noCallback=False, local=False)
                        else:
                            #    Tell the synchroniser about the message:
                            self._transactionManager.release(tId, data.command())
                            self._logger.debug("transaction '%(T)s' released" % {"T":tId})
                    elif isinstance(data, IpcDataMessage):
                        msg = data.message()
                        self._logger.debug("received data: '%(D)s'" % {"D":msg})
                        #    If the message is part of our transaction then tell the synchroniser:
                        if self._transactionManager.isValidTransactionId(tId):
                            self._logger.debug("releasing transaction: %(I)s..." % {"I":tId})
                            self._transactionManager.release(tId, msg)
                        else:
                            self._logger.debug("calling onReceive...")
                            try:
                                rtn = self._onReceive(tId, msg)
                            except NoResponseRequired, _e:
                                #    No response is required.
                                self._logger.debug("no response required!")
                                continue
                            except Exception, e:
                                #    exception needs propagating.
                                self._logger.debug("Exception response!")
                                rtn = e
                            #    Now return the response (exception or otherwise):
                            if tId != None:
                                self.sendData(rtn, solicited=True, transactionId=tId)
                    self._checkIsFinished()
        except (TransportFinishedError, TransportDisconnectedError, TransportFinished), _e:
            #    Received finishing naturally or deliberately:
            self._logger.warn("TransportFinished")
        except Exception, e:
            #    Unexpected error in thread!
            self._logger.exception("Unexpected error in thread.")
        #    Receiver finished!
        self._logger.warn("thread finished!")

