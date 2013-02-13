
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface
import pickle

class iIpcTransport(Interface):
    r"""
    @summary: The interface that the transport mechanisms must expose.
    @attention: Transport mechanisms have conceptual 'channels' over 
    which the data is transmitted and received.
    @attention: This interface is NOT thread-safe.
    """
    def __init__(self, transport, transactionManager, i_ipc_transport_state_change_listener=None, i_ipc_transport_data_receive_listener=None, logger=None):
        r"""
        @summary: Constructor. No transport actions to be performed.
        @param i_ipc_listener: Listener to receive TransportStateChange and TransportDataReceive events.
        @param transport: Transport specific parameters.
        @param transactionManager: The pr-econfigured TransactionManaager to use.
        @param logger: A logger to use, if not specified one will be created.
        @raise Exception: error when closing transport.
        """
        raise NotImplementedException("iIpcTransport.__init__")
    def close(self, ignoreErrors=False, noCallback=True):
        r"""
        @summary: Immediately close the transport channels.
        @attention: When the call returns, the channels are closed.
        @param ignoreErrors: True - no exception raised on error, False - otherwise.
        @param noCallback: True - no calls to iIpcTransportListener, False - otherwise.
        @return: True - transport closed.
        @raise Exception: error when closing transport.
        @raise TransportFinishedError: Transport terminally broken.
        @raise TransportDisconnectedError: Transport is disconnected.
        """
        raise NotImplementedException("iIpcTransport.close")
    def disconnect(self, timeout=None, solicited=False, noCallback=True):
        r"""
        @summary: Disconnect the transport channels.
        @attention: When the call returns, the channels are disconnected.
        @param timeout: Timeout is seconds in which to perform the disconnection.
        @param solicited: True - send by the Head, False - sent by the Neck.
        @param noCallback: True - don't trigger any iIpcTransportListener callbacks, False - otherwise.
        @raise TransportFinishedError: Transport terminally broken.
        @raise TransportDisconnectedError: Transport is disconnected.
        """
        raise NotImplementedException("iIpcTransport.disconnect")
    def isFinished(self):
        r"""
        @summary: A predicate of whether the Transport is irrecoverably finished.
        @return: True - Finished, False - otherwise.
        """
        raise NotImplementedException("iIpcTransport.isFinished")
    def isConnected(self):
        r"""
        @summary: A predicate of whether the Transport is connected.
        @return: True - Connected, False - otherwise.
        """
        raise NotImplementedException("iIpcTransport.isConnected")
    def connect(self, timeout=None):
        r"""
        @summary: Immediately connect the transport channels.
        @attention: When the call returns, the channels are connected.
        @param timeout: Timeout is seconds to make the connection. None==infinite timeout.
        @raise ConnectionTimeoutError: Transport connection timed-out.
        @raise TransportFinishedError: Transport terminally broken.
        @raise TransportDisconnectedError: Transport is disconnected.
        @attention: No calls to iIpcTransportListener are made.
        """
        raise NotImplementedException("iIpcTransport.connect")
    def sendData(self, data, solicited=True, transactionId=None, callback=None):
        r"""
        @summary: Send data through the transport channels.
        @param data: The data to send. The data is subsequently encapsulated within a IpcDataMessage.
        @param solicited: True - is assigned a transactionId if one is not provided, False - existing transactionId is used.
        @param transactionId: The unique id associated with this data. Can be None.
        @param callback: The callback to be called when the transaction completes.
        @raise TransportFinishedError: Transport terminally broken.
        @raise TransportDisconnectedError: Transport is disconnected.
        """
        raise NotImplementedException("iIpcTransport.sendData")
    def sendRaw(self, data):
        r"""
        @summary: Send raw data through the transport channels. The data is not encapsulated.
        @param data: The data to send.
        @raise TransportFinishedError: Transport terminally broken.
        @raise TransportDisconnectedError: Transport is disconnected.
        """
        raise NotImplementedException("iIpcTransport.send")
    def getTransactionManager(self):
        r"""
        @summary: Return the current TransactionManager.
        """
        raise NotImplementedException("iIpcTransport.getTransactionManager")
    def setTransportStateChangeListener(self, listener):
        r"""
        @summary: Register a listener for Transport StateChange events.
        """
        raise NotImplementedException("iIpcTransport.setTransportStateChangeListener")
    def setTransportDataReceiveListener(self, listener):
        r"""
        @summary: Register a listener for Transport DataReceive events.
        """
        raise NotImplementedException("iIpcTransport.setTransportDataReceiveListener")
    def getTransportStateChangeListener(self):
        r"""
        @summary: Retrieve the listener for Transport StateChange events.
        """
        raise NotImplementedException("iIpcTransport.getTransportStateChangeListener")
    def getTransportDataReceiveListener(self):
        r"""
        @summary: Retrieve the listener for Transport DataReceive events.
        """
        raise NotImplementedException("iIpcTransport.getTransportDataReceiveListener")
    @staticmethod
    def testPickleability(signal, logger):
        try:
            return pickle.dumps(signal)
        except Exception, _e:
            logger.exception("Can't pickle signal type %(T)s: %(S)s" % {"T":type(signal), "S":signal})
            raise



