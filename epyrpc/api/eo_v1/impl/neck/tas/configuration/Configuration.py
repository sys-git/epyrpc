
from epyrpc.api.eo_v1.impl.checkers.tas.ConfigurationChecker import \
    ConfigurationChecker
from epyrpc.api.eo_v1.impl.common.tas.ConfigurationResult import \
    ConfigurationResult
from epyrpc.api.eo_v1.interfaces.neck.tas.configuration.iConfiguration import iConfiguration
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser

class Configuration(iConfiguration):
    def __init__(self, ns="", solicited=False):
        super(Configuration, self).__init__(ns=ns, solicited=solicited)
    """ HANDLERS: """
    def _handler_configure(self, tId, bSynchronous, args):
        args = self._handleStandardCheck(tId, bSynchronous, ConfigurationChecker.checkConfigure, args)
        def _override(args):
            eo = ExecutionOrganiser()
            config = eo.overrideArgs(args)
            return ConfigurationResult(config)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _override(x), args)
    def _handler_query(self, tId, bSynchronous, args):
        args = self._handleStandardCheck(tId, bSynchronous, ConfigurationChecker.checkQuery, args)
        def _query(args):
            eo = ExecutionOrganiser()
            config = eo.queryArgs(args)
            return ConfigurationResult(config)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _query(x), args)
    def _handler_queryAll(self, tId, bSynchronous, args):
        args = self._handleStandardCheck(tId, bSynchronous, ConfigurationChecker.checkQuery, args)
        def _queryAll():
            eo = ExecutionOrganiser()
            config = eo.queryArgsAll()
            return ConfigurationResult(config)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _queryAll())
