
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface

class iIpcTransportStateChangeListener(Interface):
    r"""
    @summary: Anything controlling an instance of iIpcTransport MUST implement this interface.
    """
    def __init__(self, *args, **kwargs):
        pass
    def transportStateChange(self, e_ipc_transport_state):
        r"""
        @summary: The connection state of the IPC has changed.
        @param e_ipc_transport_state: The new state of the Ipc transport.
        @see: eIpcTransportState.
        @attention: When the state changes to disconnected, all the transaction listeners are released with TransportFinishedError().
        @attention: This is never called if the connection state changes as a direct result of a call to iIpcTransport (connect, disconnect, etc).
        """
        raise NotImplementedException("iIpcTransportListener.transportStateChange")

class iIpcTransportDataReceiveListener(Interface):
    r"""
    @summary: Anything controlling an instance of iIpcTransport MUST implement this interface.
    """
    def __init__(self, *args, **kwargs):
        pass
    def transportDataReceive(self, tId, data):
        r"""
        @summary: New data has been received from the other side of the Ipc.
        @param tId: The transactionId for this data (if applicable).
        @param data: The raw data received. type=IpcMessageBase.
        @return: A return value to be returned to the other side of the Ipc.
        @attention: If synchronous==True, the return value should be send through the IPC via a sendData(tId=tId).
        @attention: The return value will be encapsulated within a IpcDataMessage.
        @raise NoResponseRequired: No return value should be sent to the other side of the Ipc.
        """
        raise NotImplementedException("iIpcTransportListener.transportDataReceive")
