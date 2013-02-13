
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.common.peers.APeer import APeer
from epyrpc.api.eo_v1.impl.common.testManagement.tests.ATestId import ATestId
from epyrpc.api.eo_v1.impl.head.testManagement.results.Results import Results
from epyrpc.api.eo_v1.interfaces.common.peers.iAPeer import iAPeer
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iATestId import \
    iATestId
from epyrpc.api.iApiAction import iApiAction
import unittest

class TestTestResult(unittest.TestCase):
    def setUp(self):
        self.results = Results("me")
        self.eNs = "me.results.testResult".lower()
    def testArgsIsNone(self):
        try:
            self.results.testResult(None)
        except ApiParamError, e:
            assert e.item == None
            assert list in e.allowedTypes
            assert iATestId in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryNoArgs(self):
        try:
            self.results.testResult()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQueryEmptyList(self):
        try:
            self.results.testResult([])
        except ApiParamError, e:
            assert e.item == []
            assert list in e.allowedTypes
            assert iATestId in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryValidListOfITestIds(self):
        result = self.results.testResult([ATestId(123), ATestId(456), ATestId(789)])
        assert isinstance(result, iApiAction)
        assert result.getNamespace() == self.eNs
    def testQueryValidListOfITestIdsWithNones(self):
        result = self.results.testResult([ATestId(123), None, ATestId(789)])
        assert isinstance(result, iApiAction)
        assert result.getNamespace() == self.eNs
    def testQueryInvalidListOfITestIds(self):
        badData = object()
        try:
            self.results.testResult([ATestId(123), badData, ATestId(789)])
        except ApiParamError, e:
            assert e.item == badData
            assert list in e.allowedTypes
            assert iATestId in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryValidTestId(self):
        result = self.results.testResult(ATestId(123))
        assert isinstance(result, iApiAction)
        assert result.getNamespace() == self.eNs

class TestPeerResult(unittest.TestCase):
    def setUp(self):
        self.results = Results("me")
        self.eNs = "me.results.peerResult".lower()
    def testArgsIsNone(self):
        try:
            self.results.peerResult(None)
        except ApiParamError, e:
            assert e.item == None
            assert list in e.allowedTypes
            assert iAPeer in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryNoArgs(self):
        try:
            self.results.peerResult()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQueryEmptyList(self):
        try:
            self.results.peerResult([])
        except ApiParamError, e:
            assert e.item == []
            assert list in e.allowedTypes
            assert iAPeer in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryValidListOfITestIds(self):
        result = self.results.peerResult([APeer(123), APeer(456), APeer(789)])
        assert isinstance(result, iApiAction)
        assert result.getNamespace() == self.eNs
    def testQueryValidListOfITestIdsWithNones(self):
        result = self.results.peerResult([APeer(123), None, APeer(789)])
        assert isinstance(result, iApiAction)
        assert result.getNamespace() == self.eNs
    def testQueryInvalidListOfITestIds(self):
        badData = object()
        try:
            self.results.peerResult([APeer(123), badData, APeer(789)])
        except ApiParamError, e:
            assert e.item == badData
            assert list in e.allowedTypes
            assert iAPeer in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryValidTestId(self):
        result = self.results.peerResult(APeer(123))
        assert isinstance(result, iApiAction)
        assert result.getNamespace() == self.eNs

class TestPackage(unittest.TestCase):
    def setUp(self):
        self.results = Results("me")
        self.eNs = "me.results.package".lower()
    def testArgsIsNone(self):
        try:
            self.results.package(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQueryNoArgs(self):
        assert isinstance(self.results.package(), iApiAction)
    def testQueryEmptyList(self):
        try:
            self.results.package([])
        except TypeError, _e:
            assert True
        else:
            assert False

if __name__ == '__main__':
    unittest.main()


