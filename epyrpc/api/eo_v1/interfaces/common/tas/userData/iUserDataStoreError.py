
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iUserDataStoreError(Exception):
    r"""
    @summary: A UserData key cannot be manipulated or queried due to a fault
    dependent on the data (ie: cannot be serialised etc).
    """
    def key(self):
        r"""
        @summary: The UserData key which is in error.
        """
        raise NotImplementedException("iUserDataStoreError.key")
    def error(self):
        r"""
        @summary: The error.
        """
        raise NotImplementedException("iUserDataStoreError.error")
