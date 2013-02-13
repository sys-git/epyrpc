
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException
from epyrpc.api.iApi import iApi

class iUserData(iApi):
    def overwrite(self, data):
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
        raise NotImplementedException("iUserData.overwrite")
    def update(self, data):
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
        raise NotImplementedException("iUserData.update")
    def clear(self, data):
        r"""
        @summary: Clear (remove) the given UserData.
        @param data: The data to remove from UserData.
        @return: UserDataResult.
        @attention: If a given UserData key does not exist in UserData, the returned 
        value for this key will be equal to 'UserDataNoValueError'. For a successful
        clear, the key is not returned.
        @raise iApiParamError: Error in parameters.
        @raise UserDataError: Unable to clear the UserData (ie: storage limit exceeded).
        """
        raise NotImplementedException("iUserData.clear")
    def clearAll(self):
        r"""
        @summary: Clear (remove) ALL the UserData.
        @return: None.
        @raise UserDataError: Unable to clear all the UserData (ie: storage limit exceeded).
        """
        raise NotImplementedException("iUserData.clearAll")
    def retrieve(self, data):
        r"""
        @summary: Retrieve the given UserData.
        @param data: The data to retrieve from UserData.
        @attention: If a given UserData key does not exist in UserData, the returned 
        value for this key will be equal to 'UserDataNoValueError'. For a successful
        clear, the key is returned.
        @return: UserDataResult.
        @raise iApiParamError: Error in parameters.
        @raise UserDataError: Unable to retrieve the UserData (ie: storage corrupted).
        """
        raise NotImplementedException("iUserData.retrieve")
    def retrieveAll(self, data):
        r"""
        @summary: Retrieve ALL the UserData.
        @return: UserDataResult.
        @raise UserDataError: Unable to retrieve the UserData (ie: storage corrupted).
        """
        raise NotImplementedException("iUserData.retrieveAll")

