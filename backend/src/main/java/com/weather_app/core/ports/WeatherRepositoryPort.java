package com.weather_app.core.ports;

import java.util.Optional;

import com.weather_app.core.domain.Weather;

public interface WeatherRepositoryPort {
  Weather save(Weather weather);

  Optional<Weather> findByCity(String city);
}