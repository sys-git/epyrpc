
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilters import iFilters
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iSignalFilterStatus import iSignalFilterStatus

class Filters(iFilters):
    def __init__(self, status, filters={}):
        if not isinstance(status, iSignalFilterStatus):
            raise ApiParamError(status, iSignalFilterStatus)
        if not isinstance(filters, dict):
            raise ApiParamError(filters, dict)
        self._status = status
        self._filters = filters
    def status(self):
        return self._status
    def filters(self):
        return self._filters
