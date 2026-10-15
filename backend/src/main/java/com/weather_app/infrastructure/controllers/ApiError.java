package com.weather_app.infrastructure.controllers;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * TO LEARN: Stable JSON shape for API errors.
 * {@code fieldErrors} is only present for validation failures (400);
 * other errors omit it thanks to {@code @JsonInclude(NON_EMPTY)}.
 */
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public record ApiError(
        int status,
        String error,
        String message,
        String path,
        Map<String, String> fieldErrors
) {
    /** Convenience for errors without per-field details (404, 500, ...). */
    public ApiError(int status, String error, String message, String path) {
        this(status, error, message, path, Map.of());
    }
}
