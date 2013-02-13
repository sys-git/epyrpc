from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.head.testManagement.tests.Tests import Tests
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestId import \
    iTestId
from epyrpc.api.iApiAction import iApiAction
import unittest

class voo(iTestId):
    pass

class TestAbort(unittest.TestCase):
    def setUp(self):
        self.tests = Tests("me")
        self.tv = voo()
    def testAbortNothing(self):
        try:
            self.tests.abort()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testAbortNone(self):
        try:
            self.tests.abort(None)
        except ApiParamError, e:
            assert e.item == None
        else:
            assert False
    def testAbortEmptyList(self):
        assert isinstance(self.tests.abort([]), iApiAction)
    def testAbortListContainingNone(self):
        assert isinstance(self.tests.abort([None]), iApiAction)
    def testAbortListContainingNotITestId(self):
        item = 123
        try:
            self.tests.abort([item])
        except ApiParamError, e:
            assert e.item == item
            assert iTestId in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False
    def testAbortListContainsInamespaceInList(self):
        assert isinstance(self.tests.abort([self.tv]), iApiAction)
    def testAbortListContainsInamespaceOnly(self):
        assert isinstance(self.tests.abort(self.tv), iApiAction)
    def testAbortListContainingValidAndInvalids(self):
        item = 123
        v = self.tv
        try:
            self.tests.abort([v, v, item, v, v])
        except ApiParamError, e:
            assert e.item == item
            assert iTestId in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False

class TestQueryTests(unittest.TestCase):
    def setUp(self):
        self.tests = Tests("me")
        self.tv = voo()
    def testQueryNothing(self):
        try:
            self.tests.queryTests()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQueryNone(self):
        try:
            self.tests.queryTests(None)
        except ApiParamError, e:
            assert e.item == None
        else:
            assert False
    def testQueryEmptyList(self):
        assert isinstance(self.tests.queryTests([]), iApiAction)
    def testQueryListContainingNone(self):
        assert isinstance(self.tests.queryTests([None]), iApiAction)
    def testQueryListContainingNotITestId(self):
        item = 123
        try:
            self.tests.queryTests([item])
        except ApiParamError, e:
            assert e.item == item
            assert iTestId in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False
    def testQueryListContainsInamespaceInList(self):
        assert isinstance(self.tests.queryTests([self.tv]), iApiAction)
    def testQueryListContainsInamespaceOnly(self):
        assert isinstance(self.tests.queryTests(self.tv), iApiAction)
    def testQueryListContainingValidAndInvalids(self):
        item = 123
        v = self.tv
        try:
            self.tests.queryTests([v, v, item, v, v])
        except ApiParamError, e:
            assert e.item == item
            assert iTestId in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False

class TestQueryTestPacks(unittest.TestCase):
    def setUp(self):
        self.tests = Tests("me")
        self.tv = voo()
    def testQueryNothing(self):
        self.tests.queryTestPacks()
    def testQueryNone(self):
        try:
            self.tests.queryTestPacks(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQuerySomething(self):
        try:
            self.tests.queryTestPacks(object())
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQueryListOfSomething(self):
        try:
            self.tests.queryTestPacks([object()])
        except TypeError, _e:
            assert True
        else:
            assert False
