package com.weather_app.infrastructure.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public HelloResponse sayHello() {
        return new HelloResponse("Java 21 is running!", "UP");
    }
}