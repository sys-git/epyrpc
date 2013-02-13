
from epyrpc.api.iApiData import iApiData
from epyrpc.eExceptions.NotImplemented import NotImplementedException

class iConfigurationResult(iApiData):
    def config(self):
        raise NotImplementedException("iConfigurationResult.config")
