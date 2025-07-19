package hy452.ws.rest_springboot;

public class CountryDetails {
    private String name;
    private String population;
    private String totalArea;
    private String capitalName;
    private String politicalSystem;

    // Constructor
    public CountryDetails(String name, String population, String totalArea, String capitalName, String politicalSystem) {
        this.name = name;
        this.population = population;
        this.totalArea = totalArea;
        this.capitalName = capitalName;
        this.politicalSystem = politicalSystem;
    }

    // Getters and Setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPopulation() {
        return population;
    }

    public void setPopulation(String population) {
        this.population = population;
    }

    public String getTotalArea() {
        return totalArea;
    }

    public void setTotalArea(String totalArea) {
        this.totalArea = totalArea;
    }

    public String getCapitalName() {
        return capitalName;
    }

    public void setCapitalName(String capitalName) {
        this.capitalName = capitalName;
    }

    public String getPoliticalSystem() {
        return politicalSystem;
    }

    public void setPoliticalSystem(String politicalSystem) {
        this.politicalSystem = politicalSystem;
    }
}
