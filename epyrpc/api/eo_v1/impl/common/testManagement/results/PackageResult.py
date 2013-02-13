
from epyrpc.api.eo_v1.interfaces.common.testManagement.results.iPackageResult import iPackageResult

class PackageResult(iPackageResult):
    def __init__(self):
        pass
    def export(self):
        return PackageResult()
