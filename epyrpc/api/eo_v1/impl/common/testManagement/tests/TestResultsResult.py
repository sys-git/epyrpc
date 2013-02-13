
from epyrpc.api.eo_v1.interfaces.common.testManagement.tests.iTestResultsResult import \
    iTestResultsResult
import copy

_INDEX_PREFIX = u"INDEX"
_INDEX_PASS = u"pass"
_INDEX_FAIL = u"fail"
_INDEX_ERROR = u"error"
_INDEX_SKIP = u"skip"
_INDEX_TIMEDOUT = u"timeout"
_INDEX_DBUSERROR = u"DbusError"
_INDEX_DBUSNOREPLY = u"DbusNoReply"
_INDEX_DEADBOX = u"deadBox"
_INDEX_DEADSLAVECRASH = u"deadSlaveCrash"
_INDEX_SLAVECRASH = u"slaveCrash"
_INDEX_NOXML = u"noXml"
_INDEX_INVALIDXML = u"invalidXml"
_INDEX_INSUFFICIENTENV = u"insufficientEnv"
_INDEX_ENVSERVER = u"envServer"

_blankStats = { _INDEX_PASS:0,
                _INDEX_FAIL:0,
                _INDEX_ERROR:0,
                _INDEX_SKIP:0,
                _INDEX_TIMEDOUT:0,
                _INDEX_DBUSERROR:0,
                _INDEX_DBUSNOREPLY:0,
                _INDEX_DEADBOX:0,
                _INDEX_DEADSLAVECRASH:0,
                _INDEX_SLAVECRASH:0,
                _INDEX_NOXML:0,
                _INDEX_INVALIDXML:0,
                _INDEX_INSUFFICIENTENV:0,
                _INDEX_ENVSERVER:0,
               }

class TestResultsResult(iTestResultsResult):
    INDEX_PASS = _INDEX_PASS
    INDEX_FAIL = _INDEX_FAIL
    INDEX_ERROR = _INDEX_ERROR
    INDEX_SKIP = _INDEX_SKIP
    INDEX_TIMEDOUT = _INDEX_TIMEDOUT
    INDEX_DBUSERROR = _INDEX_DBUSERROR
    INDEX_DBUSNOREPLY = _INDEX_DBUSNOREPLY
    INDEX_DEADBOX = _INDEX_DEADBOX
    INDEX_DEADSLAVECRASH = _INDEX_DEADSLAVECRASH
    INDEX_SLAVECRASH = _INDEX_SLAVECRASH
    INDEX_NOXML = _INDEX_NOXML
    INDEX_INVALIDXML = _INDEX_INVALIDXML
    INDEX_INSUFFICIENTENV = _INDEX_INSUFFICIENTENV
    INDEX_ENVSERVER = _INDEX_ENVSERVER
    _indexes = []
    def __init__(self, stats=_blankStats, flush=False):
        self._stats = stats
        self._flush = None  #    Guarantee default value.
        self.flushed = flush
        if len(TestResultsResult._indexes) == 0:
            #    Calculate the available indexes:
            for i in dir(TestResultsResult):
                if i.isupper() and i.startswith(_INDEX_PREFIX):
                    TestResultsResult._indexes.append(i)
    def getItems(self):
        return self._indexes
    def stats(self):
        return self._stats
    def export(self):
        return TestResultsResult(copy.deepcopy(self._stats))
    @staticmethod
    def compute(tests, flush=False):
        r"""
        @summary: Compile the stats from an array of CachedTestDetails objects.
        @static-constructor.
        @type tests: dict.
        """

        from YouView.TAS.Master.Domain.Test.TestStates import TestState

        result = TestResultsResult(flush=flush)
        if tests == None:
            return result
        r""" Calculate stats... """
        #    #Modules, #Classes, #MaxIterations, #Invalids, #ManualInspection, #Envs:
        passes = fail = error = skip = timedout = dbusError = 0
        dbusNoReply = deadSlaveCrash = slaveCrash = deadBox = 0
        noXml = invalidXml = insufficientEnv = envServer = 0
        for t in tests.values():
            test = t.test()
            #    State:
            s = test.state
            if s == TestState.PASS():
                passes += 1
            if s == TestState.FAILURE():
                fail += 1
            if s == TestState.ERROR():
                error += 1
            if s == TestState.SKIP():
                skip += 1
            if s == TestState.TIMEOUT():
                timedout += 1
            if s == TestState.DBUS_ERROR():
                dbusError += 1
            if s == TestState.DBUS_NO_REPLY_ERROR():
                dbusNoReply += 1
            if s == TestState.DEAD_SLAVE_CRASH():
                deadSlaveCrash += 1
            if s == TestState.SLAVE_CRASH():
                slaveCrash += 1
            if s == TestState.NO_XML():
                noXml += 1
            if s == TestState.INVALID_XML():
                invalidXml += 1
            if s == TestState.INSUFFICIENT_ENV():
                insufficientEnv += 1
            if s == TestState.ENV_SERVER():
                envServer += 1
            if s == TestState.DEADBOX():
                deadBox += 1
        #    Set the stats:
        result.passes = passes
        result.fail = fail
        result.error = error
        result.skip = skip
        result.timedout = timedout
        result.dbusError = dbusError
        result.dbusNoReply = dbusNoReply
        result.deadSlaveCrash = deadSlaveCrash
        result.slaveCrash = slaveCrash
        result.noXml = noXml
        result.invalidXml = invalidXml
        result.insufficientEnv = insufficientEnv
        result.envServer = envServer
        result.deadBox = deadBox
        return result
    r""" SETTERS & GETTERS for properties: """
    def setFlushed(self, flush):
        if not isinstance(flush, bool):
            raise ValueError("flush must be a boolean, but got: %(F)s" % {"F":flush})
        self._flush = flush
    def setPass(self, total):
        self._setStats(TestResultsResult.INDEX_PASS, total)
    def setFail(self, total):
        self._setStats(TestResultsResult.INDEX_FAIL, total)
    def setError(self, total):
        self._setStats(TestResultsResult.INDEX_ERROR, total)
    def setSkip(self, total):
        self._setStats(TestResultsResult.INDEX_SKIP, total)
    def setTimedout(self, total):
        self._setStats(TestResultsResult.INDEX_TIMEDOUT, total)
    def setDbusError(self, total):
        self._setStats(TestResultsResult.INDEX_DBUSERROR, total)
    def setDbusNoReply(self, total):
        self._setStats(TestResultsResult.INDEX_DBUSNOREPLY, total)
    def setDeadBox(self, total):
        self._setStats(TestResultsResult.INDEX_DEADBOX, total)
    def setDeadSlaveCrash(self, total):
        self._setStats(TestResultsResult.INDEX_DEADSLAVECRASH, total)
    def setSlaveCrash(self, total):
        self._setStats(TestResultsResult.INDEX_SLAVECRASH, total)
    def setNoXml(self, total):
        self._setStats(TestResultsResult.INDEX_NOXML, total)
    def setInvalidXml(self, total):
        self._setStats(TestResultsResult.INDEX_INVALIDXML, total)
    def setInsufficientEnv(self, total):
        self._setStats(TestResultsResult.INDEX_INSUFFICIENTENV, total)
    def setEnvServer(self, total):
        self._setStats(TestResultsResult.INDEX_ENVSERVER, total)
    def getFlushed(self):
        return self._flush
    def getPass(self):
        return self._getStat(TestResultsResult.INDEX_PASS)
    def getFail(self):
        return self._getStat(TestResultsResult.INDEX_FAIL)
    def getError(self):
        return self._getStat(TestResultsResult.INDEX_ERROR)
    def getSkip(self):
        return self._getStat(TestResultsResult.INDEX_SKIP)
    def getTimedout(self):
        return self._getStat(TestResultsResult.INDEX_TIMEDOUT)
    def getDbusError(self):
        return self._getStat(TestResultsResult.INDEX_DBUSERROR)
    def getDbusNoReply(self):
        return self._getStat(TestResultsResult.INDEX_DBUSNOREPLY)
    def getDeadBox(self):
        return self._getStat(TestResultsResult.INDEX_DEADBOX)
    def getDeadSlaveCrash(self):
        return self._getStat(TestResultsResult.INDEX_DEADSLAVECRASH)
    def getSlaveCrash(self):
        return self._getStat(TestResultsResult.INDEX_SLAVECRASH)
    def getNoXml(self):
        return self._getStat(TestResultsResult.INDEX_NOXML)
    def getInvalidXml(self):
        return self._getStat(TestResultsResult.INDEX_INVALIDXML)
    def getInsufficientEnv(self):
        return self._getStat(TestResultsResult.INDEX_INSUFFICIENTENV)
    def getEnvServer(self):
        return self._getStat(TestResultsResult.INDEX_ENVSERVER)
    r""" PROPERTIES: """
    flushed = property(getFlushed, setFlushed)
    passes = property(getPass, setPass)
    fail = property(getFail, setFail)
    error = property(getError, setError)
    skip = property(getSkip, setSkip)
    timedout = property(getTimedout, setTimedout)
    dbusError = property(getDbusError, setDbusError)
    dbusNoReply = property(getDbusNoReply, setDbusNoReply)
    deadBox = property(getDeadBox, setDeadBox)
    deadSlaveCrash = property(getDeadSlaveCrash, setDeadSlaveCrash)
    slaveCrash = property(getSlaveCrash, setSlaveCrash)
    noXml = property(getNoXml, setNoXml)
    invalidXml = property(getInvalidXml, setInvalidXml)
    insufficientEnv = property(getInsufficientEnv, setInsufficientEnv)
    envServer = property(getEnvServer, setEnvServer)
    r""" MISC: """
    def _getStat(self, index):
        if index not in self._stats:
            raise KeyError("Cannot get stats for: %(W)s" % {"W":index})
        return self._stats[index]
    def _setStats(self, index, value):
        if value == None or value < 0:
            value = 0
        self._stats[index] = value
