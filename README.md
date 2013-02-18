epyrpc
======

Object based pure Python RPC for inter-process communications.

Inter-process RPC exposed over an interface (currently supported: multiprocessing.queue) as hierarchical object
based api.
Full suport for synchronous (blocking with timeout) / asynchronous (both with timeout: callback, semaphore release), both solicited
and non-solicited data (events).
All RPC is heirarchical dot seperated namespace based, with generic handlers for unhandled api methods which 
can be overridden.
The receiving api can chose which methods to handle, non-handled methods will automatically raise an exception at
the caller.
Receiver APIs can have hard-coded handler methods, or a reciever can register handler methods on an api to be
called when an api request is received for a namespace which isn't handled.
APIs can be dynamically created (ie: from config) although this is still to be done, but as long as the api's inherit
from a particular superclass and obey particular rules then they can be created/destroyed ad infenitum over the
lifetime of a given transport.
An api has default values for timeout, solicited, sync / non-sync (callback or semaphore)
If the called api yields an exception, then the caller receives the exception as a raised exception (blocking call)
or as an exception object as the result in an asynchronous callback.
Asynchronous calls return an AsyncResult object which can be held by the caller and queried for it's current status.
All solicited api calls result in a new transaction being created in their respective transactionManagers. Each
transactionManager has a unique format which allows it to determine if a transaction originated from its self or another
transactionManager.
Transactions are retired by the transactionManager's thread-safe synchroniser which then result in the synchronous
or asynchronous api call completing.

It sounds a lot but is really dead simple to create the apis, the underlying transport, the ipc channel that the apis
communicate through over the transport and eventually call the apis.
The receiver apis are multithreaded, the exact number of threads used is configurable. Specifying a single thread results
in only one api call being transacted on the receiver, probably not what you want and will result in the calling side
appearing to lockup on blocking calls (unless a timeout is specified), or timeout on asynchronous calls!

There is a full suite of unit-tests which take about 285 seconds and yield no leftover threads or processes.

Example taken and extended from one of the unit-tests:

        #    Create the IPC:
        #    Create the transactionManagers that manage the asynchronous api calls - matching clients to responses and
        #    handling timeouts, callbacks, error-handling etc.
        tmHead = TransactionManager(HeadTransactionIdGenerator())
        tmNeck = TransactionManager(NeckTransactionIdGenerator())
        #    Create the listeners that handle unsolicited api calls or calls that have no existing handler set:
        self.hl = My1Listener()
        self.nl = My1Listener()
        #   Abstracted queue transport factory:
        self.qTransport = QueueTransportDetails()
        #   Create the underlying transports (Neck and Head):
        #    Create the Head as one side of the transport:
        self.ipcHead = QueueTransporter(self.qTransport, tmHead, self.hl, logger=LogManager().getLogger("Head"))
        #    Create the Neck as the other side of the transport:
        self.ipcNeck = QueueTransporter(self.qTransport.invert(), tmNeck, self.nl, logger=LogManager().getLogger("Neck"))
        #    Create the hierarchical api 'objects' on each side:
        #    Head api with namespace 'test':
        self.apiHead = Api("test")
        ...etc (more apis bound as attributes to self.apiHead, of infinite depth)
        #    Bind the ipc into the Head apis:
        self.apiHead.ipc = self.ipcHead
        #    Neck api with namespace 'test', where all api calls 'originating from the Neck' are solicited only (ie: no
        #    spontaneous unsolicited events, unless overridden):
        self.apiNeck = Api("test", solicited=True)
        ...etc
        #    Bind the ipc into the Neck apis:
        self.apiNeck.ipc = self.ipcNeck
        #    Connect each side of the transport to it's IPC transport:
        self.ipcHead.connect()
        self.ipcNeck.connect()
        #    Now call the api method 'method_a' in the apiHead:
        #    Create the api method to be called, passing all args & kwargs:
        func = self.apiHead.method_a(*(0, 1, 2, 3), **{"four":4, "five":5})
        try:
            #    Now modify the default behaviour of the api (synchronicity/blocking, solicited, timeout, etc) and CALL IT !
            #    This is entirely optional, if the api has it's default behaviour set then there is no need to override it!
            result = func(sync, timeout, solicited, callback, ignoreErrors)
        except (iApiParamError, UnknownApiError, UnsupportedApiError, TransactionFailed), e:
            #    D'oh! Foobar'd, etc
        #    If the call is asynchronous, 'result' is an iAsyncResult, if the call is synchronous, the result is the
        #    actual result!
        #    Bear in mind that the result has come over the IPC so any references need to be copied into the result
        #    object before being returned over the IPC.
