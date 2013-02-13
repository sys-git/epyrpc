
from epyrpc.api.eo_v1.impl.head.testManagement.stats.Stats import Stats
from epyrpc.api.iApiAction import iApiAction
import unittest

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.stats = Stats("me")
    def testAbortNothing(self):
        assert isinstance(self.stats.query(), iApiAction)
    def testQueryNone(self):
        try:
            self.stats.query(None)
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQuerySomething(self):
        try:
            self.stats.query([object()])
        except TypeError, e:
            assert e.item == None
        else:
            assert False

if __name__ == '__main__':
    unittest.main()


