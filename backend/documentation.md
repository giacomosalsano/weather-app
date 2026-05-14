# Weather App Backend - Complete Documentation

## 📋 Overview

Weather App Backend is a Java-based service built with Spring Boot and Maven.  
At its current stage, the project is a foundational backend scaffold prepared for future weather-related features, with containerized local infrastructure and baseline test coverage.

---

## 🏗️ System Architecture

### Tech Stack

- **Backend:** Java 21 + Spring Boot 3.4.x
- **Database:** PostgreSQL 15 (Relational)
- **Security:** Spring Security (Stateful/JWT transition planned)
- **Containerization:** Docker Multi-stage + Compose

### Current Runtime Flow

**1.** Start containers (PostgreSQL + backend)    →    **2.** Wait for DB port availability     →    **3.** Run Spring Boot application JAR

---

## 🗂️ Project Structure

```text
backend/
  ├─ src/
  │  ├─ main/
  │  │  ├─ java/com/example/weather_app/
  │  │  │  └─ WeatherAppApplication.java      # Spring Boot entry point
  │  │  └─ resources/
  │  │     └─ application.properties          # App base configuration
  │  └─ test/
  │     └─ java/com/example/weather_app/
  │        └─ WeatherAppApplicationTests.java # Context-load smoke test
  ├─ scripts/
  │  └─ start.sh                              # Wait-for-DB + app startup script
  ├─ compose.yaml                             # Local services (PostgreSQL + backend)
  ├─ dockerfile                               # Multi-stage Docker image
  ├─ pom.xml                                  # Maven dependencies and plugins
  ├─ mvnw / mvnw.cmd                          # Maven Wrapper scripts
  └─ wrapper/maven-wrapper.properties         # Maven Wrapper config
```

---

## 🧩 Main Components

- **`WeatherAppApplication`**  
  Main Spring Boot bootstrap class responsible for application startup.

- **`application.properties`**  
  Defines the application name (`weather-app`). Additional runtime properties are currently injected through Docker environment variables.

- **`compose.yaml`**  
  Declares two services:
  - `db`: PostgreSQL 15 Alpine, exposed on port `5432`;
  - `backend`: builds from `./backend`, exposed on port `8080`, and configured with datasource environment variables.

- **`dockerfile`**  
  Uses a multi-stage strategy:
  1. Build stage with `eclipse-temurin:21-jdk-alpine` and Maven packaging;
  2. Runtime stage with `eclipse-temurin:21-jre-alpine`, copying the generated JAR and startup script.

- **`scripts/start.sh`**  
  Waits for database availability (`nc -z $DB_HOST 5432`) before running `java -jar app.jar`.

---

## 🔐 Security Status

- Spring Security dependencies are present in `pom.xml`.
- No explicit security configuration classes, authentication flow, or protected endpoint strategy are implemented yet.
- This means security infrastructure is prepared at dependency level but not yet customized for business requirements.

---

## 🧪 Testing Status

- Current test suite includes a basic Spring Boot context load test (`contextLoads`).
- No controller, service, repository, or integration tests exist yet.
- Test dependencies for Web MVC, JPA, and Security are already included, enabling expansion of test coverage.

---

## 📦 Dependencies

### Production / Runtime

- `spring-boot-starter-webmvc`
- `spring-boot-starter-data-jpa`
- `spring-boot-starter-security`
- `spring-boot-devtools` (optional, runtime scope)
- `spring-boot-docker-compose` (optional, runtime scope)
- `lombok` (optional)

### Test

- `spring-boot-starter-webmvc-test`
- `spring-boot-starter-data-jpa-test`
- `spring-boot-starter-security-test`

---
## 🚀 Local Development and Execution

### 🛠️ Prerequisites
- **Colima** (recomended for macOS users with **Intel**)
- **Docker & Docker Compose**

### 1) Building the System
To see the styled build process:
```bash
  docker compose build --progress=plain
```

### 2) Running the Application

```bash
  docker compose up
```

### 3) Verifying the Service

Once you see the Spring Boot logo, test the custom endpoint:

```bash
  curl http://localhost:8080/hello
```

### Expected Outcome: 
```json
  {"message":"Java 21 is running!","status":"UP"}
```

---

## 🌟 Current Strengths

1. **Modern Java Baseline** - Java 21 with recent Spring Boot foundation.
2. **Container-Ready Setup** - Multi-stage Docker build and compose-based local stack.
3. **Persistence/Security Starters Included** - Core backend capabilities already wired at dependency level.
4. **Clean Bootstrap State** - Minimal codebase that is easy to evolve intentionally.
5. **Maven Wrapper Standardization** - Consistent build tooling across environments.

---

## 🔧 Suggested Next Steps

### High Priority

1. **Define Domain and API Modules** - Introduce weather endpoints, DTOs, service layer, and persistence model.
2. **Add Explicit Security Configuration** - Configure authentication/authorization and public vs protected routes.
3. **Improve Configuration Management** - Add profile-based config (`dev`, `test`, `prod`) and environment validation.
4. **Expand Test Coverage** - Add unit and integration tests for controllers, services, and repositories.

### Medium Priority

1. **Database Migrations** - Introduce Flyway or Liquibase for versioned schema changes.
2. **Observability** - Add structured logging and health/readiness endpoints (Actuator).
3. **API Documentation** - Add OpenAPI/Swagger for endpoint discoverability.
4. **Error Handling Standardization** - Implement global exception handling with consistent error response format.

### Low Priority

1. **CI Pipeline** - Automate build, test, and image validation steps.
2. **Code Quality Gates** - Enforce static analysis and test coverage thresholds.
3. **Performance Baseline** - Add basic load testing and profiling as features mature.

---

## 🎯 Conclusion

The backend is currently a solid technical foundation rather than a feature-complete weather platform.  
It is well-positioned for iterative growth, with the essential runtime, dependency, and container infrastructure already in place.  
The next phase should focus on implementing business modules, formalizing security, and increasing test and operational maturity.