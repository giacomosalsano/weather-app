package com.weather_app.application.services;

import org.springframework.stereotype.Service;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.GetWeatherUseCase;
import com.weather_app.core.ports.SaveWeatherUseCase;
import com.weather_app.core.ports.WeatherRepositoryPort;

@Service
public class WeatherService implements GetWeatherUseCase, SaveWeatherUseCase {

  private final WeatherRepositoryPort weatherRepositoryPort;

  // Dependency Injection via Construtor
  public WeatherService(WeatherRepositoryPort weatherRepositoryPort) {
    this.weatherRepositoryPort = weatherRepositoryPort;
  }

  @Override
  public Weather execute(String city) {
    return weatherRepositoryPort.findByCity(city)
        .orElseThrow(() -> new RuntimeException("City not found: " + city));
  }

  @Override
    public Weather execute(Weather weather) {
        // We can put business rules here before saving
        return weatherRepositoryPort.save(weather);
    }
}