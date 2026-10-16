# Weather App — Java 21 & Spring Boot

Learning-oriented weather backend using **Hexagonal Architecture** (ports & adapters).  
Local stack runs with Docker Compose (PostgreSQL + Spring Boot API).

## Architecture

| Layer | Responsibility |
|-------|----------------|
| **Core** (`domain` + `ports`) | Pure business concepts and contracts — no Spring/JPA |
| **Application** | Use-case implementations (`WeatherService`) |
| **Infrastructure** | REST controllers, JPA, OpenWeather HTTP client, security, error handling |

**Smart GET flow:** look up city in PostgreSQL (cache) → if missing, call OpenWeatherMap → save → return.

## Tech stack

- Java **21**
- Spring Boot **4.0.5** (Web MVC, Data JPA, Security, Validation, Flyway)
- PostgreSQL **15**
- OpenWeatherMap (Current Weather API, free tier)
- Maven Wrapper + Docker multi-stage build

## Prerequisites

- Docker & Docker Compose
- An [OpenWeatherMap](https://home.openweathermap.org/api_keys) API key

```bash
cp .env.example .env
# edit .env and set WEATHER_API_KEY=...
```

Never commit `.env` (it is gitignored).

## How to run

```bash
docker compose build --progress=plain
docker compose up
```

Health check:

```bash
curl -s http://localhost:8080/hello
# {"message":"Java 21 is running!","status":"UP"}
```

### API examples

```bash
# Cache miss → OpenWeather → persist
curl -s http://localhost:8080/weather/Porto | python3 -m json.tool

# Unknown city → 404 JSON (ApiError)
curl -s http://localhost:8080/weather/UnexistentCityXYZ | python3 -m json.tool

# Invalid POST body → 400 + fieldErrors
curl -s -X POST http://localhost:8080/weather \
  -H "Content-Type: application/json" \
  -d '{"city":"","temperature":null,"description":""}' | python3 -m json.tool

# Valid create → 201 + Location
curl -s -i -X POST http://localhost:8080/weather \
  -H "Content-Type: application/json" \
  -d '{"city":"Lisbon","temperature":22.0,"description":"Sunny"}'
```

### Offline mock profile

By default the real OpenWeather adapter is active (`@Profile("!mock")`).  
To use the fake adapter (only `"London"`):

```bash
# e.g. set on the backend service:
# SPRING_PROFILES_ACTIVE=mock
```

## Project structure

```plaintext
weather-app/
├── docker-compose.yml
├── .env.example
├── README.md
├── docs/                          # Optional study-guide PDF tooling
└── backend/
    ├── dockerfile
    ├── pom.xml
    ├── documentation.md           # Backend deep-dive
    └── src/main/java/com/weather_app/
        ├── core/
        │   ├── domain/            # Weather, CityNotFoundException
        │   └── ports/             # Use cases + outbound ports
        ├── application/services/  # WeatherService
        └── infrastructure/
            ├── config/            # SecurityConfig, OpenWeatherConfig
            ├── controllers/       # REST + ApiError + GlobalExceptionHandler
            └── adapters/out/
                ├── persistence/   # JPA entity, repository, adapter
                └── external/      # OpenWeather + mock adapters
```

## What is already implemented

- Hexagonal weather module (GET by city, POST create)
- Flyway migration `V1__create_tb_weather.sql`
- OpenWeatherMap outbound adapter + env-based API key
- Mock adapter via Spring profile `mock`
- Global errors: `CityNotFoundException` → **404**, validation → **400**
- Bean Validation on `WeatherRequest` (`@Valid`)
- Public routes: `/hello`, `/weather/**`, `/error`

## Next learning steps

1. Automated tests (service + `@WebMvcTest`)
2. More error cases (duplicate city **409**, external API failures **502**, malformed JSON **400**)
3. Cache TTL, Actuator, OpenAPI, CI

## Extra docs

- Backend details: [`backend/documentation.md`](./backend/documentation.md)
- Study guide PDF tooling: [`docs/README.md`](./docs/README.md)
