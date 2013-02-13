from StringIO import StringIO
from epyrpc.exceptions.ConfigurationManagerExceptions import \
    InvalidConfigurationFiles, InvalidConfigurationXML
from epyrpc.utils.LogManager import LogManager
from gnosis.xml.objectify._objectify import make_instance, tagname, attributes, \
    content
from minixsv import pyxsval
from sys import stdout
from traceback import format_exc
from types import StringTypes
import hashlib
import os

class Objectify(object):
    """
    The objectify class allows the application
    to setup and use Objectify by using the
    constructor, then accessing Objectify
    by using the .instance attribute
    @param xml: XML file path
    @param xsd: XSD file path 
    @raise InvalidConfigurationXML: Non existent XML/XSD. Invalid formatted files 
    """

    KWARGS = {
      "xmlIfClass"      : pyxsval.XMLIF_ELEMENTTREE,
      "warningProc"     : pyxsval.PRINT_WARNINGS,
      "errorLimit"      : 200,
      "verbose"         : 0,
      "useCaching"      : 0,
      "processXInclude" : 0
    }

    def __init__(self, xml, xsd):
        self.logger = LogManager().getLogger(self.__class__.__name__)

        self.cwd = os.path.abspath('.')
        self.xmlFile = os.path.abspath(xml)
        self.xsdFile = os.path.abspath(xsd)

        if not os.path.exists(self.xmlFile) or not os.path.exists(self.xsdFile):
            raise InvalidConfigurationFiles("Given Files: %s - %s"
                % (self.xmlFile, self.xsdFile))

        self.logger.debug("Attempting to find XML hash")
        successfulLoad, xmlHash, xsdHash = self.__loadFromCache(xml, xsd)

        if not successfulLoad:  # Hashes are incorrect
            self.logger.debug("Validating XML against XSD")
            self.__loadAndValidate(xml, xsd, xmlHash, xsdHash)

    def __loadFromCache(self, xml, xsd):
        hashPath = self.__getXmlHashFile(xml)
        xmlHash = self.__hashFile(xml)
        xsdHash = self.__hashFile(xsd)

        if not os.path.exists(hashPath):
            self.logger.debug("Hash doesn't exist: %s" % hashPath)
            return (False, xmlHash, xsdHash)

        hashFile = open(hashPath, 'r')
        cachedXMLHash = hashFile.readline().strip()
        cachedXSDHash = hashFile.readline().strip()
        hashFile.close()

        if cachedXMLHash != xmlHash or cachedXSDHash != xsdHash:
            self.logger.info("Incorrect Hashes: %s - %s, %s - %s" % 
                (cachedXMLHash, xmlHash, cachedXSDHash, xsdHash))
            return (False, xmlHash, xsdHash)

        self.configuration = make_instance(xml)
        return (True, xmlHash, xsdHash)

    def __hashFile(self, path):
        xmlFile = open(path, 'rb')
        shaHash = hashlib.sha1()

        while True:
            data = xmlFile.read(4096)
            if not data: break
            shaHash.update(hashlib.sha1(data).hexdigest())
        xmlFile.close()

        return shaHash.hexdigest()

    def __loadAndValidate(self, xml, xsd, xmlHash, xsdHash):
        try:  # Validate the config file
            pyxsval.parseAndValidate(\
                 inputFile=xml,
                 xsdFile=xsd,
                 **Objectify.KWARGS)
        except Exception:
            raise InvalidConfigurationXML(format_exc())
        self.logger.debug("Validated XML against XSD")

        # gnosis.xml.objectify._XO_node = Node.Node
        # gnosis.xml.objectify._XO_interface = Interface.Interface
        self.configuration = make_instance(xml)
        hashPath = self.__getXmlHashFile(xml)

        try:
            hashFile = open(hashPath, 'w')
            hashFile.write("%s\n%s" % (xmlHash, xsdHash))
            hashFile.close()
        except IOError, e:
            self.logger.error(e)

    def __getXmlHashFile(self, xmlPath):
        head, tail = os.path.split(xmlPath)
        hashFile = os.path.join(head, ".hash.%s" % tail)
        return hashFile

    def getConfiguration(self):
        """
        Get the configuration object
        @return: Objects representing the configuration
        """
        return self.configuration

    def getXMLFileLocation(self):
        """
        Return the path of the related XML file
        @return: Path of XML file
        """
        return self.xmlFile

    def getXSDFileLocation(self):
        """
        Return the path of the related XSD file
        @return: Path of XSD file
        """
        return self.xsdFile

    def revalidate(self):
        """ Re-validate the in memory object tree against the related XSD """
        xmlBuffer = self.__write_xml(self.configuration, StringIO())
        xml = xmlBuffer.getvalue()
        xmlBuffer.close()

        xsdBuffer = open(self.xsdFile, 'r')
        xsd = "".join(xsdBuffer.readlines())
        xsdBuffer.close()

        try:  # Validate the config file
            cwd = os.path.sep.join(self.xmlFile.split(os.path.sep)[:-1])
            os.chdir(cwd)
            self.logger.debug("Validating XML against XSD")

            pyxsval.parseAndValidateXmlInputString(
                inputText=xml,
                xsdText=xsd,
                validateSchema=1,
                **Objectify.KWARGS)
        except Exception:
            self.logger.error("Error occurred within %s" % cwd)
            raise InvalidConfigurationXML(format_exc())
        finally: os.chdir(self.cwd)
        self.logger.debug("Validated XML against XSD")

    def __write_xml(self, o, out=stdout):
        """ Serialize an _XO_ object back into XML """
        out.write("<%s" % tagname(o))
        for attr in attributes(o):
            out.write(' %s="%s"' % attr)
        out.write('>')
        for node in content(o):
            if type(node) in StringTypes:
                out.write(node)
            else: self.__write_xml(node, out=out)
        out.write("</%s>" % tagname(o))
        return out
