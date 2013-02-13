
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestPacks import \
    iTestPacks

class TestPacks(iTestPacks):
    #    FIXME!
    def export(self):
        return TestPacks()
