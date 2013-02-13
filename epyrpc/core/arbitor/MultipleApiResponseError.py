
class MultipleApiResponseError(Exception):
    def __init__(self, ns="", count=0, results=[]):
        super(MultipleApiResponseError, self).__init__()
        self._ns = ns
        self._results = results
        self._count = count
        l = len(self._results)
        if l > 0:
            self._count = l
    def results(self):
        return self._results
    def ns(self):
        return self._ns
    def count(self):
        return self._count
    def __str__(self):
        s = ["MultipleApiResponseError(ns: '%(NS)s') - Got %(C)s results: %(R)s" % {"NS":self._ns, "C":self._count, "R":self._results}]
        return " ".join(s)
