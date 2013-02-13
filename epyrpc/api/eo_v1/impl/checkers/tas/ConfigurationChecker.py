
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.checkers.tas.iStateControlChecker import \
    iStateControlChecker

class ConfigurationChecker(iStateControlChecker):
    r"""
    @summary: Check the params for the api.tas.configuration methods.
    """
    @staticmethod
    def checkConfigure(args):
        if not isinstance(args, dict):
            raise ApiParamError(args, dict)
        return args
    @staticmethod
    def checkQuery(args):
        if not isinstance(args, list):
            raise ApiParamError(args, list)
        newArgs = []
        for i in args:
            if i != None:
                if not isinstance(i, basestring):
                    raise ApiParamError(i, basestring)
                newArgs.append(i)
        if len(args) == 0:
            raise ApiParamError(args, list)
        return newArgs
