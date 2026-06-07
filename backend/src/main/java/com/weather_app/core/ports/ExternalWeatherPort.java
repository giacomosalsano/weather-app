package com.weather_app.core.ports;

import java.util.Optional;

import com.weather_app.core.domain.Weather;


public interface ExternalWeatherPort {
    Optional<Weather> fetchWeather(String city);
}