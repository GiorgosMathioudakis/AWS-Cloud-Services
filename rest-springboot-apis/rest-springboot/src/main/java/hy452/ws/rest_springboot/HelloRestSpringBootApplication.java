package hy452.ws.rest_springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.web.bind.annotation.RequestParam;
import io.swagger.v3.oas.annotations.*;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@OpenAPIDefinition(info = @Info(title = "HelloWorld API", version = "1.0", description = "HelloWorld information about the API"))
@RestController
public class HelloRestSpringBootApplication {

	public static void main(String[] args) {
		SpringApplication.run(HelloRestSpringBootApplication.class, args);
	}

	@Operation(summary = "Say hello [name].")
	@GetMapping("/hellospring")
	public String hello(@RequestParam(value="name",defaultValue="World") String name) {

		return String.format("Hello %s!" , name);
	}

}


