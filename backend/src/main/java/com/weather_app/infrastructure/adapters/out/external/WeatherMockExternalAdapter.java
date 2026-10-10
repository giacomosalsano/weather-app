package com.weather_app.infrastructure.adapters.out.external;

import java.time.LocalDateTime;
import java.util.Optional;

import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.ExternalWeatherPort;

/**
 * TO LEARN: Kept for offline demos. Active only with profile {@code mock}:
 *   SPRING_PROFILES_ACTIVE=mock
 * By default ({@code !mock}) the real OpenWeatherExternalAdapter is used instead.
 * Spring allows only ONE bean of type ExternalWeatherPort at a time.
 */
@Component
@Profile("mock")
public class WeatherMockExternalAdapter implements ExternalWeatherPort {

    @Override
    public Optional<Weather> fetchWeather(String city) {
        // Simulating that we went to the internet and searched for the weather dynamically if the city is London
        if (city.equalsIgnoreCase("Londres")) {
            Weather mockWeather = new Weather(
                "Londres", 
                15.0, 
                "Fine British rain (Simulated)", 
                LocalDateTime.now()
            );
            return Optional.of(mockWeather); // Wraps the object inside the Optional container
        }
        
        // If for any other city, we simulate that the external API did not find it
        return Optional.empty(); 
    }
}