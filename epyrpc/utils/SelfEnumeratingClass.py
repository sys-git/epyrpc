
import copy

class SelfEnumeratingClass(object):
    """
    @summary: This class enumerates it's attributes where the attributes fulfil the following criteria:
    1.    Begin with an uppercase character.
    2.    Are not callable
    3.    Does not start with an underscore character.
    @attention: Module imports are thread-safe so as long as we instantiate the class when
    loading it cls._enumerations will be thread-safe.
    """
    @classmethod
    def __init__(cls):
        cls._enumerations = {}
        cls._enumerate()

    @classmethod
    def enumerateAttributes(cls, t, catchall=False):
        if t == None:
            if catchall is False:
                raise ValueError("None is not a valid enumeration value!")
            return None

        try:
            return getattr(cls, "_enumerations")[t]
        except KeyError:
            if catchall: return
            raise ValueError("Cannot enumerate: %(T)s" % {"T":t})

    @classmethod
    def lookupEnumerationValue(cls, enumeratedValue, catchall=False):
        """ @summary: Perform a reverse-lookup on the enumeratedValue. """
        if enumeratedValue == None:
            if catchall: return
            raise ValueError("None is not a valid enumeratedValue!")

        enumerations = getattr(cls, "_enumerations")

        enumeratedValueLower = enumeratedValue.lower()
        for key, value in enumerations.items():
            if value.lower() == enumeratedValueLower:
                return key
        raise ValueError("Unable to enumerate: <%(V)s>(<%(L)s>) from: %(E)s" % {"V":enumeratedValue, "L":enumeratedValueLower, "E":enumerations})

    @classmethod
    def _enumerate(cls):
        enumerations = getattr(cls, "_enumerations")

        for i in dir(cls):
            if not i.startswith("_") and i[0].isupper() and not callable(i):
                value = getattr(cls, i)
                enumerations[value] = i

    @classmethod
    def isValid(cls, value):
        if value is None:
            raise ValueError("value cannot be None.")
        return value in getattr(cls, "_enumerations").keys()

    @classmethod
    def isValidEnumeration(cls, enumeratedValue):
        enumeratedValueLower = enumeratedValue.lower()

        for i in getattr(cls, "_enumerations").values():
            if i.lower() == enumeratedValueLower:
                return True
        return False

    @classmethod
    def getEnumerations(cls):
        copy.copy(getattr(cls, "_enumerations"))

    @classmethod
    def getIterator(cls):
        sortedKeys = getattr(cls, "_enumerations").keys()
        sortedKeys.sort()
        return iter(sortedKeys)

    @staticmethod
    def getCyclicIterator(cls, existingValue):
        """
        @summary: Create a cyclic iterator.
        @attention: It goes forever!
        """
        while True:
            cls._check(existingValue)
            sortedKeys = cls._enumerations.keys()
            sortedKeys.sort()

            for i, key in enumerate(sortedKeys):
                if key == existingValue:
                    break

            i += 1  # Cycle
            if i == len(sortedKeys):
                i = 0
            existingValue = sortedKeys[i]
            yield sortedKeys[i]

