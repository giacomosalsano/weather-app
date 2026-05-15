package com.weather_app.core.domain;

import java.time.LocalDateTime;

public record Weather(
    String city,
    Double temperature,
    String description,
    LocalDateTime timestamp
) {}