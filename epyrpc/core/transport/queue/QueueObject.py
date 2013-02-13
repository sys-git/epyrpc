
class QueueObject(object):
    def __init__(self, data, format_):
        self._data = data
        self._format = format_
    def data(self):
        return self._data
    def getFormat(self):
        return self._format
