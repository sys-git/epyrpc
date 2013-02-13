
from epyrpc.core.transport.messages.IpcMessageBase import IpcMessageBase
from epyrpc.core.transport.messages.eIpcTransportCommand import \
    eIpcTransportCommand

class IpcTransportMessage(IpcMessageBase):
    r"""
    @summary: All connection related messages ride in this car.
    """
    def __init__(self, e_ipc_transport_command, tId=None):
        r"""
        @summary: e_ipc_transport_command: The transport command.
        @see: eIpcTransportCommand
        """
        super(IpcTransportMessage, self).__init__(tId)
        self._command = e_ipc_transport_command
    def command(self):
        return self._command
    def __str__(self):
        s = ["IpcTransportMessage[%(TID)s]" % {"TID":self.tId}]
        s.append("%(M)s" % {"M":eIpcTransportCommand.enumerateAttributes(self._command)})
        return " ".join(s)
