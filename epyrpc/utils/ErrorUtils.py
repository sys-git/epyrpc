import traceback
import threading

def getTraceback(e):
    """
    @summary: Get remote RPyC traceback, if not then get local traceback.
    @return: String representation of traceback.
    """
    if e and hasattr(e, "_remote_tb"):
        return e._remote_tb
    return traceback.format_exc()

def importModule(where, what):
    _module = __import__(where, globals(), locals(), [what], -1)
    _type = getattr(_module, what)
    return _type

def getCurrentThreads():
    s = ["Active thread count: %(N)s" % {"N":threading.activeCount()}]
    for i, thr in enumerate(threading.enumerate()):
        s.append("Thread[%(I)s] = %(THR)s" % {"I":i, "THR":thr})
    return "\r\n".join(s)
