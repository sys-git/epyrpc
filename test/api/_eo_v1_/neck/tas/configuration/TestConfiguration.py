
from MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
from YouView.TAS.Common.SignalExchangeHub.SignalExchangeHub import \
    SignalExchangeHub
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.impl.common.tas.ConfigurationResult import \
    ConfigurationResult
from epyrpc.api.eo_v1.impl.neck.tas.configuration.Configuration import \
    Configuration
from epyrpc.api.iApiTransportResponse import iApiTransportResponse
from epyrpc.utils.configuration.ConfigurationManager import ConfigurationManager
import sys
import unittest

class TestConfigure(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[:1]
        path = "config/ipc"
        ConfigurationManager(cwd=path)
        SignalExchangeHub()
        ExecutionOrganiser().bindInterface()
        self.c = Configuration("me")
    def tearDown(self):
        ExecutionOrganiser()._stageController._STAGES_TIMEOUT = 1
        ExecutionOrganiser.destroySingleton()
    def tXXXestWithInvalidArgs(self):
        tId = 123
        bSynchronous = True
        args = [1, 2, 3]
        try:
            self.c._handler_configure(tId, bSynchronous, args)
        except ApiParamError, e:
            assert e.item == args
            assert dict in e.allowedTypes
            assert len(e.allowedTypes) == 1
        else:
            assert False
    def testValidArgs(self):
        tId = 123
        bSynchronous = True
        args = {"key":"value"}
        result = self.c._handler_configure(tId, bSynchronous, args)
        assert isinstance(result, iApiTransportResponse)
        response = result.response()
        assert isinstance(response, ConfigurationResult)

# class TestQuery(unittest.TestCase):
#    def setUp(self):
#        sys.argv = sys.argv[:1]
#        path = "config/ipc"
#        ConfigurationManager(cwd=path)
#        SignalExchangeHub()
#        ExecutionOrganiser().bindInterface()
#        self.c = Configuration("me")
#    def tearDown(self):
#        ExecutionOrganiser()._stageController._STAGES_TIMEOUT = 1
#        ExecutionOrganiser.destroySingleton()
#    def testWithInvalidArgs(self):
#        tId = 123
#        bSynchronous = True
#        args = [1,2,3]
#        try:
#            self.c._handler_query(tId, bSynchronous, args)
#        except ApiParamError, e:
#            assert e.item==1
#            assert basestring in e.allowedTypes
#            assert len(e.allowedTypes)==1
#        else:
#            assert False
#    def testValidArgNoConfiguration(self):
#        tId = 123
#        bSynchronous = True
#        args = ["key"]
#        result = self.c._handler_query(tId, bSynchronous, args)
#        assert isinstance(result, iApiTransportResponse)
#        response = result.response()
#        assert isinstance(response, iConfigurationResult)
#        config = response.config()
#        assert len(config.keys())==1
#        r = config.values()[0]
#        assert isinstance(r, InvalidConfiguration)
#        assert r.message.count(args[0])==1
#    def testValidArgConfigurationExists(self):
#        tId = 123
#        bSynchronous = True
#        args = ["masterLauncher", "discovery", "execution", "bad.name"]
#        result = self.c._handler_query(tId, bSynchronous, args)
#        assert isinstance(result, iApiTransportResponse)
#        response = result.response()
#        assert isinstance(response, iConfigurationResult)
#        config = response.config()
#        assert len(config.keys())==4
#        for i in range(0, len(args)-1):
#            assert isinstance(config[args[i]], Objectify)
#        r = config[args[3]]
#        assert isinstance(r, InvalidConfiguration)
#        assert r.message.count(args[3])==1

# class TestQueryAll(unittest.TestCase):
#    def setUp(self):
#        sys.argv = sys.argv[:1]
#        path = "config/ipc"
#        ConfigurationManager(cwd=path)
#        SignalExchangeHub()
#        ExecutionOrganiser().bindInterface()
#        self.c = Configuration("me")
#    def tearDown(self):
#        ExecutionOrganiser()._stageController._STAGES_TIMEOUT = 1
#        ExecutionOrganiser.destroySingleton()
#    def testWithInvalidArgs(self):
#        tId = 123
#        bSynchronous = True
#        args = [1,2,3]
#        try:
#            self.c._handler_query(tId, bSynchronous, args)
#        except ApiParamError, e:
#            assert e.item==1
#            assert basestring in e.allowedTypes
#            assert len(e.allowedTypes)==1
#        else:
#            assert False
#    def testValidArgs(self):
#        tId = 123
#        bSynchronous = True
#        args = ["key"]
#        assert isinstance(self.c._handler_query(tId, bSynchronous, args), iApiTransportResponse)

if __name__ == '__main__':
    unittest.main()
