package com.weather_app.infrastructure.adapters.out.external;

import java.time.LocalDateTime;
import java.util.Optional;

import org.springframework.stereotype.Component;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.ExternalWeatherPort;

@Component // This tells the Spring that this class is a valid Bean for injection!
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