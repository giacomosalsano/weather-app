package com.weather_app.infrastructure.adapters.out.external;

import java.util.List;

/**
 * TO LEARN: This DTO mirrors only the JSON fields we need from OpenWeatherMap.
 * It lives in infrastructure — the domain record {@code Weather} must not know
 * about OpenWeather's JSON shape (main.temp, weather[0].description, etc.).
 */
public record OpenWeatherResponse(
        String name,
        Main main,
        List<WeatherItem> weather
) {
    public record Main(Double temp) {}

    public record WeatherItem(String description) {}
}
