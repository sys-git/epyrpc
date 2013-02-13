
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iUserDataChecker(iApi):
    @staticmethod
    def checkOverwrite(data):
        r"""
        @summary: Check that the data is a dict of key:value pairs.
        """
        raise NotImplementedException("iUserDataChecker.checkOverwrite")
    @staticmethod
    def checkUpdate(data):
        r"""
        @summary: Check that the data is a dict of key:value pairs.
        """
        raise NotImplementedException("iUserDataChecker.checkUpdate")
    @staticmethod
    def checkClear(data):
        r"""
        @summary: Check that the data is a list of keys.
        """
        raise NotImplementedException("iUserDataChecker.checkClear")
    @staticmethod
    def checkRetrieve(data):
        r"""
        @summary: Check that the data is a dict of key:value pairs.
        """
        raise NotImplementedException("iUserDataChecker.checkRetrieve")

