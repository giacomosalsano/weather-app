# PDF Documentation

Optional tooling, separate from the Java backend — used only to generate the study guide PDF.

## Prerequisite: `fpdf2`

The script uses the [fpdf2](https://pypi.org/project/fpdf2/) library (imported as `from fpdf import FPDF`). It is **not** part of the main application and does **not** belong in `pom.xml` or any backend dependency.

Install it in your Python environment (outside the Java backend), for example:

```bash
pip3 install --user fpdf2
```

Or, with an isolated venv under `docs/` (recommended if your editor reports an unresolved import):

```bash
cd docs
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The `docs/requirements.txt` file lists only this dependency — it does not affect Maven or the app Docker setup.

Verify the installation:

```bash
python3 -c "from fpdf import FPDF; print('fpdf2 OK')"
```

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

On macOS, the script uses the system **Arial Unicode** font for correct UTF-8 character rendering (Portuguese content in the PDF).
