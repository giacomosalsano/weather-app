# 🌤️ Weather App - Java 21 & Spring Boot

A high-performance, weather monitoring service built with **Java 21**, applying **Hexagonal Architecture** and modern backend practices.

## 🏗️ Architecture: Hexagonal (Ports & Adapters)
We use this pattern to decouple the application core from external technologies.

- **Core (Domain & Application):** Contains pure business logic and use cases. No framework dependencies.
- **Infrastructure (Adapters):** External world connections.
  - **Inbound:** REST Controllers (Spring Web).
  - **Outbound:** Persistence (JPA/PostgreSQL) and External API Clients.


## 🛠️ Tech Stack
- **Language:** Java 21 (LTS)
- **Framework:** Spring Boot 3.4.x
- **Build Tool:** Maven (mvnw)
- **Database:** PostgreSQL 15
- **Infrastructure:** Docker & Docker Compose (Colima optimized)

## 🚀 How to Run (Development)

1. **Build the containers:**

```bash
   docker compose build --progress=plain
```

2. **Start the environment:**

```bash
   docker compose up
```

3. **Verify the Health Check:**

```bash
   curl http://localhost:8080/hello
```

4. **Expected Response:**

```json
   {"message":"Java 21 is running!","status":"UP"}
```


## 🗂️ Project Structure

```plaintext
backend/
  ├── src/main/java/com/weather_app/
  │   ├── core/             # Business Logic (No Spring dependencies)
  │   │   ├── domain/       # Entities and Value Objects (Records)
  │   │   └── ports/        # Interfaces (In/Out)
  │   ├── application/      # Implementation of Use Cases
  │   └── infrastructure/   # Adapters and Config
  │       ├── config/       # Spring Configuration (Security, Beans)
  │       ├── controllers/  # Inbound Adapters (REST)
  │       └── persistence/  # Outbound Adapters (JPA/Entities)
```
---