package com.weather_app.infrastructure.controllers;

public record WeatherRequest(
    String city,
    Double temperature,
    String description
) {}