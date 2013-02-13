
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.common.tas.signalFilter.Namespace import Namespace
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iNamespace import \
    iNamespace
import copy
import unittest

class TestNamespace(unittest.TestCase):
    def setUp(self):
        pass
    def testInvalid(self):
        try:
            Namespace()
        except ApiParamError, e:
            assert basestring in e.allowedTypes
            assert iNamespace in e.allowedTypes
            assert len(e.allowedTypes) == 2
    def testStringNamespace(self):
        eN = "i.am.a.namespace"
        eN1 = "not"
        eN2 = copy.deepcopy(eN)
        ns = Namespace(namespace=eN)
        ns1 = Namespace(namespace=eN1)
        ns2 = Namespace(namespace=eN2)
        assert ns.namespace() == eN
        assert ns1.namespace() == eN1
        assert ns2.namespace() == eN2
        assert isinstance(ns.id_(), basestring)
        assert isinstance(ns1.id_(), basestring)
        assert isinstance(ns2.id_(), basestring)
        assert not ns.isRegx()
        assert not ns.compare(None)
        assert not ns.compare(object())
        assert not ns.compare(ns1)
        assert ns.compare(ns2)
    def testExport(self):
        eN = "i.am.a.namespace"
        ns = Namespace(namespace=eN)
        assert ns.namespace() == eN
        c = ns.export()
        assert c.compare(ns)
        assert ns != c
    def testCopyConstructorNs(self):
        eN = "i.am.a.namespace"
        n = Namespace(namespace=eN)
        n1 = Namespace(n)
        assert n.compare(n1)

if __name__ == '__main__':
    unittest.main()
