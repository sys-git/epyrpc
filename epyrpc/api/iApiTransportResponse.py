
from epyrpc.api.iApiTransportItem import iApiTransportItemBase
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iApiTransportResponse(iApiTransportItemBase):
    r"""
    @summary: Used for asynchronous API responses.
    """
    def response(self):
        raise NotImplementedException("iApiTransportResponse.response")
