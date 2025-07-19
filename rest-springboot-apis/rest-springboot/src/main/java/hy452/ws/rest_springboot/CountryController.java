package hy452.ws.rest_springboot;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CountryController {

    private final CountryInfoExtractor countryInfoExtractor;

    // Constructor-based Dependency Injection
    public CountryController(CountryInfoExtractor countryInfoExtractor) {
        this.countryInfoExtractor = countryInfoExtractor;
    }

    @GetMapping("/country/{code}")
    public CountryDetails getCountryDetails(@PathVariable String code) {
        String name = countryInfoExtractor.getCountryAttribute(code, "name");
        String population = countryInfoExtractor.getCountryAttribute(code, "population");
        String totalArea = countryInfoExtractor.getCountryAttribute(code, "total_area");
        String capitalName = countryInfoExtractor.getCapitalName(code);
        String politicalSystem = countryInfoExtractor.getCountryAttribute(code, "government");

        return new CountryDetails(name, population, totalArea, capitalName, politicalSystem);
    }



    @GetMapping("/country/{code}/name")
    public String getCountryName(@PathVariable String code) {
        return countryInfoExtractor.getCountryAttribute(code, "name");
    }

    @GetMapping("/country/{code}/population")
    public String getCountryPopulation(@PathVariable String code) {
        return countryInfoExtractor.getCountryAttribute(code, "population");
    }

    @GetMapping("/country/{code}/total_area")
    public String getCountryTotalArea(@PathVariable String code) {
        return countryInfoExtractor.getCountryAttribute(code, "total_area");
    }

    @GetMapping("/country/{code}/capital_name")
    public String getCountryCapitalName(@PathVariable String code) {
        return countryInfoExtractor.getCapitalName(code);
    }

    @GetMapping("/country/{code}/political_system")
    public String getCountryPoliticalSystem(@PathVariable String code) {
        return countryInfoExtractor.getCountryAttribute(code, "government");
    }
}
