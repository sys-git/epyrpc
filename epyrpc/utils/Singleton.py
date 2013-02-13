from epyrpc.exceptions.NotImplemented import NotImplementedException
import weakref

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        cls._instanceLock.acquire()

        try:
            if not cls._instance:
                instance = object.__new__(cls)
                instance._setup(*args, **kwargs)
                cls._instance = instance
            return weakref.proxy(cls._instance)
        finally:
            cls._instanceLock.release()

    def _setup(self):
        raise NotImplementedException()

    @classmethod
    def destroySingleton(cls):
        cls._instanceLock.acquire()

        try:
            if cls.hasInstance() and \
            hasattr(cls._instance, "shutdown"):
                cls._instance.shutdown()
            cls._instance = None
        finally:
            cls._instanceLock.release()

    @classmethod
    def createNewInstance(cls, *args, **kwargs):
        cls._instanceLock.acquire()

        try:
            cls.destroySingleton()
            return cls(*args, **kwargs)
        finally:
            cls._instanceLock.release()

    @classmethod
    def hasInstance(cls):
        cls._instanceLock.acquire()

        try:
            return cls._instance != None
        finally:
            cls._instanceLock.release()
