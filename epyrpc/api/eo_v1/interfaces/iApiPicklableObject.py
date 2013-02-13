from epyrpc.exceptions.NotImplemented import NotImplementedException

class iApiPicklableObject(object):
    r"""
    All API objects which are sent over the IPC must implement this interface.
    """
    def export(self):
        r"""
        @summary: Recursively export ourselves in a picklable state.
        @return: A copy of ourselves with all non-relevant and non-picklable attributes removed.
        """
        raise NotImplementedException("iApiPicklableObject.export")
