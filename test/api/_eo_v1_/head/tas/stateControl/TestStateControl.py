
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.head.tas.StateControl import StateControl
from epyrpc.api.iApiAction import iApiAction
import unittest

class TestInit(unittest.TestCase):
    def setUp(self):
        self.sc = StateControl("me")
    def testWithArgs(self):
        try:
            self.sc.init(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.sc.init(), iApiAction)

class TestTerminate(unittest.TestCase):
    def setUp(self):
        self.sc = StateControl("me")
    def testWithArgs(self):
        try:
            self.sc.terminate(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.sc.terminate(), iApiAction)

class TestRun(unittest.TestCase):
    def setUp(self):
        self.sc = StateControl("me")
    def testWithArgs(self):
        try:
            self.sc.run(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.sc.run(), iApiAction)

class TestPause(unittest.TestCase):
    def setUp(self):
        self.sc = StateControl("me")
    def testWithArgs(self):
        try:
            self.sc.pause(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.sc.pause(), iApiAction)

class TestPauseAtEnd(unittest.TestCase):
    def setUp(self):
        self.sc = StateControl("me")
    def testWithArgs(self):
        try:
            self.sc.pauseAtEnd(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.sc.pauseAtEnd(), iApiAction)

class TestStop(unittest.TestCase):
    def setUp(self):
        self.sc = StateControl("me")
    def testNoArgs(self):
        assert isinstance(self.sc.stop(), iApiAction)
    def testWithArgsIsNone(self):
        try:
            self.sc.stop(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testWithArgsValidEmptyArgs(self):
        try:
            self.sc.stop({})
        except TypeError, _e:
            assert True
        else:
            assert False
    def testWithArgsValidPopulatedArgs(self):
        try:
            args = {"noFlush":False, "noRecovery":True, "allowReboots":False, "noPackage":True, "noUpload":False}
            self.sc.stop(args)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testWithArgsInvalidPopulatedArgs(self):
        eInvalid = 123
        try:
            kwargs = {"noFlush":False, "noRecovery":eInvalid, "allowReboots":False, "noPackage":True, "noUpload":False}
            self.sc.stop(**kwargs)
        except ApiParamError, e:
            assert e.item == eInvalid
            assert bool in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False

if __name__ == '__main__':
    unittest.main()
