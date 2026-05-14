package com.weather_app.infrastructure.controllers;

// Um Record é como um 'type' ou 'interface' no TS, mas gera imutabilidade e getters automaticamente
public record HelloResponse(String message, String status) {}