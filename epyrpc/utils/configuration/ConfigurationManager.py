from epyrpc.exceptions.ConfigurationManagerExceptions import \
    InvalidConfigurationXML, InvalidConfiguration
from epyrpc.utils.LogManager import LogManager
from epyrpc.utils.Singleton import Singleton
from epyrpc.utils.configuration.Objectify import Objectify
from glob import glob
from threading import RLock
import os

class ConfigurationManager(Singleton):
    _instance = None
    _instanceLock = RLock()

    def _setup(self, cwd=None):
        if not cwd: cwd = os.getcwd()
        existingCwd = os.getcwd()

        self.logger = LogManager().getLogger(self.__class__.__name__)
        self.logger.debug('Current Directory: %s' % os.getcwd())

        try:
            xml = None
            os.chdir(cwd)
            self.xmls = {}
            self.logger.info("Loading configuration from: %s" % os.getcwd())

            for xml in glob("config/*.xml"):
                name = xml.split("/")[-1].split(".")[0]
                xsd = "config/validation/%s.xsd" % name
                if not os.path.exists(xsd): continue
                self.loadConfiguration(xml, xsd)
        except Exception, e:
            self.logger.info("Failed to load %s" % xml)
            self.__raiseError(str(e))
            raise
        finally:
            os.chdir(existingCwd)

    def loadConfiguration(self, xml, xsd):
        """
        Load and validate the configuration file provided
        @param xml: XML to convert into an object
        @param xsd: XSD file to validate the XML
        """
        if not xml.endswith(".xml") or not os.path.exists(xml):
            raise InvalidConfigurationXML("Invalid XML File: %s"
                % os.path.realpath(xml))

        if not xsd.endswith(".xsd") or not os.path.exists(xsd):
            raise InvalidConfigurationXML("Invalid XSD File: %s"
                % os.path.realpath(xsd))

        name = xml.split(os.path.sep)[-1][:-4]
        if name in self.xmls.keys():
            raise InvalidConfigurationXML("Duplicate XML File: %s"
                % os.path.realpath(xml))

        self.logger.debug("Loading config file: %s - %s"
            % (os.path.realpath(xml), os.path.realpath(xsd)))

        xmlObject = Objectify(xml, xsd)
        self.xmls[name.lower()] = xmlObject
        self.logger.debug("Loaded config file: %s - %s"
            % (os.path.realpath(xml), os.path.realpath(xsd)))

    def getConfiguration(self, name):
        """
        Retrieve a configuration object based on its name
        @param name: Name of configuration file with the .xml (exp.xml = exp)
        @raise InvalidConfiguration: Configuration instance not found
        @return: Configuration instance
        """
        name = name.lower()
        if name not in self.xmls.keys():
            msg = "Cannot find configuration: %s, %s" % (name, os.getcwd())
            self.__raiseError(msg)
            raise InvalidConfiguration(msg)
        return self.xmls[name]

    def configurationExists(self, name):
        """
        Finds if a given configuration has been loaded
        @param name: Name of configuration file with the .xml (exp.xml = exp)
        @return: True if the configuration exists, else false
        """
        return name.lower() in self.xmls.keys()

    def configurationNames(self):
        """
        Return a list of configuration names that have been loaded
        @return: List of configuration names
        """
        return self.xmls.keys()

    def revalidateXMLs(self):
        """ Re-validate all the XMLs against their related XSD """
        for xml in self.xmls.values():
            xml.revalidate()

    def __raiseError(self, msg):
        print msg
