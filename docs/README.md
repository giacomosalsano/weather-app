# PDF Documentation

## Study Guide

Generated file:

**[Guia-Arquitetura-Hexagonal-Weather-App.pdf](./Guia-Arquitetura-Hexagonal-Weather-App.pdf)**

Contents (19 chapters):

1. Introduction and project goals  
2. Java 21 (records, DI, Optional)  
3. Hexagonal architecture in practice  
4. Spring Boot and syntax in use  
5. Docker and local environment  
6. Role of each class  
7. CRUD and external API / microservices  
8. Apache Kafka (first steps)  
9. SonarQube  
10. Cucumber (BDD)  
11. Testing strategy  
12. Suggested roadmap  
13–18. Maven, JPA, DDD, OpenAPI, CI/CD, tool × layer summary  
19. References  

## Regenerate the PDF

```bash
cd docs
python3 generate_study_guide.py
```

Requirement: `pip install fpdf2` (or `pip3 install fpdf2`).

On macOS, the script uses the system's **Arial Unicode** font for proper UTF-8 character rendering.
