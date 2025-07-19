package hy452.ws.rest_springboot;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.springframework.stereotype.Service;
import java.io.InputStream;
import java.io.FileNotFoundException;

@Service
public class CountryInfoExtractor {

    private Document document;
    private XPath xPath;

    public CountryInfoExtractor() {
        try {
            // Load the XML file from the classpath
            InputStream inputStream = getClass().getClassLoader().getResourceAsStream("xmldata_mondial-3.0.xml");
            if (inputStream == null) {
                throw new FileNotFoundException("Mondial XML file not found in resources");
            }

            // Parse the XML file
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            document = builder.parse(inputStream);
            document.getDocumentElement().normalize();

            // Initialize XPath
            xPath = XPathFactory.newInstance().newXPath();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getCountryAttribute(String datacode, String attribute) {
        try {
            String expression = String.format("//country[@datacode='%s']/@%s", datacode, attribute);
            Node node = (Node) xPath.evaluate(expression, document, XPathConstants.NODE);
            return node != null ? node.getNodeValue() : "Not found";
        } catch (Exception e) {
            e.printStackTrace();
            return "Error retrieving attribute.";
        }
    }

    public String getCapitalName(String datacode) {
        try {
            String capitalIdExpression = String.format("//country[@datacode='%s']/@capital", datacode);
            Node capitalIdNode = (Node) xPath.evaluate(capitalIdExpression, document, XPathConstants.NODE);

            if (capitalIdNode != null) {
                String capitalNameExpression = String.format("//city[@id='%s']/name", capitalIdNode.getNodeValue());
                Node capitalNameNode = (Node) xPath.evaluate(capitalNameExpression, document, XPathConstants.NODE);
                return capitalNameNode != null ? capitalNameNode.getTextContent().trim() : "Not found";
            }
            return "Not found";
        } catch (Exception e) {
            e.printStackTrace();
            return "Error retrieving capital name.";
        }
    }
}
