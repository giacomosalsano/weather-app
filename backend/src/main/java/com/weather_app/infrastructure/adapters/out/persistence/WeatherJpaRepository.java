package com.weather_app.infrastructure.adapters.out.persistence;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface WeatherJpaRepository extends JpaRepository<WeatherEntity, Long> {
    Optional<WeatherEntity> findByCity(String city);

    // TO LEARN: findAll() já existe em JpaRepository e devolve List<WeatherEntity>.
    // Não declare de novo aqui. Quem converte essa lista em List<Weather> é o adapter.
}