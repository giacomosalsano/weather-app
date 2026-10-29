package com.weather_app.core.ports;

import java.util.List;

import com.weather_app.core.domain.Weather;

// TO LEARN: Use case próprio, separado de GetWeatherUseCase.
// Aquele recebe uma cidade e devolve um Weather. Este não recebe nada e devolve a lista.
// O retorno é o domínio (Weather). WeatherEntity é linha de tabela e fica só no adapter.
public interface GetAllWeathersUseCase {
    List<Weather> execute();
}
