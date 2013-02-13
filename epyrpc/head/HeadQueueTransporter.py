from epyrpc.core.IpcExceptions import NoResponseRequired
from epyrpc.core.transport.queue.QueueTransporter import QueueTransporter

class HeadQueueTransporter(QueueTransporter):
    r"""
    The Head never returns data to the Neck.
    """
    def __init__(self, *args, **kwargs):
        super(HeadQueueTransporter, self).__init__(*args, **kwargs)
    def _emitTransportDataReceive(self, tId, data):
        if self._dataReceiveListener == None:
            return
        try:
            self._dataReceiveListener.transportDataReceive(tId, data)
        except NoResponseRequired, e:
            raise
        except Exception, e:
            self._logger.exception("listener exception when handling transportDataReceive(%(C)s)" % {"C":(tId, data)})
            raise NoResponseRequired(tId, e)
        raise NoResponseRequired(tId)
