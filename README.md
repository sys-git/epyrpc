epyrpc
======

Object based pure Python RPC for inter-process communications.

Inter-process RPC exposed over an interface (currently supported: multiprocessing.queue) as hierarchical object
based api over an underlying IPC transport.
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
lifetime of a given IPC transport.
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

There is a full suite of unit-tests which yield no leftover threads or processes.

The IPC allows a single api access to it. In order to allow multiple apis concurrant access to the same IPC, the
TransportFactory uses an api arbitrator: ApiArb as shown below:

    Typical example usage:
    ( HEAD                     ) -------------------------( BODY                     )
    ['1' handler workers]-api1-\                          /-api1-['x' handler workers]
    ['1' handler workers]-api2-ApiArb--IPC-wire-IPC--ApiArb-api2-['y' handler workers]
    ['1' handler workers]-api3-/                          \-api3-['z' handler workers]

TODO:
Make api inheritance automatic.
Auto-create apis from configuration xml, alternatively make api methods automatically generated when hard-coded.
Implement other IPC transports (ie: socket)

Example taken and extended from one of the unit-tests:

        #    Create the IPC:
        #    Create the transactionManagers that manage the asynchronous api calls - matching clients to responses and
        #    handling timeouts, callbacks, error-handling etc.
        tmHead = TransactionManager(HeadTransactionIdGenerator())
        tmNeck = TransactionManager(NeckTransactionIdGenerator())

        #    Create the listeners that handle unsolicited api calls or calls that have no existing handler set:
        def MyHeadListener(iIpcTransportDataReceiveListener, iIpcTransportStateChangeListener):
            def transportStateChange(self, e_ipc_transport_state):
                #       The IPC state has changed, see: eIpcTransportState
            def transportDataReceive(self, tId, data):
                #       Unhandled api call received with type(data)=IpcMessageBase.
        self.hl = MyHeadListener()
        #   Abstracted queue transport factory:
        self.qTransport = QueueTransportDetails()
        #   Create the underlying transports (Neck and Head):
        #    Create the Head as one side of the transport:
        self.ipcHead = QueueTransporter(self.qTransport, tmHead, self.hl, logger=LogManager().getLogger("Head"))
        #    Create the Neck as the other side of the transport:
        self.ipcNeck = QueueTransporter(self.qTransport.invert(), tmNeck, logger=LogManager().getLogger("Neck"))
        #    Create the hierarchical api 'objects' on each side:
        #    Head api with namespace 'test':
        self.apiHead = Head("test")
        ...etc (more apis bound as attributes to self.apiHead, of infinite depth)
        #    Bind the ipc into the Head apis:
        self.apiHead.ipc = self.ipcHead
        #    Neck api with namespace 'test', where all api calls 'originating from the Neck' are solicited only (ie: no
        #    spontaneous unsolicited events, unless overridden):
        self.apiNeck = Neck("test", solicited=True)
        ...etc
        #    Bind the ipc into the Neck apis:
        self.apiNeck.ipc = self.ipcNeck
        #    Connect each side of the IPC to it's underlying transport:
        self.ipcHead.connect()
        self.ipcNeck.connect()
        #    Now call the api method 'method_a' in the apiHead:
        #    Create the api method to be called, passing all args & kwargs,
        #       This will be handled by Neck.nestedApiObject._handler_method_a():
        func = self.apiHead.nestedApiObject.method_a(*(0, 1, 2, 3), **{"four":4, "five":5})
        #       Or call from the non-nested top-level api:
        func = self.apiNeck.method_c("hello", world=True)
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
        
        #    Send an unsolicited event from the Neck to the head:
        #    Create the rpc method, this will be handled by Head._handler_method_b():
        func1 = self.apiNeck.method_b("hello", world=True)
        #       Or call from the nested api:
        func1 = self.apiNeck.nestedNeckApiObject.method_d("there is no handler", world="for this api call")
        #    And call it!
        #    FYI - unsolicited events are 'fire-and-forget', setting 'ignoreErrors'=True prevents exceptions
        #    from being raised if the call failed due to one of: [IpcException, TransactionFailed, iApiParamError].
        func1(solicited = False, ignoreErrors=True)
        
        #       Here the Head's controller registers a handler to receive api calls on a given namespace ("method_d")
        #       which currently has no hard-coded handler in the class 'NestedHeadApi':
        def myHandlerMethod(self, tId, bSynchronous, *func_args, **func_kwargs):
                #       Do work.
                pass
        #       Both of these calls are equivalent:
        self.apiHead.setHandler("nestedNeckApiObject.method_d", myHandlerMethod)
        self.apiHead.nestedNeckApiObject.setHandler("method_d", myHandlerMethod)
        
        
        An example of the Head api containing the nested api object:
        #       Note there is no handler for method_d in NestedHeadApi, this will result in an exception back at the
        #       caller in the Neck or the Head's controller can set a global handler for all unhandled calls to allow
        #       it to selectively process them or it can register handlers directly onto any part of the Head's nested
        #       api by reference to it's namespace.
        class NestedHeadApi(ApiBase):
            def __init__(self, ns="", solicited=False, ipc=None):
                super(NestedHeadApi, self).__init__(ns=ns, solicited=solicited)
            def method_a(self, *func_args, **func_kwargs):
                #       Check func_args and func_kwargs...or do something else prior to sending the data:
                return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *func_args, **func_kwargs)
        
        class Head(ApiBase):
            def __init__(self, ns="", solicited=False, ipc=None):
                super(Head, self).__init__(ns=ns, solicited=solicited)
                if ipc != None:
                    self.ipc = ipc

            def _setup(self, **kwargs):
                #       Create the nested api object:
                self.nestedHeadApiObject = NestedHeadApi(**kwargs)
                #       Add it to our internal api list:
                self._apis.append(self.nestedHeadApiObject)
        
            #   A method prefix of '_handler_' automatically makes it an api handler:
            def _handler_method_b(self, tId, bSynchronous, *func_args, **func_kwargs):
                def work(*funcArgs, **funcKargs)
                        #       Do work in here in response to the rpc call from the Neck...
                        #       Or raise an exception, checked or unchecked:
                        raise some_exception        
                #       Handle the call correctly or use the builtin handler wrapper:
                return self._handleStandardCall(tId, bSynchronous, work, *func_args, **func_kwargs)
        
            #   A normal method acts as the api method which the Head's caller can use:
            def method_c(self, *func_args, **func_kwargs):
                #       Check func_args and func_kwargs...or do something else prior to sending the data:
                return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *func_args, **func_kwargs)

        #       ...Here's an example of the Neck:
        class NestedNeckApi(ApiBase):
            def __init__(self, ns="", solicited=False, ipc=None):
                super(NestedNeckApi, self).__init__(ns=ns, solicited=solicited)

            def _handler_method_a(self, tId, bSynchronous, *func_args, **func_kwargs):
                #       Do work in here in response to the rpc call from the Head...
                return some_result
                #       Or raise an exception, checked or unchecked:
                raise some_exception

            def method_d(self, *func_args, **func_kwargs):
                #       Check func_args and func_kwargs...or do something else prior to sending the data:
                return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *func_args, **func_kwargs)
                
        class Neck(ApiBase):
            def __init__(self, ns="", solicited=True, ipc=None):
                super(Neck, self).__init__(ns=ns, solicited=solicited)
                if ipc != None:
                        self.ipc = ipc
 
            def _setup(self, **kwargs):
                #       Create the nested api object:
                self.nestedNeckApiObject = NestedNeckApi(**kwargs)
                #       Add it to our internal api list:
                self._apis.append(self.nestedNeckApiObject)
                
            #   A method prefix of '_handler_' automatically makes it an api handler:
            def _handler_method_c(self, tId, bSynchronous, *func_args, **func_kwargs):
                #       Do work in here in response to the rpc call from the Head...
                return some_result
                #       Or raise an exception, checked or unchecked:
                raise some_exception
                
            def method_b(self, *func_args, **func_kwargs):
                #       Check func_args and func_kwargs...or do something else prior to sending the data:
                return ApiAction(self.ipc, self._makeNamespace(self._whoami()), self.solicited, *func_args, **func_kwargs)
                
                
