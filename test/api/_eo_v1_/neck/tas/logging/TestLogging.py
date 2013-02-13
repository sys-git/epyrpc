
from epyrpc.api.eo_v1.enums.eLoggingState import eLoggingState
from epyrpc.api.eo_v1.impl.neck.tas.Logging import Logging
from epyrpc.api.eo_v1.interfaces.common.tas.logging.iLoggingResult import \
    iLoggingResult
from epyrpc.api.iApiTransportResponse import iApiTransportResponse
from epyrpc.utils.LogManager import LogManager
import sys
import unittest

def checkLoggingResult(result):
    assert isinstance(result, iApiTransportResponse)
    response = result.response()
    assert isinstance(response, iLoggingResult)
    l = LogManager()
    if l.isOn() == True:
        assert response.isOn() == eLoggingState.ON
    else:
        assert response.isOn() == eLoggingState.OFF
    assert response.location() == l.FILENAME

class TestLoggingOn(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        self.logging = LogManager()
        self.l = Logging()
    def tearDown(self):
        LogManager.destroySingleton()
    def testWithInvalidArgs(self):
        tId = 123
        bSynchronous = True
        args = [1, 2, 3]
        try:
            self.l._handler_turnOn(tId, bSynchronous, args)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testValidNoArgs(self):
        tId = 123
        bSynchronous = True
        checkLoggingResult(self.l._handler_turnOn(tId, bSynchronous))

class TestLoggingOff(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        self.logging = LogManager()
        self.l = Logging()
    def tearDown(self):
        LogManager.destroySingleton()
    def testWithInvalidArgs(self):
        tId = 123
        bSynchronous = True
        args = [1, 2, 3]
        try:
            self.l._handler_turnOff(tId, bSynchronous, args)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testValidNoArgs(self):
        tId = 123
        bSynchronous = True
        checkLoggingResult(self.l._handler_turnOff(tId, bSynchronous))
    
class TestQuery(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        self.logging = LogManager()
        self.l = Logging()
    def tearDown(self):
        LogManager.destroySingleton()
    def testWithInvalidArgs(self):
        tId = 123
        bSynchronous = True
        args = [1, 2, 3]
        try:
            self.l._handler_query(tId, bSynchronous, args)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testValidNoArgs(self):
        tId = 123
        bSynchronous = True
        checkLoggingResult(self.l._handler_query(tId, bSynchronous))

if __name__ == '__main__':
    unittest.main()
