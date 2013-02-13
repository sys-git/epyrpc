
from epyrpc.api.iApi import iApi
from exceptions.NotImplemented import NotImplementedException

class iPeersChecker(iApi):
    @staticmethod
    def checkAdd(i_a_peer):
        raise NotImplementedException("iSignalFilterChecker.checkAdd")
    @staticmethod
    def checkRemove(i_a_peer_remove):
        raise NotImplementedException("iSignalFilterChecker.checkRemove")
    @staticmethod
    def checkStats(i_peer_stats):
        raise NotImplementedException("iSignalFilterChecker.checkStats")
    @staticmethod
    def checkQuery(i_a_peer):
        raise NotImplementedException("iSignalFilterChecker.checkQuery")
    @staticmethod
    def checkQueryAll(filters):
        raise NotImplementedException("iSignalFilterChecker.checkQueryAll")

