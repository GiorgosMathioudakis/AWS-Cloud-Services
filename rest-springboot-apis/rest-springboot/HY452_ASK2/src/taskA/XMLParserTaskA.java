package taskA;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import com.google.gson.*;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;


public class XMLParserTaskA {
    public static void main(String[] args) {
        try {
        	
        	//taskA (I)
        	System.out.println("taskA (I)");
            // Load and parse the XML file
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.parse("resources/xmldata_mondial-3.0.xml");
            
            // Normalize the document
            document.getDocumentElement().normalize();
            
            // Print root node name
            System.out.println("Root Node: " + document.getDocumentElement().getNodeName());
            
            // Get first-level nodes
            NodeList childNodes = document.getDocumentElement().getChildNodes();
            System.out.println("First-level nodes:");
            for (int i = 0; i < childNodes.getLength(); i++) {
                Node node = childNodes.item(i);
                if (node.getNodeType() == Node.ELEMENT_NODE) {
                    System.out.println(" - " + node.getNodeName());
                }
            }
            
            //taskA (II)
            System.out.println("taskA (II)");
            // Create an XPath object
            XPathFactory xPathFactory = XPathFactory.newInstance();
            XPath xPath = xPathFactory.newXPath();
            
            // XPath expression to find European countries
            String expression = "//country[encompassed[@continent='f0_119']]";
            
            // Evaluate XPath expression
            NodeList europeanCountries = (NodeList) xPath.evaluate(expression, document, XPathConstants.NODESET);
            
            // Print names of European countries
            System.out.println("European Countries:");
            for (int i = 0; i < europeanCountries.getLength(); i++) {
                Node countryNode = europeanCountries.item(i);
                String countryName = countryNode.getAttributes().getNamedItem("name").getNodeValue();
                System.out.println(" - " + countryName);
            }
            
            //taskA (III)
            System.out.println("taskA (III)");
            xPathFactory = XPathFactory.newInstance();
            xPath = xPathFactory.newXPath();
            
            // XPath expression to find countries in both Europe and Asia
            expression = "//country[encompassed[@continent='f0_119'] and encompassed[@continent='f0_123']]";
            
            // Evaluate XPath expression
            NodeList transcontinentalCountries = (NodeList) xPath.evaluate(expression, document, XPathConstants.NODESET);
            
            // Print attributes of each country
            System.out.println("Countries in both Europe and Asia:");
            for (int i = 0; i < transcontinentalCountries.getLength(); i++) {
                Node countryNode = transcontinentalCountries.item(i);
                System.out.println("Country:");
                NamedNodeMap attributes = countryNode.getAttributes();
                for (int j = 0; j < attributes.getLength(); j++) {
                    Node attribute = attributes.item(j);
                    System.out.println(" - " + attribute.getNodeName() + ": " + attribute.getNodeValue());
                }
            }
            
            //task A(IV)
         // Create a list to store all country data
            ArrayList<HashMap<String, String>> countriesList = new ArrayList<>();

            // Iterate through European countries and extract attributes
            for (int i = 0; i < europeanCountries.getLength(); i++) {
                Node countryNode = europeanCountries.item(i);
                NamedNodeMap attributes = countryNode.getAttributes();
                HashMap<String, String> countryData = new HashMap<>();
                
                for (int j = 0; j < attributes.getLength(); j++) {
                    Node attribute = attributes.item(j);
                    countryData.put(attribute.getNodeName(), attribute.getNodeValue());
                }
                countriesList.add(countryData);
            }

            // Convert to JSON using Gson
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            String jsonOutput = gson.toJson(countriesList);

            // Write JSON to a file
            try (FileWriter fileWriter = new FileWriter("european_countries.json")) {
                fileWriter.write(jsonOutput);
                System.out.println("JSON file 'european_countries.json' created successfully!");
            } catch (IOException e) {
                e.printStackTrace();
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
