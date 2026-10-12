package com.weather_app.core.domain;

/**
 * TO LEARN: Domain/application failure — "this city does not exist for us".
 * It does NOT know about HTTP. The web layer (GlobalExceptionHandler) decides
 * that this exception becomes a 404 JSON response.
 */
public class CityNotFoundException extends RuntimeException {

    public CityNotFoundException(String city) {
        super("City not found: " + city);
    }
}
