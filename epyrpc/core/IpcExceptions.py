
class IpcException(Exception): pass

class TransportStateError(IpcException): pass

class TransportClosedError(TransportStateError):
    def __str__(self):
        return "TransportClosed %(S)s" % {"S":super(TransportDisconnectedError, self).__str__()}

class TransportDisconnectedError(TransportStateError):
    def __str__(self):
        return "TransportDisconnected %(S)s" % {"S":super(TransportDisconnectedError, self).__str__()}

class TransportFinishedError(TransportStateError):
    def __str__(self):
        return "TransportFinished %(S)s" % {"S":super(TransportFinishedError, self).__str__()}

class ConnectionTimeoutError(TransportStateError):
    def __str__(self):
        return "ConnectionTimeout %(S)s" % {"S":super(ConnectionTimeoutError, self).__str__()}

class NoData(IpcException): pass

class NoResponseRequired(IpcException):
    def __init__(self, nsPrefix, e=None):
        eStr = ""
        if e != None:
            m = e.message
            if m and (len(m) > 0):
                eStr = m
            else:
                eStr = str(e)
        msg = "%(NSP)s" % {"NSP":nsPrefix, "E":eStr}
        super(NoResponseRequired, self).__init__(msg)
