
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterId import iFilterId
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterIdentifier import iFilterIdentifier

class FilterId(iFilterId):
    def __init__(self, id_):
        if not (isinstance(id_, int) or (isinstance(id_, basestring))):
            raise ApiParamError(id_, [int, basestring])
        if not isinstance(id_, basestring):
            id_ = ("fid_%(ID)s" % {"ID":iFilterIdentifier.nId.next()})
        self._id = id_
    def id_(self):
        return self._id
    def export(self):
        fId = FilterId(0)
        fId._id = self._id
        return fId
    def __eq__(self, other):
        if isinstance(other, iFilterId):
            if other.id_() == self.id_():
                return True
        return False
