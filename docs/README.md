# Documentação em PDF

## Guia de estudos

Arquivo gerado:

**[Guia-Arquitetura-Hexagonal-Weather-App.pdf](./Guia-Arquitetura-Hexagonal-Weather-App.pdf)**

Conteúdo (19 capítulos):

1. Introdução e objetivo do projeto  
2. Java 21 (records, DI, Optional)  
3. Arquitetura hexagonal aplicada  
4. Spring Boot e sintaxe usada  
5. Docker e ambiente local  
6. Papel de cada classe  
7. CRUD e API externa / microserviços  
8. Apache Kafka (primeiros passos)  
9. SonarQube  
10. Cucumber (BDD)  
11. Estratégia de testes  
12. Roadmap sugerido  
13–18. Maven, JPA, DDD, OpenAPI, CI/CD, resumo ferramenta × camada  
19. Referências  

## Regenerar o PDF

```bash
cd docs
python3 generate_study_guide.py
```

Requisito: `pip install fpdf2` (ou `pip3 install fpdf2`).

No macOS, o script usa **Arial Unicode** do sistema para caracteres em português.
