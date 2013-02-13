
from YouView.TAS.Master.MasterBusinessLogic.Utils.Interfaces import Interface
from YouView.TAS.Common.Exceptions.NotImplemented import NotImplementedException

class iRange(Interface):
    def start(self):
        r"""
        @summary: Retrieve the start of range.
        """
        raise NotImplementedException("iRange.end")
    def end(self):
        r"""
        @summary: Retrieve the end of range.
        """
        raise NotImplementedException("iRange.end")
    def chunkSize(self):
        r"""
        @summary: Retrieve the chunksize for retrieval.
        """
        raise NotImplementedException("iRange.chunkSize")
    def userData(self):
        r"""
        @summary: Retrieve the userData which can be used to identify this request.
        """
        raise NotImplementedException("iRange.userData")
