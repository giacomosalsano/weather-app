package com.weather_app.infrastructure.controllers;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/**
 * TO LEARN: Input DTO (API boundary) — not the domain Weather.
 * Validation annotations declare rules HERE, at the edge of the system.
 * If they fail, the controller method never runs; Spring throws
 * MethodArgumentNotValidException → GlobalExceptionHandler → 400.
 */
public record WeatherRequest(
        @NotBlank(message = "city is required")
        @Size(max = 255, message = "city must be at most 255 characters")
        String city,

        @NotNull(message = "temperature is required")
        Double temperature,

        @NotBlank(message = "description is required")
        @Size(max = 255, message = "description must be at most 255 characters")
        String description
) {}
