
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iUserDataNoValueError(Exception):
    r"""
    @summary: The key does not exist in UserData.
    """
    def key(self):
        r"""
        @summary: The UserData key which is in error.
        """
        raise NotImplementedException("iUserDataNoValueError.key")
