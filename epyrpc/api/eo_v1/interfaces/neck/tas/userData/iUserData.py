
from epyrpc.api.iApi import iApi
from epyrpc.exceptions.NotImplemented import NotImplementedException

class iUserData(iApi):
    r"""
    @summary: This mirrors the iUserData class to provide handlers
    for the corresponding methods in iUserData.
    @param tId: TransactionId.
    @param bSynchronous: True - method is being run synchronously and should
    return synchronously, False - otherwise.
    """
    def _handler_overwrite(self, tId, bSynchronous, data):
        r"""
        @summary: Overwrite ALL UserData with the given data.
        @param data: The data to blat UserData with.
        @return: UserDataResult.
        @attention: If a given UserData key cannot be stored in UserData, 
        the returned value for this key will be equal to 'UserDataStoreError'.
        For a successful store, the key is not returned.
        @raise iApiParamError: Error in parameters.
        @raise UserDataError: Unable to clear the UserData (ie: storage limit exceeded).
        """
        raise NotImplementedException("iUserData._handler_overwrite")
    def _handler_update(self, tId, bSynchronous, data):
        r"""
        @summary: Freshen and Update the UserData.
        @param data: The data to write to UserData.
        @return: UserDataResult.
        @attention: If a given UserData key cannot be stored in UserData, 
        the returned value for this key will be equal to 'UserDataStoreError'.
        For a successful store, the key is not returned.
        @raise iApiParamError: Error in parameters.
        @raise UserDataError: Unable to clear the UserData (ie: storage limit exceeded).
        """
        raise NotImplementedException("iUserData._handler_update")
    def _handler_clear(self, tId, bSynchronous, data):
        r"""
        @summary: Clear (remove) the given UserData.
        @param data: The data to remove from UserData.
        @return: UserDataResult.
        @attention: If a given UserData key does not exist in UserData, the returned 
        value for this key will be equal to 'UserDataNoValueError'. For a successful
        clear, the key is not returned
        @raise iApiParamError: Error in parameters.
        @raise UserDataError: Unable to clear the UserData (ie: storage limit exceeded).
        """
        raise NotImplementedException("iUserData._handler_clear")
    def _handler_clearAll(self, tId, bSynchronous):
        r"""
        @summary: Clear (remove) ALL the UserData.
        @return: None.
        @raise UserDataError: Unable to clear all the UserData (ie: storage limit exceeded).
        """
        raise NotImplementedException("iUserData._handler_clearAll")
    def _handler_retrieve(self, tId, bSynchronous, data):
        r"""
        @summary: Retrieve the given UserData.
        @param data: The data to retrieve from UserData.
        @attention: If a given UserData key does not exist in UserData, the returned 
        value for this key will be equal to 'UserDataNoValueError'.
        @return: UserDataResult.
        @raise UserDataError: Unable to retrieve the UserData (ie: storage corrupted).
        """
        raise NotImplementedException("iUserData._handler_retrieve")
    def _handler_retrieveAll(self, tId, bSynchronous):
        r"""
        @summary: Retrieve ALL the UserData.
        @return: UserDataResult.
        @raise UserDataError: Unable to retrieve the UserData (ie: storage corrupted).
        """
        raise NotImplementedException("iUserData._handler_retrieveAll")
