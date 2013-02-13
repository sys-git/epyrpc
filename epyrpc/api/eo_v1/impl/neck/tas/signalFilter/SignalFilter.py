
from epyrpc.api.eo_v1.impl.checkers.tas.SignalFilterChecker import \
    SignalFilterChecker
from epyrpc.api.eo_v1.interfaces.neck.tas.signalFilter.iSignalFilter import \
    iSignalFilter
from YouView.TAS.Master.MasterBusinessLogic.ExecutionOrganiser.ExecutionOrganiser import \
    ExecutionOrganiser
import pickle

class SignalFilter(iSignalFilter):
    r"""
    Handlers are preceded with '_handler_'.
    In theory, you could have a symmetrical API all in the same iApi file as the Head (if we
    wanted the head to be able to talk to it's ExecutionOrganiser (if it had one that we wanted
    to export to the Neck!)
    Handlers MUST obey the IPC iIpcTransportDataReceiveListener.transportDataReceive contract.
    @attention: All return objects are either native types, Exceptions or iApiData.
    @attention: The return type must be PICKLABLE!
    """
    def __init__(self, ns="", solicited=False):
        super(SignalFilter, self).__init__(ns=ns, solicited=solicited)
    """ HANDLERS: """
    def _handler_add(self, tId, bSynchronous, i_namespaces):
        i_namespaces = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkAdd, i_namespaces)
        def _add(i_namespaces):
            #    Make the operation atomic:
            result = {}
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                for i_namespace in i_namespaces:
                    try:
                        addedResult = sf.add(i_namespace)
                    except Exception, addedResult:
                        #    The exception goes directly into the return result object.
                        pass
                    result[i_namespace.id_()] = addedResult
            return (result, sf.status())
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _add(x), i_namespaces)
    def _handler_remove(self, tId, bSynchronous, filters):
        filters = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkRemove, filters)
        def _remove(filters):
            #    Make the operation atomic:
            result = {}
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                for fltr in filters:
                    id_ = fltr.id_()
                    try:
                        removeResult = sf.remove(fltr)
                    except Exception, removeResult:
                        #    The exception goes directly into the return result object.
                        pass
                    result[id_] = removeResult
                return (result, sf.status())
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _remove(x), filters)
    def _handler_removeAll(self, tId, bSynchronous):
        def _removeAll():
            #    Make the operation atomic:
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                sf.removeAll()
                return sf.status()
        return self._handleStandardCall(tId, bSynchronous, _removeAll)
    def _handler_muteAll(self, tId, bSynchronous, e_global_mute):
        e_global_mute = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkMuteAll, e_global_mute)
        def _globalMute(e_global_mute):
            sf = ExecutionOrganiser().signalFilters()
            sf.globalMute(e_global_mute)
            return sf.status()
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _globalMute(x), e_global_mute)
    def _handler_mute(self, tId, bSynchronous, filters):
        filters = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkMute, filters)
        def _mute(filters):
            result = {}
            #    Make the operation atomic:
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                for fltr in filters:
                    try:
                        i_a_signal_filter = sf.mute(fltr)
                    except Exception, i_a_signal_filter:
                        #    The exception goes directly into the return result object.
                        pass
                    result[fltr[0].id_()] = i_a_signal_filter
                return (result, sf.status())
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _mute(x), filters)
    def _handler_query(self, tId, bSynchronous, filters):
        filters = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkQuery, filters)
        def _query(filters):
            result = {}
            #    Make the operation atomic:
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                for fltr in filters:
                    try:
                        i_a_signal_filter = sf.query(fltr)
                    except Exception, i_a_signal_filter:
                        #    The exception goes directly into the return result object.
                        pass
                    result[fltr.id_()] = i_a_signal_filter
            return (result, sf.status())
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _query(x), filters)
    def _handler_queryAll(self, tId, bSynchronous):
        def _queryAll():
            result = {}
            #    Make the operation atomic:
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                #    Get all the current filters...
                filters = sf.queryAll()
                #    Convert the list into a dict:{filterId:filter)
                for fltr in filters:
                    result[fltr.fId()] = fltr
            return (result, sf.status())
        return self._handleStandardCall(tId, bSynchronous, _queryAll)
    def _handler_globalEnable(self, tId, bSynchronous, e_global_enable):
        e_global_enable = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkGlobalEnable, e_global_enable)
        def _globalEnable(e_global_enable):
            sf = ExecutionOrganiser().signalFilters()
            sf.globalEnable(e_global_enable)
            return sf.status()
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _globalEnable(x), e_global_enable)
    def _handler_status(self, tId, bSynchronous):
        sf = ExecutionOrganiser().signalFilters()
        return self._handleStandardCall(tId, bSynchronous, sf.status)
    def _handler_archive(self, tId, bSynchronous, i_location):
        i_location = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkArchive, i_location)
        def _archive(i_location):
            #    Make the operation atomic:
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                result = sf.archive(i_location)
            return (result, sf.status())
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _archive(x), i_location)
    def _handler_retrieve(self, tId, bSynchronous, i_range):
        i_range = self._handleStandardCheck(tId, bSynchronous, SignalFilterChecker.checkRetrieve, i_range)
        def _retrieve(i_range):
            sf = ExecutionOrganiser().signalFilters()
            with sf.lock():
                #    This could be massive, so split it into i_range.chunkSize()
                signals = sf.retrieve(i_range)
            numSignals = len(signals)
            if numSignals == 0:
                return (i_range, signals, sf.status())
            chunks = []
            dump = pickle.dumps(signals)
            chunkSize = i_range.chunkSize()
            if len(dump) > chunkSize:
                #    split it into approx chunks:
                meanSignalSize = len(dump) / len(signals)
                numSignalsPerChunk = max(1, (chunkSize / meanSignalSize))  #    Rounded-down.
                signalCount = 0
                while signalCount < numSignals:
                    signalsRemaining = (numSignals - signalCount)
                    chunkSize = min(signalsRemaining, numSignalsPerChunk)
                    item = signals[signalCount:(signalCount + chunkSize)]
                    chunks.append(item)
                    signalCount += chunkSize
                #    Now send all the chunks...
                return self._returnChunks(tId, chunks, ("Ipc.api.eo_v1.impl.combiners.tas.SignalFilterCombiner", "SignalFilterCombiner"), lambda x, index: (i_range, x[index]))
            else:
                return (i_range, signals)
        return self._handleStandardCall(tId, bSynchronous, lambda(x): _retrieve(x), i_range)

