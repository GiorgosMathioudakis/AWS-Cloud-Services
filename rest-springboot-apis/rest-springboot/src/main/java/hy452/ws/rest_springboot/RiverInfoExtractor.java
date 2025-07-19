package hy452.ws.rest_springboot;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;
import org.w3c.dom.*;
import java.io.InputStream;
import java.io.FileNotFoundException;

@Service
public class RiverInfoExtractor {

    private Document document;
    private XPath xPath;

    public RiverInfoExtractor() {
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

    // Get the list of countries through which the river passes
    public List<String> getRiverCountries(String riverName) {
        try {
            // Find all country IDs in <located> tags for the given river
            String locatedExpression = String.format("//river[@name='%s']/located/@country", riverName);
            NodeList countryIdNodes = (NodeList) xPath.evaluate(locatedExpression, document, XPathConstants.NODESET);

            List<String> countries = new ArrayList<>(); // Use a List to store country names

            for (int i = 0; i < countryIdNodes.getLength(); i++) {
                String countryId = countryIdNodes.item(i).getNodeValue().trim();

                // Find the country name for the corresponding country ID
                String countryNameExpression = String.format("//country[@id='%s']/@name", countryId);
                Node countryNameNode = (Node) xPath.evaluate(countryNameExpression, document, XPathConstants.NODE);

                if (countryNameNode != null) {
                    String countryName = countryNameNode.getNodeValue();
                    // Add the country only if it's not already in the list
                    if (!countries.contains(countryName)) {
                        countries.add(countryName);
                    }
                } else {
                    countries.add("Unknown Country ID: " + countryId);
                }
            }

            return countries;

        } catch (Exception e) {
            e.printStackTrace();
            return List.of("Error retrieving countries.");
        }
    }


    // Get the outfall of the river
    public String getRiverOutfall(String riverName) {
        try {
            // Find the <to> tag for the river
            String toExpression = String.format("//river[@name='%s']/to", riverName);
            Node toNode = (Node) xPath.evaluate(toExpression, document, XPathConstants.NODE);

            if (toNode != null) {
                // Retrieve the type (river, sea, lake) and water ID
                String type = toNode.getAttributes().getNamedItem("type").getNodeValue();
                String waterId = toNode.getAttributes().getNamedItem("water").getNodeValue();

                // Determine the XPath expression to find the name based on the type
                String waterNameExpression = "";
                switch (type) {
                    case "river":
                        waterNameExpression = String.format("//river[@id='%s']/@name", waterId);
                        break;
                    case "sea":
                        waterNameExpression = String.format("//sea[@id='%s']/@name", waterId);
                        break;
                    case "lake":
                        waterNameExpression = String.format("//lake[@id='%s']/@name", waterId);
                        break;
                    default:
                        return "Unknown outfall type: " + type;
                }

                // Retrieve the name of the water body
                Node waterNameNode = (Node) xPath.evaluate(waterNameExpression, document, XPathConstants.NODE);
                return waterNameNode != null ? waterNameNode.getNodeValue() : "Unknown water ID: " + waterId;
            }

            return "Outfall not found";

        } catch (Exception e) {
            e.printStackTrace();
            return "Error retrieving outfall.";
        }
    }

}
