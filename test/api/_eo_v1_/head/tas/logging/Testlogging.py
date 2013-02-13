
from epyrpc.api.eo_v1.impl.head.tas.Logging import Logging
from epyrpc.api.iApiAction import iApiAction
import unittest

class TestTurnOn(unittest.TestCase):
    def setUp(self):
        self.logging = Logging("me")
    def testWithArgs(self):
        try:
            self.logging.turnOn(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.logging.turnOn(), iApiAction)

class TestTerminate(unittest.TestCase):
    def setUp(self):
        self.logging = Logging("me")
    def testWithArgs(self):
        try:
            self.logging.turnOff(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.logging.turnOff(), iApiAction)

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.logging = Logging("me")
    def testWithArgs(self):
        try:
            self.logging.query(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        assert isinstance(self.logging.query(), iApiAction)

if __name__ == '__main__':
    unittest.main()
