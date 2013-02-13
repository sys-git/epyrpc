
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iFilterIdentifier import \
    iFilterIdentifier
from epyrpc.api.eo_v1.interfaces.common.tas.signalFilter.iNamespace import \
    iNamespace

class Namespace(iNamespace):
    def __init__(self, namespace=None, regx=None, _nId=None, direction=eFilterDirection.IN):
        if namespace == None:
            if not (isinstance(regx, basestring) or (isinstance(regx, iNamespace))):
                raise ApiParamError((namespace, regx), [basestring, iNamespace])
            if isinstance(regx, iNamespace):
                #    Copy-constructor:
                self._namespace = namespace.namespace()
                self._regx = namespace.isRegx()
                _nId = namespace.id_()
            self._namespace = regx
            self._regx = True
        elif regx == None:
            if not (isinstance(namespace, basestring) or (isinstance(namespace, iNamespace))):
                raise ApiParamError((namespace, regx), [basestring, iNamespace])
            if isinstance(namespace, iNamespace):
                #    Copy-constructor:
                self._namespace = namespace.namespace()
                self._regx = namespace.isRegx()
                _nId = namespace.id_()
            else:
                self._namespace = namespace
                self._regx = False
        self.setDirection(direction)
        if _nId == None:
            _nId = "ns_%(NS)s_(%(D)s)" % {"NS":iFilterIdentifier.nId.next(), "D":eFilterDirection.enumerateAttributes(self._direction)}
        self._nId = _nId
    def export(self):
        ns = self.namespace()
        regx = self.isRegx()
        if regx == False:
            regx = None
            namespace = ns
        else:
            regx = ns
            namespace = None
        return Namespace(namespace=namespace, regx=regx, _nId=self.id_(), direction=self.direction())
    def isRegx(self):
        r"""
        @summary: Determine if the namespace is a regx expression.
        @return: True - is regx, False - otherwise.
        """
        try:
            return self._regx
        except Exception, _e:
            pass
    def namespace(self):
        return self._namespace
    def compare(self, other, ignoreDirection=False):
        if not isinstance(other, iNamespace):
            return False
        if other.isRegx() != self.isRegx():
            return False
        if other.namespace() != self.namespace():
            return False
        if ignoreDirection == False:
            if other.direction() != self.direction():
                return False
        return True
    def id_(self):
        return self._nId
    def setDirection(self, e_filter_direction=eFilterDirection.IN):
        if eFilterDirection.lookupEnumerationValue(e_filter_direction) == None:
            raise ApiParamError(e_filter_direction, eFilterDirection)
        self._direction = e_filter_direction
    def direction(self):
        return self._direction




