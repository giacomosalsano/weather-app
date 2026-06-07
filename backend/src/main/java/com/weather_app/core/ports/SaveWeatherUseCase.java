package com.weather_app.core.ports;

import com.weather_app.core.domain.Weather;

public interface SaveWeatherUseCase {
    Weather execute(Weather weather);
}