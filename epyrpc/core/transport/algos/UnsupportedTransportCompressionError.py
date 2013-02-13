
class UnsupportedTransportCompressionError(Exception):
    def __init__(self, algo):
        self._algo = algo
    def algo(self):
        return self._algo
