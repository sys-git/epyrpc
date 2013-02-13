
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.checkers.tas.iStateControlChecker import \
    iStateControlChecker

class StateControlChecker(iStateControlChecker):
    r"""
    @summary: Check the params for the api.tas.stateControl methods.
    """
    @staticmethod
    def checkStop(**kwargs):
        noFlush = kwargs.pop("noFlush", False)
        noRecovery = kwargs.pop("noRecovery", False)
        allowReboots = kwargs.pop("allowReboots", True)
        noPackage = kwargs.pop("noPackage", True)
        noUpload = kwargs.pop("noUpload", True)
        if not isinstance(noFlush, bool):
            raise ApiParamError(noFlush, bool)
        if not isinstance(noRecovery, bool):
            raise ApiParamError(noRecovery, bool)
        if not isinstance(allowReboots, bool):
            raise ApiParamError(allowReboots, bool)
        if not isinstance(noPackage, bool):
            raise ApiParamError(noPackage, bool)
        if not isinstance(noUpload, bool):
            raise ApiParamError(noUpload, bool)
        return kwargs
