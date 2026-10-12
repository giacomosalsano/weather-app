package com.weather_app.infrastructure.controllers;

/**
 * TO LEARN: Stable JSON shape for API errors.
 * Clients always get the same fields — easier to consume than an empty 404 body.
 */
public record ApiError(
        int status,
        String error,
        String message,
        String path
) {}
