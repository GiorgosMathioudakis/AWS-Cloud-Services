package hy452.ws.rest_springboot;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
public class RiverController {

    private final RiverInfoExtractor riverInfoExtractor;

    public RiverController(RiverInfoExtractor riverInfoExtractor) {
        this.riverInfoExtractor = riverInfoExtractor;
    }

    @GetMapping("/river/{name}/passes_through_countries")
    public List<String> getRiverCountries(@PathVariable String name) {
        return riverInfoExtractor.getRiverCountries(name);
    }

    @GetMapping("/river/{name}/river_outfall")
    public String getRiverOutfall(@PathVariable String name) {
        return riverInfoExtractor.getRiverOutfall(name);
    }
}
