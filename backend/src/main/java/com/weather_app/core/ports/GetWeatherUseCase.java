package com.weather_app.core.ports;

import com.weather_app.core.domain.Weather;

public interface GetWeatherUseCase {

    Weather execute(String city);
}
