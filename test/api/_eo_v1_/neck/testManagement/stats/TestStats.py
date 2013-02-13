
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
from epyrpc.api.eo_v1.impl.neck.testManagement.stats.Stats import Stats
from epyrpc.api.eo_v1.interfaces.common.testManagement.stats.iStatsResult import \
    iStatsResult
from epyrpc.api.iApiTransportResponse import iApiTransportResponse
from epyrpc.utils.configurationManager import ConfigurationManager
import os
import sys
import unittest

class TestNs(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        ConfigurationManager.destroySingleton()
        path = os.path.realpath("config/ipc")
        self.eo = ExecutionOrganiser()
        self.eo.bindInterface()
        ConfigurationManager(cwd=path)
    def testNs(self):
        tests = Stats(ns="me")
        eNs = "me.stats".lower()
        assert tests._getNamespace() == eNs, "Got: %(NS)s" % {"NS":eNs}

class TestQuery(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        ConfigurationManager.destroySingleton()
        path = os.path.realpath("config/ipc")
        self.eo = ExecutionOrganiser()
        self.eo.bindInterface()
        ConfigurationManager(cwd=path)
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
        ConfigurationManager.destroySingleton()
    def testStats(self):
        #    FIXME: Implement once we know how Stats is implemented.
        tests = Stats(ns="me")
        tId = 123
        bSynchronous = True
        result = tests._handler_query(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, iStatsResult)

if __name__ == '__main__':
    unittest.main()

