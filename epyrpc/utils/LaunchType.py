
from epyrpc.utils.SelfEnumeratingClass import SelfEnumeratingClass

class LaunchType(SelfEnumeratingClass):
    PROCESS = 654
    THREAD = 987
LaunchType()
