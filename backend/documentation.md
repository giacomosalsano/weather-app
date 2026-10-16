# Weather App Backend — Documentation

Status of the backend as of the OpenWeather + error-handling + validation work.  
This file replaces the old scaffold-era notes (`com.example.*`, “features not built yet”).

---

## Overview

Java 21 / Spring Boot **4.0.5** service that:

1. Exposes a small REST API for weather
2. Caches results in PostgreSQL
3. Fetches missing cities from **OpenWeatherMap** (or a mock profile)
4. Returns consistent JSON errors for “not found” and invalid input

Architecture: **hexagonal** (ports & adapters).

---

## Tech stack

| Area | Choice |
|------|--------|
| Language | Java 21 |
| Framework | Spring Boot 4.0.5 |
| Web | `spring-boot-starter-webmvc` |
| Persistence | `spring-boot-starter-data-jpa` + PostgreSQL 15 |
| Migrations | Flyway (`spring-boot-starter-flyway`) |
| Security | `spring-boot-starter-security` + `SecurityConfig` |
| Validation | `spring-boot-starter-validation` |
| External weather | OpenWeatherMap Current Weather API |
| Build / run | Maven Wrapper, Docker multi-stage, Compose at repo root |

---

## Runtime flow

1. `docker compose up` starts `db` (Postgres) and `backend`
2. `scripts/start.sh` waits for `$DB_HOST:5432`, then `java -jar app.jar`
3. Flyway applies `classpath:db/migration` (creates `tb_weather`)
4. API listens on **8080**

### Environment variables (backend container)

| Variable | Purpose |
|----------|---------|
| `SPRING_DATASOURCE_URL` | JDBC URL |
| `SPRING_DATASOURCE_USERNAME` / `PASSWORD` | DB credentials |
| `DB_HOST` | Used by `start.sh` wait loop |
| `WEATHER_API_KEY` | OpenWeatherMap key (from host `.env`) |

Optional: `SPRING_PROFILES_ACTIVE=mock` → `WeatherMockExternalAdapter` instead of OpenWeather.

---

## Package map

```text
com.weather_app
├── WeatherAppApplication
├── core
│   ├── domain
│   │   ├── Weather                      # record
│   │   └── CityNotFoundException        # domain failure → mapped to 404
│   └── ports
│       ├── GetWeatherUseCase
│       ├── SaveWeatherUseCase
│       ├── WeatherRepositoryPort
│       └── ExternalWeatherPort
├── application.services
│   └── WeatherService                   # cache-aside + save
└── infrastructure
    ├── config
    │   ├── SecurityConfig               # CSRF off; public /hello, /weather, /error
    │   └── OpenWeatherConfig            # RestClient bean (@Profile("!mock"))
    ├── controllers
    │   ├── HelloController / HelloResponse
    │   ├── WeatherController / WeatherRequest
    │   ├── ApiError
    │   └── GlobalExceptionHandler
    └── adapters.out
        ├── persistence                  # Entity, JpaRepository, PersistenceAdapter
        └── external                     # OpenWeather* + WeatherMockExternalAdapter
```

---

## HTTP API

| Method | Path | Behaviour |
|--------|------|-----------|
| `GET` | `/hello` | Simple health-style JSON |
| `GET` | `/weather/{city}` | DB → else OpenWeather → save → `200` `Weather` |
| `POST` | `/weather` | Body `WeatherRequest` → `201` + `Location` |

### Error responses (`ApiError`)

Shared JSON shape:

```json
{
  "status": 404,
  "error": "Not Found",
  "message": "City not found: Atlantis",
  "path": "/weather/Atlantis"
}
```

| Case | Status | Mechanism |
|------|--------|-----------|
| City not in DB and not found externally | **404** | `CityNotFoundException` |
| Invalid POST body | **400** | `@Valid` + `MethodArgumentNotValidException` (+ optional `fieldErrors`) |
| Unexpected failure | **500** | Fallback handler (generic message; details in logs) |

### Validation rules (`WeatherRequest`)

- `city` / `description`: `@NotBlank`, `@Size(max = 255)`
- `temperature`: `@NotNull`

---

## Persistence

- Table: `tb_weather` (`V1__create_tb_weather.sql`)
- `city` **UNIQUE NOT NULL**
- JPA: `spring.jpa.hibernate.ddl-auto=none` (schema owned by Flyway)
- `WeatherEntity`: getters/setters via Lombok; **constructors written by hand** (avoids Lombok `@AllArgsConstructor` / JDK 25+ “Flexible Constructor Bodies” IDE issue while `java.version=21`)

---

## External weather

- Port: `ExternalWeatherPort.fetchWeather(String city) → Optional<Weather>`
- **Default:** `OpenWeatherExternalAdapter` (`@Profile("!mock")`)
  - `RestClient`, `units=metric`, `lang=pt_br`
  - Maps JSON via `OpenWeatherResponse` DTO (infrastructure only)
  - Keeps the **requested** city name for cache key consistency (`Lisboa` vs API `Lisbon`)
  - HTTP 404 from OpenWeather → `Optional.empty()`
- **Mock:** `WeatherMockExternalAdapter` (`@Profile("mock")`) — only `"Londres"`

Config keys:

```properties
weather.api.base-url=https://api.openweathermap.org/data/2.5
weather.api.key=${WEATHER_API_KEY}
```

---

## Security

`SecurityConfig`:

- CSRF disabled (typical for JSON APIs)
- `permitAll`: `/hello`, `/weather`, `/weather/**`, `/error`
- Everything else: authenticated (no custom login/JWT yet — default Spring user may appear in logs)

---

## Testing status

- Only smoke test: `WeatherAppApplicationTests` (`contextLoads`)
- **Next learning step:** unit tests for `WeatherService` + `@WebMvcTest` for controller / validation / 404

Test starters already on the classpath: webmvc-test, data-jpa-test, security-test.

---

## Dependencies (main)

- `spring-boot-starter-webmvc`
- `spring-boot-starter-validation`
- `spring-boot-starter-data-jpa`
- `spring-boot-starter-security`
- `spring-boot-starter-flyway` (+ `flyway-database-postgresql`)
- `postgresql`
- `lombok` (optional)
- `spring-boot-devtools`, `spring-boot-docker-compose` (optional, runtime)

---

## Known gaps (intentional backlog)

Not yet handled with dedicated HTTP semantics:

- Duplicate `city` on POST (DB unique) → should become **409**
- OpenWeather auth/network failures → should become **502/503**
- Malformed JSON body → clearer **400** (`HttpMessageNotReadableException`)
- Path-variable validation on GET
- Automated tests, cache TTL, Actuator, OpenAPI, CI, real auth

---

## Local commands

From **repository root** (not `backend/`):

```bash
cp .env.example .env   # once
docker compose build backend
docker compose up -d

curl -s http://localhost:8080/hello
curl -s http://localhost:8080/weather/Porto | python3 -m json.tool
```

Compile without Docker:

```bash
cd backend && ./mvnw compile
```

---

## Conclusion

The backend is past the empty scaffold stage: hexagonal weather use cases, real external API, Flyway schema, validation, and global error JSON are in place.  
The next focused learning milestone is **automated tests**, then remaining error cases and operational polish.
