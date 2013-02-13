
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.impl.head.tas.SignalFilter import SignalFilter
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterId import \
    iFilterId
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iNamespace import \
    iNamespace
from epyrpc.api.iApiAction import iApiAction
import unittest

class aFilter(iFilterId): pass

class voo(iNamespace):
    pass

class TestSignalFilter(unittest.TestCase):
    def testNs(self):
        sf = SignalFilter("me")
        eNs = "me.signalfilter"
        assert sf._getNamespace() == eNs, "Got: %(NS)s" % {"NS":eNs}

class TestAdd(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.tv = voo()
    def testAddNothing(self):
        try:
            self.sf.add()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testAddNone(self):
        try:
            self.sf.add(None)
        except ApiParamError, e:
            assert e.item == None
        else:
            assert False
    def testAddEmptyList(self):
        assert isinstance(self.sf.add([]), iApiAction)
    def testAddListContainingNone(self):
        assert isinstance(self.sf.add([None]), iApiAction)
    def testAddListContainingNotInamespace(self):
        item = 123
        try:
            self.sf.add([item])
        except ApiParamError, e:
            assert e.item == item
            assert iNamespace in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False
    def testAddListContainsInamespaceInList(self):
        assert isinstance(self.sf.add([self.tv]), iApiAction)
    def testAddListContainsInamespaceOnly(self):
        assert isinstance(self.sf.add(self.tv), iApiAction)
    def testAddListContainingValidAndInvalids(self):
        item = 123
        v = self.tv
        try:
            self.sf.add([v, v, item, v, v])
        except ApiParamError, e:
            assert e.item == item
            assert iNamespace in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False

class TestRemove(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.tv = voo()
    def tRemoveNothing(self):
        try:
            self.sf.remove()
        except TypeError, _e:
            assert True
        else:
            assert False
    def tRemoveNone(self):
        try:
            self.sf.remove(None)
        except ApiParamError, e:
            assert e.item == None
        else:
            assert False
    def tRemoveEmptyList(self):
        assert isinstance(self.sf.remove([]), iApiAction)
    def tRemoveListContainingNone(self):
        assert isinstance(self.sf.remove([None]), iApiAction)
    def tRemoveListContainingNotInamespace(self):
        item = 123
        try:
            self.sf.remove([item])
        except ApiParamError, e:
            assert e.item == item
            assert tuple in e.allowedTypes
        else:
            assert False
    def tRemoveListContainsInamespaceInList(self):
        mute = (self.tv, eMute.ON)
        assert isinstance(self.sf.remove([mute]), iApiAction)
    def tRemoveListContainsInamespaceInListInvalidMute(self):
        muteValue = ~eMute.ON
        mute = (self.tv, muteValue)
        assert not eMute.isValid(muteValue)
        try:
            self.sf.remove([mute])
        except ApiParamError, e:
            assert e.item == muteValue
            assert eMute in e.allowedTypes
        else:
            assert False
    def tRemoveListContainsInamespaceOnly(self):
        try:
            self.sf.remove(self.tv)
        except ApiParamError, e:
            assert e.item == self.tv
            assert tuple in e.allowedTypes
        else:
            assert False
    def tRemoveListContainingValidAndInvalids(self):
        item = 123
        v = self.tv
        try:
            self.sf.remove([v, v, item, v, v])
        except ApiParamError, e:
            assert e.item == v
            assert tuple in e.allowedTypes
        else:
            assert False

class TestMuteAll(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.tv = voo()
    def tNoValue(self):
        assert(self.sf.muteAll(), iApiAction)
    def tMuteOn(self):
        assert(self.sf.muteAll(eMute.ON), iApiAction)
    def tMuteOff(self):
        assert(self.sf.muteAll(eMute.OFF), iApiAction)
    def tInvalidValue(self):
        muteValue = ~eMute.ON
        assert not eMute.isValid(muteValue)
        try:
            self.sf.muteAll(muteValue)
        except ApiParamError, e:
            assert e.item == muteValue
            assert eMute in e.allowedTypes
        else:
            assert False

class TestMute(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.tv = voo()
        self.filter = aFilter()
        self.invalidMuteValue = ~eMute.ON
        assert not eMute.isValid(self.invalidMuteValue)
    def testMuteNothing(self):
        try:
            self.sf.mute()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testMuteNone(self):
        try:
            self.sf.mute(None)
        except ApiParamError, e:
            assert e.item == None
        else:
            assert False
    def testMuteEmptyList(self):
        item = []
        try:
            self.sf.mute(item)
        except ApiParamError, e:
            assert e.item == item
            assert iNamespace in e.allowedTypes
            assert iFilterId in e.allowedTypes
            assert list in e.allowedTypes
        else:
            assert False
    def testMuteListContainingNone(self):
        item = [None]
        try:
            self.sf.mute(item)
        except ApiParamError, e:
            assert e.item == item
            assert iNamespace in e.allowedTypes
            assert iFilterId in e.allowedTypes
            assert list in e.allowedTypes
        else:
            assert False
    def testMuteListContainingNotInamespaceListOrFilterid(self):
        item = 123
        try:
            self.sf.mute([item])
        except ApiParamError, e:
            assert e.item == item
            assert tuple in e.allowedTypes
            assert not iNamespace in e.allowedTypes
            assert not iFilterId in e.allowedTypes
            assert not list in e.allowedTypes
        else:
            assert False
    def testAddListContainsInamespaceInList(self):
        assert isinstance(self.sf.mute([(self.tv, eMute.OFF)]), iApiAction)
    def testAddListContainsIFilteridInList(self):
        assert isinstance(self.sf.mute([(self.filter, eMute.ON)]), iApiAction)
    def testAddListContainsInamespaceInListInvalidMute(self):
        try:
            self.sf.mute([(self.tv, self.invalidMuteValue)])
        except ApiParamError, e:
            assert e.item == self.invalidMuteValue
            assert eMute in e.allowedTypes
            assert iNamespace not in e.allowedTypes
            assert iFilterId not in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False
    def testAddListContainsIFilteridInListInvalidMute(self):
        try:
            self.sf.mute([(self.filter, self.invalidMuteValue)])
        except ApiParamError, e:
            assert e.item == self.invalidMuteValue
            assert eMute in e.allowedTypes
            assert iNamespace not in e.allowedTypes
            assert iFilterId not in e.allowedTypes
            assert list not in e.allowedTypes
        else:
            assert False

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.tv = voo()
    def tStatusWithArgs(self):
        try:
            self.sf.status("hello")
        except TypeError, _e:
            assert True
        else:
            assert False
    def tStatusWithMultipleArgs(self):
        try:
            self.sf.status("hello", "world!")
        except TypeError, _e:
            assert True
        else:
            assert False
    def tStatusWithKwargs(self):
        try:
            self.sf.status(a="hello")
        except TypeError, _e:
            assert True
        else:
            assert False
    def tStatusWithMultipleKwargs(self):
        try:
            self.sf.status(a="hello", b="world!")
        except TypeError, _e:
            assert True
        else:
            assert False
    def tStatusWithMultipleArgsAndKwargs(self):
        try:
            self.sf.status("hello", b="world!")
        except TypeError, _e:
            assert True
        else:
            assert False
    def tStatus(self):
        assert isinstance(self.sf.status(), iApiAction)

class TestGlobalEnable(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.invalidEnabler = ~eGlobalEnable.ON
        assert not eGlobalEnable.isValid(self.invalidEnabler)
    def testInvalidEnabler(self):
        item = "hello"
        try:
            self.sf.globalEnable(item)
        except ApiParamError, e:
            assert e.item == item
            assert eGlobalEnable in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False
    def testValidEnabler(self):
        item = eGlobalEnable.ON
        assert isinstance(self.sf.globalEnable(item), iApiAction)
        item = eGlobalEnable.OFF
        assert isinstance(self.sf.globalEnable(item), iApiAction)

class TestQuery(unittest.TestCase):
    def setUp(self):
        self.sf = SignalFilter("me")
        self.ns = voo()
        self.filter = aFilter()
    def testQueryNothing(self):
        try:
            self.sf.query()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testQueryNone(self):
        try:
            self.sf.query(None)
        except ApiParamError, e:
            assert e.item == None
            assert iFilterId in e.allowedTypes
            assert iNamespace in e.allowedTypes
            assert list in e.allowedTypes
            assert len(e.allowedTypes) == 3
        else:
            assert False
    def testQueryEmptyList(self):
        item = []
        try:
            self.sf.query(item)
        except ApiParamError, e:
            assert e.item == item
            assert iFilterId in e.allowedTypes
            assert iNamespace in e.allowedTypes
            assert list in e.allowedTypes
            assert len(e.allowedTypes) == 3
        else:
            assert False
    def testQueryListContainingNone(self):
        item = [None]
        try:
            isinstance(self.sf.query(item), iApiAction)
        except ApiParamError, e:
            assert e.item == item
    def testQueryListContainingNotInamespace(self):
        item = 123
        try:
            self.sf.query([item])
        except ApiParamError, e:
            assert e.item == item
            assert iFilterId in e.allowedTypes
            assert iNamespace in e.allowedTypes
            assert len(e.allowedTypes) == 2
        else:
            assert False
    def testQueryListContainsInamespaceInList(self):
        ns = self.ns
        assert isinstance(self.sf.query([ns]), iApiAction)
    def testQueryListContainsIfilteridInList(self):
        ns = self.filter
        assert isinstance(self.sf.query([ns]), iApiAction)
    def testQueryContainsIfilterid(self):
        ns = self.filter
        assert isinstance(self.sf.query(ns), iApiAction)
    def testQueryListContainingValidAndInvalidsInamespace(self):
        item = 123
        v = self.ns
        try:
            self.sf.query([v, v, item, v, v])
        except ApiParamError, e:
            assert e.item == item
            assert iNamespace in e.allowedTypes
            assert iFilterId in e.allowedTypes
        else:
            assert False
    def testQueryListContainingValidAndInvalidsIfilterid(self):
        item = 123
        v = self.filter
        try:
            self.sf.query([v, v, item, v, v])
        except ApiParamError, e:
            assert e.item == item
            assert iNamespace in e.allowedTypes
            assert iFilterId in e.allowedTypes
        else:
            assert False
    def testQueryListContainingValids(self):
        f = self.filter
        n = self.ns
        assert isinstance(self.sf.query([f, n, n, f]), iApiAction)
    def testQueryListContainingValidsAndNone(self):
        f = self.filter
        n = self.ns
        assert isinstance(self.sf.query([f, n, n, f, None]), iApiAction)

if __name__ == '__main__':
    unittest.main()


