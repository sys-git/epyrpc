
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.Cache.primitives.CachedTestDetails import \
    CachedTestDetails
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
from epyrpc.api.eo_v1.impl.common.testManagement.tests.ATestId import ATestId
from epyrpc.api.eo_v1.impl.neck.testManagement.tests.Tests import Tests
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestPacks import \
    iTestPacks
from epyrpc.api.eo_v1.interfaces.common.tests.iATest import iATest
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
        tests = Tests(ns="me")
        eNs = "me.tests".lower()
        assert tests._getNamespace() == eNs, "Got: %(NS)s" % {"NS":eNs}

class TestQueryTestPacks(unittest.TestCase):
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
        #    TODO: Fix once we know how Tests is implemented.
        t = Tests()
        tId = 123
        bSynchronous = True
        result = t._handler_queryTestPacks(tId, bSynchronous)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, iTestPacks)

class TestQueryTests(unittest.TestCase):
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
        t = Tests()
        tId = 123
        bSynchronous = True
        testIds = [ATestId(234), ATestId(345), ATestId(456)]
        result = t._handler_queryTests(tId, bSynchronous, testIds)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, dict)
        #    Now check returned results:
        for key, value in response.items():
            assert isinstance(value, CachedTestDetails)
            tId = key.testId()
            found = None
            for i in testIds:
                testId = i.testId()
                if tId == testId:
                    found = i
                    break
            assert found

class TestAbort(unittest.TestCase):
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
    def testAbort(self):
        #    TODO: Fix once we know how Tests is implemented.
        t = Tests(ns="me")
        tId = 123
        bSynchronous = True
        testIds = [ATestId(456), ATestId(567), ATestId(678)]
        result = t._handler_abort(tId, bSynchronous, testIds)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, dict)
        for key, value in response.items():
            assert isinstance(value, iATest)
            tId = key.testId()
            #    Now find the item:
            found = None
            for i in testIds:
                testId = i.testId()
                if tId == testId:
                    found = i
                    break
            assert found

if __name__ == '__main__':
    unittest.main()

