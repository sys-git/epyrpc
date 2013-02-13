from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iUserDataError(Exception):
    r"""
    @summary: UserData cannot be manipulated or queried due to a fault
    independent of the data.
    """
    def error(self):
        r"""
        @summary: The error.
        """
        raise NotImplementedException("iUserDataError.error")
