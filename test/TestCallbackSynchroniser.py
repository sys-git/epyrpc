
from epyrpc.synchronisation.CallbackSynchroniser import CallbackSynchroniser
from epyrpc.utils.synchronisation.Synchroniser import Synchroniser
from epyrpc.utils.synchronisation.TransactionFailed import TransactionFailed
import threading
import unittest

class testCallbackSynchroniser(unittest.TestCase):
    def setUp(self):
        self.eResult = "hello.world!"
        self._timers = []
    def tesNoGeneratorSpecified(self):
        try:
            self.cbs = CallbackSynchroniser()
        except:
            assert True
        assert False, "Expecting an exception to have been raised!"
    def testCallbackItemCallsCallback(self):
        self.cbCalled = False
        self.theResult = None
        self.cbI = None
        def cb(i, result=None):
            self.cbI = i
            self.cbCalled = True
            self.theResult = result
        i = 0
        item = CallbackSynchroniser.CallbackItem(i, cb)
        item.result(self.eResult)
        assert self.cbI == i
        assert self.cbCalled == True, "cb not called!"
        assert self.theResult == self.eResult, "unexpected result: %(T)s" % {"T":self._theResult}
    def testResultCallsCallback(self):
        self.cbCalled = False
        self.theResult = None
        self.cbI = None
        def cb(i, result=None):
            self.cbI = i
            self.cbCalled = True
            self.theResult = result
        tm = CallbackSynchroniser()
        tId = tm.create(callback=cb)
        tm.release(tId, self.eResult)
        assert self.cbCalled == True, "cb not called!"
        assert self.theResult == self.eResult, "unexpected result: %(T)s" % {"T":self._theResult}
    def testAcquireWithCallbackRaisesTypeError(self):
        self.cbCalled = False
        self.theResult = None
        self.cbI = None
        def cb(i, result=None):
            self.cbI = i
            self.cbCalled = True
            self.theResult = result
        tm = CallbackSynchroniser()
        tId = tm.create(callback=cb)
        try:
            tm.acquireNew(tId)
        except TypeError, _e:
            assert True
        else:
            assert False, "Expecting a TypeError to be thrown!"
    def testAcquireWithNoCallbackStillWorksWithTimeout(self):
        self.theResult = None
        tm = CallbackSynchroniser()
        tId = tm.create()
        try:
            tm.acquireNew(tId, timeout=1)
        except TransactionFailed, _e:
            assert True
        else:
            assert False, "Expecting a TransactionFailed to have been raised!"
    def testAcquireWithNoCallbackStillWorksWithNoTimeout(self):
        tm = CallbackSynchroniser()
        tId = tm.create()
        t = threading.Timer(1, self._releaseResult, args=[tm, tId, self.eResult])
        self._timers.append(t)
        t.start()
        result = tm.acquireNew(tId)
        assert result == self.eResult, "Unexpected result received: %(R)s, expecting: %(E)s" % {"R":result, "E":self.eResult}
    def _releaseResult(self, tm, tId, result):
        tm.release(tId, result)
    def tearDown(self):
        for t in self._timers:
            t.cancel()
        self._timers = []
    def testItemIsOfCorrectTypeWhenCallback(self):
        self.correctType = False
        class MyCallbackSynchroniser(CallbackSynchroniser):
            def __init__(self):
                super(MyCallbackSynchroniser, self).__init__()
                self.correctType = False
            def _getItem(self, i, callback=None):
                self.correctType = True
                return super(MyCallbackSynchroniser, self)._getItem(i, callback)
        tm = MyCallbackSynchroniser()
        def cb():
            pass
        tm.create(callback=cb)
        assert tm.correctType == True, "Failed to get the correct Item type!"
    def testItemIsOfCorrectTypeWhenNotCallback(self):
        self.correctType = False
        class MyCallbackSynchroniser(CallbackSynchroniser):
            def __init__(self):
                super(MyCallbackSynchroniser, self).__init__()
                self.correctType = False
            def _getItem(self, i, callback=None):
                result = super(MyCallbackSynchroniser, self)._getItem(callback)
                if isinstance(result, Synchroniser.Item):
                    self.correctType = True
                return result
        tm = MyCallbackSynchroniser()
        tm.create()
        assert tm.correctType == True, "Failed to get the correct Item type!"

if __name__ == '__main__':
    unittest.main()
