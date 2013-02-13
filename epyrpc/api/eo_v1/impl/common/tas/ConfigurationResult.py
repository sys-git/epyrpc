
from epyrpc.api.eo_v1.interfaces.common.tas.configuration.iConfigurationlResult import iConfigurationResult

class ConfigurationResult(iConfigurationResult):
    def __init__(self, config={}):
        self._config = config
    def config(self):
        return self.config()
    def export(self):
        return ConfigurationResult()
