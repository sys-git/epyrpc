
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eSync import eSync
from epyrpc.api.iApiAction import iApiAction
from epyrpc.core.transport.iIpcTransport import iIpcTransport
import unittest

class TestiApiAction(unittest.TestCase):
    def setUp(self):
        self.ipc = None
        self.solicited = True
    def testInvalidNumParams(self):
        try:
            iApiAction()
        except TypeError, _e:
            assert True
        else:
            assert False
    def testInvalidNamespace(self):
        ns = None
        try:
            iApiAction(self.ipc, ns, self.solicited)
        except ApiParamError, e:
            assert e.item == None
            assert e.allowedTypes == [basestring]
            assert e.allowedValues == []
    def testValidNamespaceString(self):
        ns = "hello.world"
        api = iApiAction(self.ipc, ns, self.solicited)
        assert api.namespace == ns, "Got: %(NS)s" % {"NS":api.namespace}
        assert api.args() == (), "Got: %(NS)s" % {"NS":api.args}
    def testValidArgs(self):
        ns = "hello.world"
        args = ("i", "am", "some", "args!")
        api = iApiAction(self.ipc, ns, self.solicited, *args)
        assert api.args() == args
    def testValidSync(self):
        s = eSync.SYNCHRONOUS
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        api.sync = s
        s = eSync.ASYNCHRONOUS
        api.sync = s
    def testInvalidSync(self):
        s = ~eSync.SYNCHRONOUS
        assert not eSync.isValid(s)
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        try:
            api.sync = s
        except ApiParamError, e:
            assert e.item == s
            assert eSync in e.allowedTypes
            assert len(e.allowedTypes) == 1
    def testValidTimeoutInt(self):
        t = 1
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        api.timeout = t
    def testInvalidTimeoutInt(self):
        t = -1
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        try:
            api.timeout = t
        except ApiParamError, e:
            assert e.item == t
            assert int in e.allowedTypes
            assert float in e.allowedTypes
            assert len(e.allowedTypes) == 2
    def testValidTimeoutFloat(self):
        t = 1.0
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        api.timeout = t
    def testInvalidTimeoutFloat(self):
        t = -1.0
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        try:
            api.timeout = t
        except ApiParamError, e:
            assert e.item == t
            assert int in e.allowedTypes
            assert float in e.allowedTypes
            assert len(e.allowedTypes) == 2
    def testInvalidTimeout(self):
        t = "invalid value!"
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        try:
            api.timeout = t
        except ApiParamError, e:
            assert e.item == t
            assert int in e.allowedTypes
            assert float in e.allowedTypes
            assert len(e.allowedTypes) == 2
    def testSetValidIpc(self):
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        myIpc = MyTransport()
        api.ipc = myIpc
        assert api.ipc == myIpc
    def testSetInvalidIpc(self):
        api = iApiAction(self.ipc, "hello.world", self.solicited)
        myIpc = object()
        try:
            api.ipc = myIpc
        except ApiParamError, e:
            assert e.item == myIpc
            assert iIpcTransport in e.allowedTypes
            assert len(e.allowedTypes) == 1
    def testDefaults(self):
        ns = "hello.world"
        ipc = MyTransport()
        api = iApiAction(ipc, ns, self.solicited)
        assert api.sync == iApiAction.DEFAULT_SYNC
        assert api.timeout == iApiAction.DEFAULT_TIMEOUT
        assert api.namespace == ns
        assert api.ipc == ipc
    def testSolicited(self):
        ns = "hello.world"
        ipc = MyTransport()
        api = iApiAction(ipc, ns, self.solicited)
        assert api.solicited == True
        api.solicited = False
        assert api.solicited == False
        api.solicited = True
        assert api.solicited == True
    def testCallback(self):
        ns = "hello.world"
        ipc = MyTransport()
        api = iApiAction(ipc, ns, True)
        def cb(): pass
        api.callback = cb
        assert api.callback == cb
        api.callback = None
        assert api.callback == None

class MyTransport(iIpcTransport):
    def __init__(self, *args, **kwargs):
        pass

if __name__ == '__main__':
    unittest.main()
