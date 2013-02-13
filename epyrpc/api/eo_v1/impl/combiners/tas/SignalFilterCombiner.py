
from epyrpc.api.eo_v1.interfaces.combiners.tas.iSignalFilterCombiner import \
    iSignalFilterCombiner

class SignalFilterCombiner(iSignalFilterCombiner):
    @staticmethod
    def __call__(theDict):
        r"""
        @summary: Combine multiple transaction return values into a single return type as expected
        by the caller:    tuple: (i_range, signals)
        @param theDict: Dictionary{integer__part_starts_at_zero, thePart}.
        @attention: Returns a list of ordered-in-time signals.
        """
        keys = theDict.keys()
        keys.sort()
        allSignals = []
        for part in keys:
            (i_range, signals) = theDict[part]
            allSignals.extend(signals)
        return (i_range, allSignals)




