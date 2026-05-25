package com.weather_app.infrastructure.controllers;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.GetWeatherUseCase;

@RestController
@RequestMapping("/weather")
public class WeatherController {

  private final GetWeatherUseCase getWeatherUseCase;

  public WeatherController(GetWeatherUseCase getWeatherUseCase) {
    this.getWeatherUseCase = getWeatherUseCase;
  }

  @GetMapping("/{city}")
  public ResponseEntity<Weather> getWeather(@PathVariable String city) {
    try {
      Weather weather = getWeatherUseCase.execute(city);
      return ResponseEntity.ok(weather);
    } catch (RuntimeException e) {
      return ResponseEntity.notFound().build();
    }
  }
}