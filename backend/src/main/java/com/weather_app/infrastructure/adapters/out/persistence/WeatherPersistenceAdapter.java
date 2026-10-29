package com.weather_app.infrastructure.adapters.out.persistence;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Component;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.WeatherRepositoryPort;

@Component // Avisa ao Spring que esta classe é um componente que pode ser injetado nas
           // portas
public class WeatherPersistenceAdapter implements WeatherRepositoryPort {

    private final WeatherJpaRepository jpaRepository;

    public WeatherPersistenceAdapter(WeatherJpaRepository jpaRepository) {
        this.jpaRepository = jpaRepository;
    }

    @Override
    public Weather save(Weather weather) {
        // Converte de Domain Record para Database Entity
        WeatherEntity entity = new WeatherEntity(
                null,
                weather.city(),
                weather.temperature(),
                weather.description(),
                weather.timestamp());

        WeatherEntity savedEntity = jpaRepository.save(entity);

        // Retorna mapeado de volta para Domain Record
        return new Weather(
                savedEntity.getCity(),
                savedEntity.getTemperature(),
                savedEntity.getDescription(),
                savedEntity.getTimestamp());
    }

    @Override
    public Optional<Weather> findByCity(String city) {
        return jpaRepository.findByCity(city)
                .map(entity -> new Weather(
                        entity.getCity(),
                        entity.getTemperature(),
                        entity.getDescription(),
                        entity.getTimestamp()));
    }

    // TO LEARN: jpaRepository.findAll() devolve List<WeatherEntity>, e List não tem map().
    // stream() abre a lista, map traduz cada linha para Weather (igual ao findByCity)
    // e toList() fecha de novo. O JPA continua escondido atrás desta classe.
    @Override
    public List<Weather> findAll() {
        return jpaRepository.findAll().stream()
                .map(entity -> new Weather(
                        entity.getCity(),
                        entity.getTemperature(),
                        entity.getDescription(),
                        entity.getTimestamp()))
                .toList();
    }
}