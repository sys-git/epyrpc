
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.checkers.tas.iUserDataChecker import iUserDataChecker

class UserDataChecker(iUserDataChecker):
    r"""
    @summary: Check the params for the api.tas.userData methods.
    @attention: For now, all checks just check that a dict is passed, the
    exact format of the dict is T.B.D.
    """
    @staticmethod
    def checkOverwrite(data):
        if not isinstance(data, dict):
            raise ApiParamError(data, dict)
        return data
    @staticmethod
    def checkUpdate(data):
        if not isinstance(data, dict):
            raise ApiParamError(data, dict)
        return data
    @staticmethod
    def checkClear(data):
        if not isinstance(data, list):
            raise ApiParamError(data, list)
        return data
    @staticmethod
    def checkRetrieve(data):
        if not isinstance(data, dict):
            raise ApiParamError(data, dict)
        return data
