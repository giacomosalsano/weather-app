package com.weather_app.infrastructure.adapters.out.external;

import java.time.LocalDateTime;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import com.weather_app.core.domain.Weather;
import com.weather_app.core.ports.ExternalWeatherPort;

/**
 * TO LEARN: Real outbound adapter for ExternalWeatherPort.
 * The application core still depends only on the port interface — swapping
 * mock ↔ OpenWeather does not change WeatherService or WeatherController.
 */
@Component
@Profile("!mock")
public class OpenWeatherExternalAdapter implements ExternalWeatherPort {

    private final RestClient restClient;
    private final String apiKey;

    public OpenWeatherExternalAdapter(
            RestClient openWeatherRestClient,
            @Value("${weather.api.key}") String apiKey) {
        this.restClient = openWeatherRestClient;
        this.apiKey = apiKey;
    }

    @Override
    public Optional<Weather> fetchWeather(String city) {
        try {
            OpenWeatherResponse response = restClient.get()
                    .uri(uriBuilder -> uriBuilder
                            .path("/weather")
                            .queryParam("q", city)
                            .queryParam("appid", apiKey)
                            .queryParam("units", "metric")
                            .queryParam("lang", "pt_br")
                            .build())
                    .retrieve()
                    // Only unknown city (404) → empty Optional. 401 (bad key) still fails loudly.
                    .onStatus(status -> status.value() == 404, (req, res) -> {
                        throw new CityNotFoundException();
                    })
                    .body(OpenWeatherResponse.class);

            if (response == null || response.main() == null || response.weather() == null
                    || response.weather().isEmpty()) {
                return Optional.empty();
            }

            String description = response.weather().get(0).description();

            // TO LEARN: We keep the requested city name (e.g. "Lisboa") so the local
            // DB cache key matches GET /weather/{city}. OpenWeather often returns
            // the English name ("Lisbon") in response.name.
            return Optional.of(new Weather(
                    city,
                    response.main().temp(),
                    description,
                    LocalDateTime.now()));
        } catch (CityNotFoundException e) {
            return Optional.empty();
        }
    }

    /** Internal signal: OpenWeather returned a 4xx (typically unknown city). */
    private static final class CityNotFoundException extends RuntimeException {}
}
