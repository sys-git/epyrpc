
from YouView.TAS.Common.SignalExchangeHub.Listener import Listener
from decimal import Decimal
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iLocation import iLocation
from epyrpc.exceptions.NotImplemented import NotImplementedException
from epyrpc.utils.Interfaces import Interface
from multiprocessing.synchronize import RLock
import os
import shutil
import time

class iArchiver(Interface):
    def close(self):
        raise NotImplementedException("iArchiver.close")
    def getFormat(self):
        raise NotImplementedException("iArchiver.getFormat")
    def signal(self, timestamp, payload, ns, desc):
        raise NotImplementedException("iArchiver.signal")
    def retrieve(self, i_range):
        raise NotImplementedException("iArchiver.retrieve")
    def _shouldRetrieve(self, timestamp, start, end):
        raise NotImplementedException("iArchiver._shouldRetrieve")

class MemoryArchiver(iArchiver):
    def __init__(self):
        self._signals = []
        self._closed = False
        #    FIXME: Remove this:
        for i in range(0, 1000):
            self._signals.append((os.getpid(), time.time(), {}, "ns_%(I)s" % {"I":i}, "nothing_%(I)s" % {"I":i}))
    def close(self):
        self._closed = True
    def getFormat(self):
        return iLocation.MEMORY
    def signal(self, timestamp, payload, ns, desc):
        if self._closed == True:
            return
        self._signals.append((os.getpid(), timestamp, payload, ns, desc))
    def __del__(self):
        self._signals = []
    def retrieve(self, i_range):
        result = []
        if i_range:
            try:
                start = i_range.start().time()
            except:
                start = None
            try:
                end = i_range.end().time()
            except:
                end = None
        else:
            start = end = None
        for signal in self._signals:
            (_pid, timestamp, _payload, _ns, _desc) = signal
            if self._shouldRetrieve(timestamp, start, end):
                result.append(signal)
        return result
    def _shouldRetrieve(self, timestamp, start=None, end=None):
        if start:
            if timestamp < start:
                return False
        if end:
            if timestamp > end:
                return False
        return True

class FileArchiver(iArchiver):
    HEADER = "Archived signals in text format...Timestamp, Namespace, Description:\r\n\r\n"
    def __init__(self, filename):
        self._filename = os.path.realpath(filename)
        if os.path.exists(self._filename):
            os.remove(self._filename)
        self._openFile()
        self._writeHeader()
    def _openFile(self):
        self._fp = open(self._filename, "w+b")
    def close(self):
        self._closeFile()
    def _closeFile(self):
        if self._fp:
            try:
                self._fp.write("\r\nClosed.\r\n")
                self.fp.close()
            except Exception, _e:
                pass
            self.fp = None
    def _writeHeader(self):
        self._fp.write(self.HEADER)
    def __del__(self):
        self._closeFile()
    def getFormat(self):
        return iLocation.FILE
    def signal(self, timestamp, payload, ns, desc):
        ts = time.strftime("%%Y-%%m-%%d %%H:%%M:%%S.%(MS)s" % {"MS":str(Decimal(timestamp)).split(".")[1][:6]}, time.localtime(timestamp))
        s = [ts]
        s.append("%(P)s" % {"P":os.getpid()})
        s.append(ns)
        s.append(desc)
        ss = ",\r\n".join(s) + "\r\n"
        if self._fp:
            self._fp.write(ss)
            self._fp.flush()
    def reconfigure(self, i_location):
        filename = os.path.realpath(i_location.filename())
        if filename == self._filename:
            return True
        existingFilename = self._filename
        copyExisting = i_location.copyExisting()
        if copyExisting == True:
            shutil.copy(existingFilename, filename)
        self._openFile()
        if copyExisting == False:
            self._writeHeader()
        removeExisting = i_location.removeExisting()
        if removeExisting == True:
            os.remove(existingFilename)
        return True
    def retrieve(self, i_range):
        #    FIXME: TODO: Implement this!
        return []

class SignalMonitorArchiver(object):
    _instance = None
    _instanceLock = RLock()
    def __init__(self, parent, i_location=None):
        self._parent = parent
        self._config = i_location
        self._impl = None
        self._setup()
    def start(self):
        self._listener = Listener("*", self._onReceive)
        self._parent.seh().addListener(self._listener)
    def stop(self):
        self._parent.seh().removeListener(self._listener)
        self._impl.close()
    def _onReceive(self, signal):
        payload = signal.getPayload()
        ns = signal.getNamespace()
        timestamp = signal.getTimestamp()
        desc = str(signal)
        if self._impl:
            try:
                self._impl.signal(timestamp, payload, ns, desc)
            except Exception, _e:
                pass
    def reconfigure(self, i_location):
        if self._impl and self._impl.getFormat() == i_location.theFormat():
            return self._impl.reconfigure(i_location)
        else:
            self._impl.close()
            self._impl = None
            self._config = i_location
            return self._setup()
    def retrieve(self, i_range):
        return self._impl.retrieve(i_range)
    def _setup(self):
        #    configure ourselves.
        if self._impl == None:
            self._impl = self._getImpl(self._config)
            return True
    @staticmethod
    def _getImpl(config):
        f = config.theFormat()
        if f == iLocation.FILE:
            filename = config.filename()
            return FileArchiver(filename)
        elif f == iLocation.MEMORY:
            return MemoryArchiver()
        raise ValueError("Unsupported archive format: %(F)s." % {"F":f})





