
from epyrpc.api.eo_v1.impl.head.testManagement.results.Results import Results
from epyrpc.api.eo_v1.impl.head.testManagement.tests.Tests import Tests
from epyrpc.api.eo_v1.interfaces.head.testManagement.iTestManagement import \
    iTestManagement

class TestManagement(iTestManagement):
    r"""
    @attention: This class could be auto-generated from, say XML.
    @attention: attr(tests) = The tests object.
    @attention: attr(results) = The results object.
    @see: iTests.
    @see: iResults.
    """
    def __init__(self, ns="", solicited=True, ipc=None):
        super(TestManagement, self).__init__(ns=ns, solicited=solicited)
        self._setup(ns=self._getNamespace(), solicited=self.solicited)
    def _setup(self, **kwargs):
        self.tests = Tests(**kwargs)
        self._apis.append(self.tests)
        self.results = Results(**kwargs)
        self._apis.append(self.results)

