from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.head.tas.Configuration import Configuration
from epyrpc.api.iApiAction import iApiAction
import unittest

class TestConfigure(unittest.TestCase):
    def setUp(self):
        self.c = Configuration("me")
    def testWithInvalidArgs(self):
        args = [1, 2, 3]
        try:
            self.c.configure(args)
        except ApiParamError, e:
            assert e.item == args
            assert dict in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False
    def testValidArgs(self):
        args = {"key":"value"}
        assert isinstance(self.c.configure(args), iApiAction)

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.c = Configuration("me")
    def testWithInvalidArgs(self):
        args = [1, 2, 3]
        try:
            self.c.query(args)
        except ApiParamError, e:
            assert e.item == 1
            assert basestring in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False
    def testValidArgs(self):
        args = ["key"]
        assert isinstance(self.c.query(args), iApiAction)
    def testNoArgs(self):
        args = []
        try:
            self.c.query(args)
        except ApiParamError, e:
            assert e.item == args
            assert list in e.allowedTypes
            assert len(e.allowedTypes) == 1

class TestQueryAll(unittest.TestCase):
    def setUp(self):
        self.c = Configuration("me")
    def testWithInvalidArgs(self):
        args = [1, 2, 3]
        try:
            self.c.queryAll(args)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testValidArgs(self):
        assert isinstance(self.c.queryAll(), iApiAction)

if __name__ == '__main__':
    unittest.main()
