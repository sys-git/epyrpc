
from YouView.TAS.Common.SignalExchangeHub.SignalExchangeHub import \
    SignalExchangeHub
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
from epyrpc.api.eo_v1.enums.eStateControlResult import eStateControlResult
from epyrpc.api.eo_v1.impl.neck.tas.StateControl import StateControl
from epyrpc.api.iApiTransportResponse import iApiTransportResponse
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
import sys
import time
import unittest

class TestInit(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = "config/ipc"
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        ExecutionOrganiser().bindInterface()
        self.sc = StateControl("me")
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
    def testWithArgs(self):
        tId = 123
        bSynchronous = True
        try:
            self.sc._handler_init(tId, bSynchronous, None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        tId = 123
        bSynchronous = True
        result = self.sc._handler_init(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        assert eStateControlResult.isValid(result.response())

class TestTerminate(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = "config/ipc"
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        eo = ExecutionOrganiser()
        eo.bindInterface()
        eo.createProcess()
        self.sc = StateControl("me")
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
    def testWithArgs(self):
        tId = 123
        bSynchronous = True
        try:
            self.sc._handler_terminate(tId, bSynchronous, None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def test(self):
        tId = 123
        bSynchronous = True
        result = self.sc._handler_terminate(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        assert eStateControlResult.isValid(result.response())
        #    Long enough to shutdown the ExecutionOrganiser:
        time.sleep(20)
        assert not ExecutionOrganiser.hasInstance()

class TestRun(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = "config/ipc"
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        eo = ExecutionOrganiser()
        eo.bindInterface()
        eo.createProcess()
        self.sc = StateControl("me")
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
    def testWithArgs(self):
        tId = 123
        bSynchronous = True
        try:
            self.sc._handler_run(tId, bSynchronous, None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        tId = 123
        bSynchronous = True
        result = self.sc._handler_run(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        assert eStateControlResult.isValid(result.response())

class TestPause(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = "config/ipc"
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        eo = ExecutionOrganiser()
        eo.bindInterface()
        eo.createProcess()
        self.sc = StateControl("me")
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
    def testWithArgs(self):
        tId = 123
        bSynchronous = True
        try:
            self.sc._handler_pause(tId, bSynchronous, None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        tId = 123
        bSynchronous = True
        result = self.sc._handler_pause(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        assert eStateControlResult.isValid(result.response())

class TestPauseAtEnd(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = "config/ipc"
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        eo = ExecutionOrganiser()
        eo.bindInterface()
        eo.createProcess()
        self.sc = StateControl("me")
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
    def testWithArgs(self):
        tId = 123
        bSynchronous = True
        try:
            self.sc._handler_pauseAtEnd(tId, bSynchronous, None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testNoArgs(self):
        tId = 123
        bSynchronous = True
        result = self.sc._handler_pauseAtEnd(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        assert eStateControlResult.isValid(result.response())

class TestStop(unittest.TestCase):
    def setUp(self):
        path = "config/ipc"
        sys.argv = sys.argv[:1]
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        eo = ExecutionOrganiser()
        eo.bindInterface()
        eo.createProcess()
        self.sc = StateControl("me")
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
    def testNoArgs(self):
        tId = 123
        bSynchronous = True
        result = self.sc._handler_stop(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        assert eStateControlResult.isValid(result.response())

if __name__ == '__main__':
    unittest.main()








