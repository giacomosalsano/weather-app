package com.weather_app.infrastructure.controllers;

import java.net.URI;
import java.time.LocalDateTime;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.GetWeatherUseCase;
import com.weather_app.core.ports.SaveWeatherUseCase;

@RestController
@RequestMapping("/weather")
public class WeatherController {

    private final GetWeatherUseCase getWeatherUseCase;
    private final SaveWeatherUseCase saveWeatherUseCase;

    // TO LEARN: Implementing the Interface Segregation Principle (SOLID). 
    // This way, the WeatherController requires both GetWeatherUseCase and SaveWeatherUseCase as separate dependencies instead of a single huge dependency.
    public WeatherController(GetWeatherUseCase getWeatherUseCase, SaveWeatherUseCase saveWeatherUseCase) {
        this.getWeatherUseCase = getWeatherUseCase;
        this.saveWeatherUseCase = saveWeatherUseCase;
    }

    @GetMapping("/{city}")
    // TO LEARN: PathVariable is a Spring Web annotation that maps the GET request to the getWeather method.
    // It intercepts the the parameters of the request and maps them to inject into the `String city` local variable
    // Is the equivalent of the Decorators on JS/TS
    public ResponseEntity<Weather> getWeather(@PathVariable String city) {
        try {
            Weather weather = getWeatherUseCase.execute(city);
            return ResponseEntity.ok(weather);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }


    @PostMapping
    public ResponseEntity<Weather> createWeather(@RequestBody WeatherRequest request) {
        Weather domainWeather = new Weather(
            request.city(),
            request.temperature(),
            request.description(),
            LocalDateTime.now() 
        );

        Weather savedWeather = saveWeatherUseCase.execute(domainWeather);

        URI location = URI.create("/weather/" + savedWeather.city());
        return ResponseEntity.created(location).body(savedWeather);
    }
}