
from epyrpc.api.ApiParamError import ApiParamError
from epyrpc.api.eo_v1.interfaces.checkers.testManagement.iTestsChecker import \
    iTestsChecker
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iATestId import \
    iATestId
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestStatsResult import \
    iTestStatsResult
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.Cache.primitives.CachedTestDetails import \
    CachedTestDetails
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.Cache.primitives.CachedTestMetadataDetails import \
    CachedTestMetadataDetails

class TestsChecker(iTestsChecker):
    r"""
    @summary: Check the params for the api.tas.testManagement.tests methods.
    """
    allowedTypes = [iATestId, list]
    @staticmethod
    def checkAbort(testIds):
        return TestsChecker._checkTestIds(testIds)
    @staticmethod
    def checkQueryTests(testIds):
        return TestsChecker._checkTestIds(testIds)
    @staticmethod
    def _checkTestIds(testIds):
        if not (isinstance(testIds, iATestId) or isinstance(testIds, list)):
            raise ApiParamError(testIds, TestsChecker.allowedTypes)
        args = []
        if isinstance(testIds, list):
            for i in testIds:
                if i != None:
                    args.append(TestsChecker._checkTestId(i))
        else:
            args.append(TestsChecker._checkTestId(testIds))
        if len(args) == 0:
            raise ApiParamError(testIds, TestsChecker.allowedTypes)
        return args
    @staticmethod
    def _checkTestId(testId):
        if not isinstance(testId, iATestId):
            raise ApiParamError(testId, TestsChecker.allowedTypes)
        return testId
    @staticmethod
    def checkNewTests(tests):
        if not isinstance(tests, dict):
            raise ApiParamError(tests, dict)
        for test in tests.values():
            if not isinstance(test, CachedTestDetails):
                raise ApiParamError(test, CachedTestDetails)
        return tests
    @staticmethod
    def checkStats(stats):
        if not isinstance(stats, iTestStatsResult):
            raise ApiParamError(stats, iTestStatsResult)
        return stats
    @staticmethod
    def checkTestStateChange(cachedTests):
        args = []
        if isinstance(cachedTests, CachedTestDetails):
            args = [cachedTests]
        elif isinstance(cachedTests, list):
            for i in cachedTests:
                if i != None:
                    if not isinstance(i, CachedTestDetails):
                        raise ApiParamError(i, CachedTestDetails)
                    args.append(i)
        else:
            raise ApiParamError(cachedTests, CachedTestDetails)
        return args
    @staticmethod
    def checkMetadata(metadata):
        if not isinstance(metadata, CachedTestMetadataDetails):
            raise ApiParamError(metadata, CachedTestDetails)
        return metadata

