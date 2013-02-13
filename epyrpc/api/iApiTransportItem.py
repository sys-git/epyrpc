
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iApiTransportItemBase(object):
    pass

class iApiTransportItem(iApiTransportItemBase):
    r"""
    @summary: All API objects pass over the IPC encapsulated within this.
    """
    def ns(self):
        raise NotImplementedException("iApiTransportItem.ns")
    def args(self):
        raise NotImplementedException("iApiTransportItem.args")
    def kwargs(self):
        raise NotImplementedException("iApiTransportItem.kwargs")
