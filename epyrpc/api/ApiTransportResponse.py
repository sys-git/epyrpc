
from epyrpc.api.iApiTransportResponse import iApiTransportResponse

class ApiTransportResponse(iApiTransportResponse):
    def __init__(self, response):
        self._response = response
    def response(self):
        return self._response
    @staticmethod
    def decode(response):
        if isinstance(response, ApiTransportResponse):
            #    Decode a ApiTransportResponse (sent via 'iApi.sendAsyncResponse()':
            response = response.response()
        return response
