
from epyrpc.utils.ErrorUtils import importModule
from epyrpc.utils.synchronisation.IncompleteTransactionError import \
    IncompleteTransactionError

class PartialResponse(object):
    def __init__(self, initialResponse):
        self._tId = initialResponse.tId()
        self._combinerMethod = initialResponse.combinerMethod()
        self._numChunks = initialResponse.numChunks()
        self._responses = {0: initialResponse.response()}
    def update(self, response):
        if self._tId != response.tId():
            raise ValueError("Partial response contains different tId: %(T)s, expecting: %(E)s." % {"T":response.tId(), "E":self._tId}) 
        if self._numChunks != response.numChunks():
            raise ValueError("Partial response contains different numChunks: %(T)s, expecting: %(E)s." % {"T":response.numChunks(), "E":self._numChunks}) 
        if self._combinerMethod != response.combinerMethod():
            raise ValueError("Partial response contains different combinerMethod: %(T)s, expecting: %(E)s." % {"T":response.combinerMethod(), "E":self._combinerMethod}) 
        index = response.index()
        if index in self._responses.keys():
            raise ValueError("Partial response index already received: %(I)s." % {"I":index})
        if index >= self._numChunks:
            raise ValueError("Partial response index too big: %(I)s, expecting %(E)s chunks." % {"I":index, "E":self._numChunks})
        if index < 1:
            raise ValueError("Partial response index too small: %(I)s, expecting >= 1." % {"I":index})
        self._responses[index] = response.response()
        #    Now attempt the decode:
        return self._decode()
    def check(self):
        return self._check()
    def _check(self):
        howMany = len(self._responses.keys())
        if howMany != self._numChunks:
            raise IncompleteTransactionError("Received %(R)s chunks out of %(E)s" % {"R":howMany, "E":self._numChunks})
    def _decode(self):
        self._check()
        #    Have we got a complete response? If so, return it!
        result = self._callCombinerMethod(self._combinerMethod, self._responses)
        return result
    def _callCombinerMethod(self, method, data):
        #    The combiner is a class with no constructor with a __call__(data) method.
        if method != None:
            (toImport, cls) = method
            try:
                inst = importModule(toImport, cls)
            except Exception, _e:
                raise
            else:
                result = inst()(data)
                return result
        return data
