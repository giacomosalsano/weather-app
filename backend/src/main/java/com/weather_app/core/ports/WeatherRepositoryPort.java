package com.weather_app.core.ports;

import java.util.List;
import java.util.Optional;

import com.weather_app.core.domain.Weather;

// TO LEARN: Outbound Port (SPI - Service Provider Interface)
// This is a port interface and it defines the contract for the weather repository.  
public interface WeatherRepositoryPort {
  Weather save(Weather weather);

  Optional<Weather> findByCity(String city);

  // TO LEARN: Mesma língua de save e findByCity: Weather, não WeatherEntity.
  // A porta não conhece JPA. Quem traduz a tabela para o domínio é o adapter.
  List<Weather> findAll();
}