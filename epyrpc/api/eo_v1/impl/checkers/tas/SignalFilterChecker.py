
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.enums.eGlobalEnable import eGlobalEnable
from epyrpc.api.eo_v1.enums.eMute import eMute
from epyrpc.api.eo_v1.impl.common.tas.signalFilter.Range import Range
from epyrpc.api.eo_v1.interfaces.checkers.tas.iSignalFilterChecker import \
    iSignalFilterChecker
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterId import iFilterId
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iLocation import iLocation
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iNamespace import \
    iNamespace
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iRange import iRange

class SignalFilterChecker(iSignalFilterChecker):
    r"""
    @summary: Check the params for the api.tas.signalFilter methods.
    """
    @staticmethod
    def checkAdd(namespace):
        if not (isinstance(namespace, iNamespace) or isinstance(namespace, list)):
            raise ApiParamError(namespace, [iNamespace, list])
        args = []
        if isinstance(namespace, list):
            for i in namespace:
                if i != None:
                    args.append(SignalFilterChecker._checkNamespace(i))
        else:
            args.append(SignalFilterChecker._checkNamespace(namespace))
        return args
    @staticmethod
    def checkRemove(filters):
        if not (isinstance(filters, iFilterId) or isinstance(filters, iNamespace) or isinstance(filters, list)):
            raise ApiParamError(filters, [iFilterId, iNamespace, list])
        args = []
        if isinstance(filters, list):
            for i in filters:
                if i != None:
                    args.append(SignalFilterChecker._checkAFilter(i))
        else:
            args.append(SignalFilterChecker._checkAFilter(filters))
        return args
    @staticmethod
    def checkMuteAll(e_global_mute):
        if not eMute.isValid(e_global_mute):
            raise ApiParamError(e_global_mute, eMute)
        return e_global_mute
    @staticmethod
    def checkMute(filters):
        if not (isinstance(filters, tuple) or isinstance(filters, list)):
            raise ApiParamError(filters, [iFilterId, iNamespace, list])
        args = []
        if isinstance(filters, list):
            for i in filters:
                if i != None:
                    args.append(SignalFilterChecker._checkFilter(i))
        else:
            args.append(SignalFilterChecker._checkFilter(filters))
        if len(args) == 0:
            raise ApiParamError(filters, [iFilterId, iNamespace, list])
        return args
    @staticmethod
    def checkQuery(filters):
        if not (isinstance(filters, iFilterId) or isinstance(filters, iNamespace) or isinstance(filters, list)):
            raise ApiParamError(filters, [iFilterId, iNamespace, list])
        args = []
        if isinstance(filters, list):
            for i in filters:
                if i != None:
                    args.append(SignalFilterChecker._checkAFilter(i))
        else:
            args.append(SignalFilterChecker._checkAFilter(filters))
        if len(args) == 0:
            raise ApiParamError(filters, [iFilterId, iNamespace, list])
        return args
    @staticmethod
    def checkGlobalEnable(e_global_enable):
        if not eGlobalEnable.isValid(e_global_enable):
            raise ApiParamError(e_global_enable, eGlobalEnable)
        return e_global_enable
    @staticmethod
    def _checkNamespace(namespace):
        if not isinstance(namespace, iNamespace):
            raise ApiParamError(namespace, iNamespace)
        return namespace
    @staticmethod
    def _checkFilter(i):
        try:
            (fltr, mute) = i
        except:
            raise ApiParamError(i, tuple)
        else:
            SignalFilterChecker._checkAFilter(fltr)
            if not eMute.isValid(mute):
                raise ApiParamError(mute, eMute)
        return i
    @staticmethod
    def _checkAFilter(fltr):
        if not (isinstance(fltr, iFilterId) or (isinstance(fltr, iNamespace))):
            raise ApiParamError(fltr, [iFilterId, iNamespace])
        return fltr
    @staticmethod
    def checkArchive(i_location):
        if i_location == None:
            return
        elif not isinstance(i_location, iLocation):
            raise ApiParamError(i_location, iLocation)
        return i_location
    @staticmethod
    def checkRetrieve(theRange):
        if theRange == None:
            return Range()
        elif not isinstance(theRange, iRange):
            raise ApiParamError(theRange, iRange)
        return theRange




