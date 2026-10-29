package com.weather_app.infrastructure.controllers;

import java.net.URI;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.GetAllWeathersUseCase;
import com.weather_app.core.ports.GetWeatherUseCase;
import com.weather_app.core.ports.SaveWeatherUseCase;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/weather")
public class WeatherController {

    private final GetWeatherUseCase getWeatherUseCase;
    private final GetAllWeathersUseCase getAllWeathersUseCase;
    private final SaveWeatherUseCase saveWeatherUseCase;

    // TO LEARN: Implementing the Interface Segregation Principle (SOLID). 
    // This way, the WeatherController requires both GetWeatherUseCase and SaveWeatherUseCase as separate dependencies instead of a single huge dependency.
    public WeatherController(GetWeatherUseCase getWeatherUseCase, GetAllWeathersUseCase getAllWeathersUseCase, SaveWeatherUseCase saveWeatherUseCase) {
        this.getWeatherUseCase = getWeatherUseCase;
        this.getAllWeathersUseCase = getAllWeathersUseCase;
        this.saveWeatherUseCase = saveWeatherUseCase;
    }

    @GetMapping("/{city}")
    // TO LEARN: PathVariable maps the URL segment into the city parameter.
    // No try/catch here: CityNotFoundException bubbles to GlobalExceptionHandler → 404 JSON.
    public ResponseEntity<Weather> getWeather(@PathVariable String city) {
        Weather weather = getWeatherUseCase.execute(city);
        return ResponseEntity.ok(weather);
    }

    // TO LEARN: @GetMapping sem caminho, junto com @RequestMapping("/weather"), é GET /weather.
    // @GetMapping("/") exigia a barra no final (GET /weather/). O de uma cidade continua em /{city}.
    // A resposta é List<Weather>. O controller não importa WeatherEntity.
    @GetMapping
    public ResponseEntity<List<Weather>> getAllWeather() {
        List<Weather> weathers = getAllWeathersUseCase.execute();
        return ResponseEntity.ok(weathers);
    }


    @PostMapping
    // TO LEARN: @Valid triggers Bean Validation on WeatherRequest BEFORE this method runs.
    // Invalid body → MethodArgumentNotValidException → 400 (handler), not a DB insert.
    public ResponseEntity<Weather> createWeather(@Valid @RequestBody WeatherRequest request) {
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