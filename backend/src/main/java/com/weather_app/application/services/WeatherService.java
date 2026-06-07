package com.weather_app.application.services;

import org.springframework.stereotype.Service;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.ExternalWeatherPort;
import com.weather_app.core.ports.GetWeatherUseCase;
import com.weather_app.core.ports.SaveWeatherUseCase;
import com.weather_app.core.ports.WeatherRepositoryPort; 

@Service
public class WeatherService implements GetWeatherUseCase, SaveWeatherUseCase {

    private final WeatherRepositoryPort weatherRepositoryPort;
    private final ExternalWeatherPort externalWeatherPort; 

    // Dependency Injection via Constructor
    public WeatherService(WeatherRepositoryPort weatherRepositoryPort, ExternalWeatherPort externalWeatherPort) {
        this.weatherRepositoryPort = weatherRepositoryPort;
        this.externalWeatherPort = externalWeatherPort;
    }

    @Override
    public Weather execute(String city) {
        // Smart Flow:
        // 1. Try to search in the local database (Our cache)
        return weatherRepositoryPort.findByCity(city)
            .orElseGet(() -> {
                // 2. If not found in the database, invoke the external port to search on the internet
                Weather externalWeather = externalWeatherPort.fetchWeather(city)
                    .orElseThrow(() -> new RuntimeException("City not found: " + city));
                
                // 3. Save the result of the internet in the local database for future queries
                return weatherRepositoryPort.save(externalWeather);
            });
    }

    @Override
    public Weather execute(Weather weather) {
        return weatherRepositoryPort.save(weather);
    }
}