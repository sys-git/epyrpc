
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApi import iApi

class iConfiguration(iApi):
    def _handler_configure(self, tId, bSynchronous, args):
        r"""
        @attention: Same rules apply to the arguments as that of the API that called it
        @summary: Override initial configuration arguments.
        @param args: a dict of arguments to override the ExecutionOrganiser with.
        @see: iConfiguration._handler_configure()
        @return: iConfigurationResult
        @raise Exception: Error overriding args...T.B.D.
        @TODO: Implement arg-override.
        """
        raise NotImplementedException("iConfiguration._handler_configure")
    def _handler_query(self, tId, bSynchronous, configToQuery):
        r"""
        @summary: Query configuration values.
        @param configToQuery: type(list) of config keys to query.
        @raise iApiParamError: Error in parameters.
        @return: iConfigurationResult
        """
        raise NotImplementedException("iConfiguration._handler_query")
    def _handler_queryAll(self, tId, bSynchronous):
        r"""
        @summary: Query configuration values.
        @return: iConfigurationResult
        """
        raise NotImplementedException("iConfiguration._handler_queryAll")
