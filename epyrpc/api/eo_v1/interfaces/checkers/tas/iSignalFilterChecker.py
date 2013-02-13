
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iSignalFilterChecker(iApi):
    @staticmethod
    def checkAdd(namespace):
        raise NotImplementedException("iSignalFilterChecker.checkAdd")
    @staticmethod
    def checkRemove(filters):
        raise NotImplementedException("iSignalFilterChecker.checkRemove")
    @staticmethod
    def checkMuteAll(e_global_mute):
        raise NotImplementedException("iSignalFilterChecker.checkMuteAll")
    @staticmethod
    def checkMute(filters):
        raise NotImplementedException("iSignalFilterChecker.checkMute")
    @staticmethod
    def checkQuery(filters):
        raise NotImplementedException("iSignalFilterChecker.checkQuery")
    @staticmethod
    def checkGlobalEnable(e_global_enable):
        raise NotImplementedException("iSignalFilterChecker.checkGlobalEnable")

