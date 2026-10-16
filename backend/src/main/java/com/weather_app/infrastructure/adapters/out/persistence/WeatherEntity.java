package com.weather_app.infrastructure.adapters.out.persistence;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

/**
 * TO LEARN: JPA entity for table tb_weather.
 * We keep {@code @Getter}/{@code @Setter} from Lombok, but write constructors
 * by hand. Recent Lombok + JDK 25/26 can generate {@code @AllArgsConstructor}
 * using "Flexible Constructor Bodies", which our {@code java.version=21}
 * project rejects in the IDE (error Java(4195411)). Explicit constructors
 * avoid that mismatch and are easier to read while learning.
 */
@Entity
@Table(name = "tb_weather")
@Getter
@Setter
public class WeatherEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String city;
    private Double temperature;
    private String description;
    private LocalDateTime timestamp;

    /** Required by JPA. */
    protected WeatherEntity() {}

    public WeatherEntity(Long id, String city, Double temperature, String description, LocalDateTime timestamp) {
        this.id = id;
        this.city = city;
        this.temperature = temperature;
        this.description = description;
        this.timestamp = timestamp;
    }
}
