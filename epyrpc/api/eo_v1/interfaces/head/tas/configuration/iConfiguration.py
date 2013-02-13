
from epyrpc.api.iApi import iApi
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iConfiguration(iApi):
    def configure(self, args):
        r"""
        @summary: Override initial configuration arguments.
        @param args: a dict of arguments to override the ExecutionOrganiser with.
        @see: iConfiguration._handler_configure()
        @return: iConfigurationResult
        @raise Exception: Error overriding args...T.B.D.
        """
        raise NotImplementedException("iConfiguration.configure")
    def query(self, configToQuery):
        r"""
        @summary: Query configuration values.
        @param configToQuery: type(list) of config keys to query.
        @raise iApiParamError: Error in parameters.
        @return: iConfigurationResult
        @TODO: Implement this!
        """
        raise NotImplementedException("iConfiguration.query")
    def queryAll(self):
        r"""
        @summary: Query all configuration values.
        @return: iConfigurationResult
        @TODO: Implement this!
        """
        raise NotImplementedException("iConfiguration .queryAll")
