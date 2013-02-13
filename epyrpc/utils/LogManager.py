from epyrpc.utils.Singleton import Singleton
from logbook.base import NOTSET
from logbook.handlers import FileHandler
from threading import RLock
import logbook

class LogManager(Singleton):
    _instance = None
    _instanceLock = RLock()

    CRITICAL = logbook.CRITICAL
    ERROR = logbook.ERROR
    WARNING = logbook.WARNING
    NOTICE = logbook.NOTICE
    INFO = logbook.INFO
    DEBUG = logbook.DEBUG

    FILENAME = 'application.log'

    def _setup(self):
        self.handlers = [
            FileHandler(LogManager.FILENAME, level=NOTSET, bubble=True) ]
        self.on = False
        self.turnOnLogging()

        logbook.default_handler.level = NOTSET
        self.handlers.append(logbook.default_handler)

    def turnOffLogging(self):
        #    FIXME: off/on/off cycling fails.
        if self.on == False: return
        for handler in self.handlers:
            handler.pop_application()
        self.on = False

    def turnOnLogging(self):
        if self.on == True: return
        for handler in self.handlers:
            handler.push_application()
        self.on = True

    def isOn(self):
        return (self.on == True)

    def getLogger(self, name):
        """
        Get a logger with a certain name
        @param name: Name of logger to retrieve
        """
        return logbook.Logger(name)
