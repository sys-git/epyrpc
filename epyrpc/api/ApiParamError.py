
from epyrpc.api.iApiParamError import iApiParamError

class ApiParamError(iApiParamError):
    def __init__(self, item, allowedTypes=[], allowedValues=[]):
        self.item = item
        if (allowedTypes != None) and (not isinstance(allowedTypes, list)):
            allowedTypes = [allowedTypes]
        if (allowedValues != None) and (not isinstance(allowedValues, list)):
            allowedValues = [allowedValues]
        self.allowedTypes = allowedTypes
        self.allowedValues = allowedValues
