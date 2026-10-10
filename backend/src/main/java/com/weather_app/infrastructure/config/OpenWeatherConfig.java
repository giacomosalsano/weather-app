package com.weather_app.infrastructure.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.web.client.RestClient;

@Configuration
@Profile("!mock")
public class OpenWeatherConfig {

    /**
     * TO LEARN: RestClient is Spring's modern synchronous HTTP client.
     * We configure a base URL once; the adapter only appends the path + query params.
     */
    @Bean
    RestClient openWeatherRestClient(@Value("${weather.api.base-url}") String baseUrl) {
        return RestClient.builder()
                .baseUrl(baseUrl)
                .build();
    }
}
