
class UnsupportedApiError(Exception):
    def __init__(self, who, ns):
        super(UnsupportedApiError, self).__init__(who, ns)
        self._who = who
        self._ns = ns
    def who(self):
        return self._who
    def ns(self):
        return self._ns
