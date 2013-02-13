
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestStatsResult import \
    iTestStatsResult
import copy
from epyrpc.api.eo_v1.impl.common.testManagement.NoStatError import NoStatError

_INDEX_PREFIX = u"INDEX"
_INDEX_TOTAL = u"total"
_INDEX_CLASSES = u"classes"
_INDEX_MODULES = u"modules"
_INDEX_MAXITERATIONS = u"maxIterations"
_INDEX_INVALIDS = u"invalids"
_INDEX_MANUALINSPECTION = u"manualInspection"
_INDEX_ENVIRONMENTS = u"environments"
_INDEX_MINTIMEOUT = u"minTimeout"
_INDEX_MAXTIMEOUT = u"maxTimeout"

_blankStats = { _INDEX_TOTAL:0,
                _INDEX_CLASSES:0,
                _INDEX_MODULES:0,
                _INDEX_MAXITERATIONS:0,
                _INDEX_INVALIDS:0,
                _INDEX_MANUALINSPECTION:0,
                _INDEX_ENVIRONMENTS:0,
                _INDEX_MINTIMEOUT:0,
                _INDEX_MAXTIMEOUT:0,
               }

class TestStatsResult(iTestStatsResult):
    INDEX_TOTAL = _INDEX_TOTAL
    INDEX_CLASSES = _INDEX_CLASSES
    INDEX_MODULES = _INDEX_MODULES
    INDEX_MAXITERATIONS = _INDEX_MAXITERATIONS
    INDEX_INVALIDS = _INDEX_INVALIDS
    INDEX_MANUALINSPECTION = _INDEX_MANUALINSPECTION
    INDEX_ENVIRONMENTS = _INDEX_ENVIRONMENTS
    INDEX_MINTIMEOUT = _INDEX_MINTIMEOUT
    INDEX_MAXTIMEOUT = _INDEX_MAXTIMEOUT
    _indexes = []
    def __init__(self, stats=_blankStats, flush=False):
        self._stats = stats
        self._flush = None  #    Guarantee default value.
        self.flushed = flush
        #    Set defaults:
        self.modules = 0
        self.classes = 0
        self.maxInterations = 0
        self.invalids = 0
        self.manualInspections = 0
        self.environmens = 0
        self.maxTimeout = 0
        self.minTimeout = 0
        if len(TestStatsResult._indexes) == 0:
            #    Calculate the available indexes:
            for i in dir(TestStatsResult):
                if i.isupper() and i.startswith(_INDEX_PREFIX):
                    TestStatsResult._indexes.append(i)
    def getItems(self):
        return self._indexes
    def stats(self):
        return self._stats
    def export(self):
        return TestStatsResult(copy.deepcopy(self._stats))
    @staticmethod
    def compute(tests, flush=False):
        r"""
        @summary: Compile the stats from an array of CachedTestDetails objects.
        @static-constructor.
        @type tests: dict.
        """
        result = TestStatsResult(flush=flush)
        if tests == None:
            result.total = 0
            return result
        r""" Calculate stats... """
        #    #Total tests:
        result.total = len(tests.keys())
        #    Only generate other stats if we have any tests (setters will raise Exceptions otherwise).
        if result.total > 0:
            #    #Modules, #Classes, #MaxIterations, #Invalids, #ManualInspection, #Envs:
            modules = []
            classes = []
            iterCount = 0
            invalidCount = 0
            manInspCount = 0
            envs = []
            timeouts = {}
            for t in tests.values():
                test = t.test()
                #    Class:
                testClass = test.testClass
                if testClass != None and testClass not in classes:
                    classes.append(testClass)
                #    Module:
                testFile = test.testFile
                if testFile != None and testFile not in modules:
                    modules.append(testFile)
                #    Iterations:
                iterCount = min(0, max(iterCount, test.iterations))
                #    Invalid:
                invalidCount += (0 or test.invalid)
                #    Manual Inspection:
                manInspCount += (0 or test.manualInspection)
                #    Environment:
                env = test.environment
                if env != None and env not in envs:
                    envs.append(env)
                #    Timeouts:
                tout = test.testTimeout
                timeouts[tout] = 1
            tKeys = timeouts.keys()
            tKeys.sort()
            #    Max timeout is easy (>='0' or 'None'):
            tMax = tKeys[-1]
            #    Min timeout is ('None' or 1st >='0'-non-'None')
            tMin = tKeys[0]
            if (tMin == None) and (len(tKeys) > 0):
                tMin = tKeys[1]
            #    Set the stats:
            result.modules = len(modules)
            result.classes = len(classes)
            result.maxInterations = iterCount
            result.invalids = invalidCount
            result.manualInspections = manInspCount
            result.environmens = len(envs)
            result.maxTimeout = tMax
            result.minTimeout = tMin
        return result
    r""" SETTERS & GETTERS for properties: """
    def setFlushed(self, flush):
        if not isinstance(flush, bool):
            raise ValueError("flush must be a boolean, but got: %(F)s" % {"F":flush})
        self._flush = flush
    def setTotal(self, total):
        self._setStats(TestStatsResult.INDEX_TOTAL, total)
    def setClasses(self, total):
        self._setStats(TestStatsResult.INDEX_CLASSES, total)
    def setModules(self, total):
        self._setStats(TestStatsResult.INDEX_MODULES, total)
    def setIterations(self, total):
        self._setStats(TestStatsResult.INDEX_MAXITERATIONS, total)
    def setInvalids(self, total):
        self._setStats(TestStatsResult.INDEX_INVALIDS, total)
    def setManualInspections(self, total):
        self._setStats(TestStatsResult.INDEX_MANUALINSPECTION, total)
    def setEnvironments(self, total):
        self._setStats(TestStatsResult.INDEX_ENVIRONMENTS, total)
    def setMinTimeout(self, total):
        self._setStats(TestStatsResult.INDEX_MINTIMEOUT, total)
    def setMaxTimeout(self, total):
        self._setStats(TestStatsResult.INDEX_MAXTIMEOUT, total)
    def getFlushed(self):
        return self._flush
    def getTotal(self):
        return self._getStat(TestStatsResult.INDEX_TOTAL)
    def getClasses(self):
        return self._getStat(TestStatsResult.INDEX_CLASSES)
    def getModules(self):
        return self._getStat(TestStatsResult.INDEX_MODULES)
    def getIterations(self):
        return self._getStat(TestStatsResult.INDEX_MAXITERATIONS)
    def getInvalids(self):
        return self._getStat(TestStatsResult.INDEX_INVALIDS)
    def getManualInspections(self):
        return self._getStat(TestStatsResult.INDEX_MANUALINSPECTION)
    def getEnvironments(self):
        return self._getStat(TestStatsResult.INDEX_ENVIRONMENTS)
    def getMinTimeout(self):
        return self._getStat(TestStatsResult.INDEX_MINTIMEOUT)
    def getMaxTimeout(self):
        return self._getStat(TestStatsResult.INDEX_MAXTIMEOUT)
    r""" PROPERTIES: """
    flushed = property(getFlushed, setFlushed)
    total = property(getTotal, setTotal)
    classes = property(getClasses, setClasses)
    modules = property(getModules, setModules)
    maxIterations = property(getIterations, setIterations)
    invalids = property(getInvalids, setInvalids)
    manualInspections = property(getManualInspections, setManualInspections)
    environments = property(getEnvironments, setEnvironments)
    maxTimeout = property(getMaxTimeout, setMaxTimeout)
    minTimeout = property(getMinTimeout, setMinTimeout)
    r""" MISC: """
    def _getStat(self, index):
        if index not in self._stats:
            raise KeyError("Cannot get stats for: %(W)s" % {"W":index})
        return self._stats[index]
    def _setStats(self, index, value):
        if value == None or value < 0:
            value = 0
        self._stats[index] = value
