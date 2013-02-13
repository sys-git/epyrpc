
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
from epyrpc.api.eo_v1.impl.common.peers.APeer import APeer
from epyrpc.api.eo_v1.impl.common.testManagement.tests.ATestId import ATestId
from epyrpc.api.eo_v1.impl.neck.testManagement.results.Results import Results
from epyrpc.api.eo_v1.interfaces.common.testManagement.results.iPackageResult import \
    iPackageResult
from epyrpc.api.eo_v1.interfaces.common.tests.iATestResult import iATestResult
from epyrpc.api.iApiTransportResponse import iApiTransportResponse
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
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
    def tearDown(self):
        ExecutionOrganiser.destroySingleton()
        ConfigurationManager.destroySingleton()
    def testNs(self):
        tests = Results(ns="me")
        eNs = "me.results".lower()
        assert tests._getNamespace() == eNs, "Got: %(NS)s" % {"NS":eNs}

class TestTestResult(unittest.TestCase):
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
    def test(self):
        #    TODO: Change this once we know how Results is implemented.
        r = Results(ns="me")
        tId = 123
        bSynchronous = True
        testIds = [ATestId(123), ATestId(456), ATestId(789)]
        result = r._handler_testResult(tId, bSynchronous, testIds)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, dict)
        assert len(response.keys()) == len(testIds)
        for aTestId, aTestResult in response.items():
            assert isinstance(aTestResult, iATestResult)
            tId = aTestId.testId()
            found = None
            for i in testIds:
                if i.testId() == tId:
                    found = i
                    break
            assert found, "Unrequested testId returned!"
            assert isinstance(aTestResult, iATestResult)
            assert aTestResult.testId() == aTestId

class TestPeerResult(unittest.TestCase):
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
    def test(self):
        #    TODO: Change this once we know how Results is implemented.
        r = Results(ns="me")
        tId = 123
        bSynchronous = True
        peerIds = [APeer(123), APeer(456), APeer(789)]
        result = r._handler_peerResult(tId, bSynchronous, peerIds)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, dict)
        assert len(response.keys()) == len(peerIds)
        for aTestId, aTestResult in response.items():
            assert isinstance(aTestResult, iATestResult)
            pId = aTestId.peerId()
            found = None
            for i in peerIds:
                if i.peerId() == pId:
                    found = i
                    break
            assert found, "Unrequested testId returned!"
            assert isinstance(aTestResult, iATestResult)
            assert aTestResult.testId() == aTestId

class TestPackage(unittest.TestCase):
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
    def test(self):
        #    TODO: Change this once we know how Results is implemented.
        r = Results(ns="me")
        tId = 123
        bSynchronous = True
        result = r._handler_package(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, iPackageResult)

if __name__ == '__main__':
    unittest.main()

