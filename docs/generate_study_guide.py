#!/usr/bin/env python3
"""Generate the study guide in PDF for the Weather App."""

import sys
from pathlib import Path

try:
    from fpdf import FPDF  # pyright: ignore[reportMissingModuleSource]
except ImportError:
    print(
        "Missing dependency: fpdf2\n"
        "Install outside the main project:\n"
        "  pip3 install --user fpdf2\n"
        "See docs/README.md for details.",
        file=sys.stderr,
    )
    sys.exit(1)

DOCS_DIR = Path(__file__).resolve().parent
OUTPUT = DOCS_DIR / "Guia-Arquitetura-Hexagonal-Weather-App.pdf"


def ensure_fonts() -> tuple[str, str]:
    """Fonts with support for UTF-8 (portuguese)."""
    candidates = [
        (
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ),
        (
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            return regular, bold

    fonts_dir = DOCS_DIR / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    regular = fonts_dir / "DejaVuSans.ttf"
    bold = fonts_dir / "DejaVuSans-Bold.ttf"
    if not regular.exists():
        import urllib.request

        urls = [
            (
                "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf",
                regular,
            ),
            (
                "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf",
                bold,
            ),
        ]
        for url, dest in urls:
            urllib.request.urlretrieve(url, dest)
    return str(regular), str(bold)


class StudyGuidePDF(FPDF):
    def __init__(self, regular: str, bold: str):
        super().__init__(format="A4")
        self.regular = regular
        self.bold = bold
        self.add_font("AppFont", "", regular)
        self.add_font("AppFont", "B", bold)
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

    def footer(self):
        self.set_y(-15)
        self.set_font("AppFont", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def cover(self):
        self.add_page()
        self.set_font("AppFont", "B", 26)
        self.set_text_color(30, 60, 120)
        self.multi_cell(0, 14, "Weather App\nGuia de Estudos", align="C")
        self.ln(8)
        self.set_font("AppFont", "", 14)
        self.set_text_color(50, 50, 50)
        self.multi_cell(
            0,
            8,
            "Arquitetura Hexagonal · Java 21 · Spring Boot · Docker\n"
            "Evolução: APIs externas, Kafka, SonarQube, Cucumber",
            align="C",
        )
        self.ln(20)
        self.set_font("AppFont", "", 11)
        self.multi_cell(
            0,
            7,
            "Documento gerado a partir do estado real do repositório weather-app.\n"
            "Público: desenvolvedores que estudam backend com Ports & Adapters.",
            align="C",
        )

    def h1(self, text: str):
        self.add_page()
        self.set_font("AppFont", "B", 18)
        self.set_text_color(30, 60, 120)
        self.multi_cell(0, 10, text)
        self.ln(4)
        self.set_draw_color(30, 60, 120)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(6)
        self._reset_x()

    def _reset_x(self):
        self.set_x(self.l_margin)

    def h2(self, text: str):
        self.ln(4)
        self._reset_x()
        self.set_font("AppFont", "B", 14)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def h3(self, text: str):
        self.ln(2)
        self._reset_x()
        self.set_font("AppFont", "B", 12)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body(self, text: str):
        self._reset_x()
        self.set_font("AppFont", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code(self, text: str):
        self._reset_x()
        self.set_font("AppFont", "", 9)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(20, 20, 20)
        for line in text.split("\n"):
            self.cell(0, 5, "  " + line, ln=True, fill=True)
        self.ln(3)
        self.set_font("AppFont", "", 11)

    def bullet(self, text: str):
        self._reset_x()
        self.set_font("AppFont", "", 11)
        self.multi_cell(0, 6, "  - " + text)


def build_pdf():
    regular, bold = ensure_fonts()
    pdf = StudyGuidePDF(regular, bold)
    pdf.cover()

    # --- Capítulo 1 ---
    pdf.h1("1. Introdução e objetivo do projeto")
    pdf.body(
        "O Weather App é um serviço backend em Java 21 com Spring Boot 4.0.5, "
        "organizado em Arquitetura Hexagonal (Ports & Adapters). O objetivo pedagógico "
        "é separar regras de negócio de detalhes técnicos: HTTP, JPA, PostgreSQL e Docker "
        "ficam na borda; o núcleo permanece testável e independente de framework."
    )
    pdf.body(
        "Neste momento o projeto já possui domínio Weather, portas de entrada/saída, "
        "WeatherService, adaptador JPA e endpoint de saúde /hello. Ainda falta o "
        "controller REST de clima — o fluxo de negócio está pronto, mas não exposto via HTTP."
    )

    pdf.h2("1.1 Stack real (pom.xml e docker-compose)")
    pdf.bullet("Java 21 (LTS) — records, var, pattern matching, virtual threads (opcional)")
    pdf.bullet("Spring Boot 4.0.5 — Web MVC, Data JPA, Security, DevTools, Docker Compose support")
    pdf.bullet("PostgreSQL 15 Alpine — banco relacional no Docker")
    pdf.bullet("Maven (mvnw) — build e empacotamento JAR")
    pdf.bullet("Lombok — reduz boilerplate em entidades JPA")
    pdf.bullet("Docker multi-stage — JDK 21 para build, JRE 21 para runtime")

    # --- Capítulo 2 Java ---
    pdf.h1("2. Java 21 no projeto")
    pdf.h2("2.1 Records como modelo de domínio")
    pdf.body(
        "A classe Weather no pacote core.domain é um record: tipo imutável com construtor, "
        "acessores e equals/hashCode gerados pelo compilador. Records expressam Value Objects "
        "ou entidades simples sem comportamento pesado — ideal para o núcleo hexagonal."
    )
    pdf.code(
        'public record Weather(\n'
        '    String city,\n'
        '    Double temperature,\n'
        '    String description,\n'
        '    LocalDateTime timestamp\n'
        ') {}'
    )
    pdf.body(
        "Boas práticas: use records no core quando o objeto é principalmente dados; "
        "mantenha validações de negócio em métodos estáticos de fábrica ou em serviços de aplicação."
    )

    pdf.h2("2.2 Injeção de dependência por construtor")
    pdf.body(
        "WeatherService e WeatherPersistenceAdapter recebem dependências apenas pelo construtor. "
        "Isso torna dependências explícitas, facilita testes unitários com mocks e é preferível "
        "a @Autowired em campos (field injection)."
    )
    pdf.code(
        'public WeatherService(WeatherRepositoryPort weatherRepositoryPort) {\n'
        '    this.weatherRepositoryPort = weatherRepositoryPort;\n'
        '}'
    )

    pdf.h2("2.3 Optional e exceções")
    pdf.body(
        "A porta WeatherRepositoryPort retorna Optional<Weather> em findByCity — evita null "
        "e deixa explícito que a cidade pode não existir. O WeatherService usa orElseThrow; "
        "em produção, prefira exceções de domínio (ex.: CityNotFoundException no core) "
        "mapeadas para HTTP 404 na camada infrastructure."
    )

    # --- Capítulo 3 Hexagonal ---
    pdf.h1("3. Arquitetura Hexagonal aplicada")
    pdf.h2("3.1 Anéis e pacotes")
    pdf.body(
        "Núcleo (core): domain + ports — sem Spring, sem JPA.\n"
        "Aplicação (application): implementa casos de uso (GetWeatherUseCase).\n"
        "Infraestrutura (infrastructure): controllers, config, adapters.out.persistence."
    )
    pdf.body(
        "Regra de dependência: setas de import apontam sempre para dentro. "
        "Infrastructure → Application → Core. O Core nunca importa infrastructure."
    )

    pdf.h2("3.2 Portas")
    pdf.body(
        "Porta de entrada (driving): GetWeatherUseCase — o mundo externo chama execute(city).\n"
        "Porta de saída (driven): WeatherRepositoryPort — o core pede persistência sem saber se é JPA, "
        "arquivo ou API externa."
    )

    pdf.h2("3.3 Adaptadores")
    pdf.body(
        "Adaptador de saída: WeatherPersistenceAdapter implementa WeatherRepositoryPort, "
        "traduz Weather (domínio) ↔ WeatherEntity (JPA). Este é o Anti-Corruption Layer: "
        "o modelo de banco não contamina o domínio.\n"
        "Adaptador de entrada (a criar): WeatherController chamará GetWeatherUseCase, "
        "nunca WeatherService diretamente — desacopla REST da implementação."
    )

    pdf.h2("3.4 Fluxo de uma requisição GET /weather?city=X")
    pdf.body(
        "1. Cliente HTTP → WeatherController (infrastructure.controllers)\n"
        "2. Controller injeta GetWeatherUseCase → execute(city)\n"
        "3. WeatherService (application) orquestra a regra\n"
        "4. WeatherRepositoryPort.findByCity → WeatherPersistenceAdapter\n"
        "5. WeatherJpaRepository → SQL em tb_weather\n"
        "6. Mapeamento Entity → record Weather e resposta JSON"
    )
    pdf.body(
        "Validação atual: imports em core.* usam apenas java.* e com.weather_app.core.* — "
        "regra de dependência respeitada."
    )

    # --- Capítulo 4 Spring ---
    pdf.h1("4. Spring Boot e sintaxe usada")
    pdf.h2("4.1 @SpringBootApplication")
    pdf.body(
        "WeatherAppApplication dispara o contexto IoC: scan de componentes, auto-configuração "
        "de DataSource, JPA, Security e embedded Tomcat na porta 8080."
    )

    pdf.h2("4.2 Estereótipos Spring")
    pdf.bullet("@RestController + @GetMapping — adaptador HTTP (HelloController)")
    pdf.bullet("@Service — WeatherService registrado como bean")
    pdf.bullet("@Component — WeatherPersistenceAdapter")
    pdf.bullet("@Repository — WeatherJpaRepository (Spring Data)")
    pdf.bullet("@Configuration + @Bean — SecurityConfig define SecurityFilterChain")

    pdf.h2("4.3 Spring Data JPA")
    pdf.body(
        "WeatherJpaRepository extends JpaRepository<WeatherEntity, Long> e declara "
        "Optional<WeatherEntity> findByCity(String city). O Spring gera a query pelo nome do método "
        "(query derivation) — convenção findBy + Campo."
    )
    pdf.code(
        '@Entity\n'
        '@Table(name = "tb_weather")\n'
        'public class WeatherEntity { ... }'
    )

    pdf.h2("4.4 Spring Security")
    pdf.body(
        "SecurityConfig desabilita CSRF (comum em APIs stateless) e libera apenas /hello; "
        "demais rotas exigem autenticação. Ao criar GET /weather, adicione .requestMatchers(\"/weather/**\").permitAll() "
        "em dev ou configure JWT/OAuth2 para produção."
    )

    pdf.h2("4.5 Lombok")
    pdf.body(
        "@Getter @Setter @NoArgsConstructor @AllArgsConstructor em WeatherEntity: JPA exige construtor "
        "vazio; Lombok evita dezenas de linhas. O domínio Weather não usa Lombok — permanece puro."
    )

    # --- Capítulo 5 Docker ---
    pdf.h1("5. Docker e ambiente local")
    pdf.h2("5.1 docker-compose.yml")
    pdf.body(
        "Serviço db: imagem postgres:15-alpine, healthcheck com pg_isready, porta 5432.\n"
        "Serviço backend: build do dockerfile, depende do db healthy, variáveis SPRING_DATASOURCE_*."
    )

    pdf.h2("5.2 Dockerfile multi-stage")
    pdf.body(
        "Estágio 1 (build): eclipse-temurin:21-jdk-alpine, ./mvnw package -DskipTests.\n"
        "Estágio 2 (runtime): JRE 21, copia app.jar e start.sh. Benefício: imagem final menor, "
        "sem Maven nem código-fonte em produção."
    )

    pdf.h2("5.3 start.sh")
    pdf.body(
        "Script aguarda nc -z $DB_HOST 5432 antes de java -jar app.jar — evita falha de conexão "
        "quando o backend sobe antes do PostgreSQL estar aceitando conexões."
    )

    pdf.h2("5.4 Comandos úteis")
    pdf.code(
        "docker compose build --progress=plain\n"
        "docker compose up\n"
        'curl http://localhost:8080/hello'
    )

    # --- Capítulo 6 Classes ---
    pdf.h1("6. Papel de cada classe do projeto")
    classes = [
        ("Weather", "core.domain", "Modelo de negócio imutável (record)."),
        ("GetWeatherUseCase", "core.ports", "Contrato de caso de uso — porta de entrada."),
        ("WeatherRepositoryPort", "core.ports", "Contrato de persistência — porta de saída."),
        ("WeatherService", "application", "Implementa o caso de uso; orquestra regras."),
        ("WeatherPersistenceAdapter", "infrastructure", "Implementa repositório; mapeia Entity ↔ Domain."),
        ("WeatherEntity", "infrastructure", "Modelo JPA da tabela tb_weather."),
        ("WeatherJpaRepository", "infrastructure", "Acesso Spring Data ao banco."),
        ("HelloController", "infrastructure", "Health check; fora do fluxo de clima."),
        ("SecurityConfig", "infrastructure", "Política de segurança HTTP."),
    ]
    for name, pkg, role in classes:
        pdf.bullet(f"{name} ({pkg}): {role}")

    # --- Capítulo 7 Próximos passos CRUD ---
    pdf.h1("7. Próximos passos: CRUD e API externa")
    pdf.h2("7.1 Completar o adaptador de entrada")
    pdf.body(
        "Crie WeatherController com GET /weather/{city}, POST para cadastro e DELETE se necessário. "
        "Injete GetWeatherUseCase (interface), não a classe concreta. DTOs de request/response ficam "
        "em infrastructure (ex.: WeatherResponse) — nunca no core."
    )
    pdf.code(
        '@RestController\n'
        '@RequestMapping("/weather")\n'
        'public class WeatherController {\n'
        '  private final GetWeatherUseCase getWeatherUseCase;\n'
        '  @GetMapping("/{city}")\n'
        '  public WeatherResponse get(@PathVariable String city) {\n'
        '    Weather w = getWeatherUseCase.execute(city);\n'
        '    return WeatherResponse.from(w);\n'
        '  }\n'
        '}'
    )

    pdf.h2("7.2 CRUD completo na hexagonal")
    pdf.bullet("CreateWeatherUseCase + save na porta — já existe save em WeatherRepositoryPort")
    pdf.bullet("UpdateWeatherUseCase — update na porta ou save com merge")
    pdf.bullet("DeleteWeatherUseCase — nova operação deleteByCity na porta")
    pdf.bullet("ListWeatherUseCase — findAll na porta")
    pdf.body(
        "Cada operação = uma porta de entrada no core + serviço em application + método no adaptador JPA."
    )

    pdf.h2("7.3 Consumir API ou microserviço externo")
    pdf.body(
        "Para clima em tempo real (OpenWeather, etc.), crie nova porta de saída no core, "
        "ex.: WeatherProviderPort com Weather fetchCurrent(String city). "
        "Implemente WeatherApiAdapter em infrastructure.adapters.out.http usando RestClient ou WebClient."
    )
    pdf.body(
        "WeatherService pode combinar: primeiro consulta API externa, depois persiste via "
        "WeatherRepositoryPort (cache). O core só enxerga interfaces — troca de provedor não quebra regras."
    )
    pdf.body(
        "Microserviços: mesmo padrão — porta no core, cliente HTTP no adaptador; contratos versionados "
        "(OpenAPI), timeouts, circuit breaker (Resilience4j) na infrastructure, não no domain."
    )

    pdf.h2("7.4 Flyway e perfis")
    pdf.bullet("Flyway: migrations versionadas V1__create_weather.sql")
    pdf.bullet("application-dev.properties vs application-prod.properties")
    pdf.bullet("Spring Boot Actuator: /actuator/health para Kubernetes/Docker")

    # --- Capítulo 8 Kafka ---
    pdf.h1("8. Primeiros passos com Apache Kafka")
    pdf.body(
        "Kafka encaixa na hexagonal como adaptador de saída (publicar eventos) ou entrada "
        "(consumir). Exemplo: após salvar clima, publicar WeatherUpdatedEvent."
    )
    pdf.h2("8.1 Conceitos")
    pdf.bullet("Topic — canal de mensagens (ex.: weather.events)")
    pdf.bullet("Producer — adaptador que envia após caso de uso")
    pdf.bullet("Consumer — outro serviço ou listener na infrastructure")
    pdf.bullet("Partition / offset — paralelismo e ordenação por chave (city)")

    pdf.h2("8.2 Integração Spring")
    pdf.body(
        "Dependência: spring-kafka. Porta no core: WeatherEventPublisherPort. "
        "Adaptador: KafkaWeatherEventAdapter com KafkaTemplate. "
        "Nunca importe org.apache.kafka no core."
    )
    pdf.code(
        "# docker-compose (exemplo)\n"
        "  kafka:\n"
        "    image: confluentinc/cp-kafka:7.5.0\n"
        "  zookeeper: ...  # ou KRaft sem Zookeeper"
    )

    # --- Capítulo 9 SonarQube ---
    pdf.h1("9. SonarQube — qualidade e segurança")
    pdf.body(
        "SonarQube analisa bugs, vulnerabilidades, code smells e cobertura. "
        "Encaixa no pipeline CI após mvn test jacoco:report."
    )
    pdf.h2("9.1 Primeiros passos")
    pdf.bullet("Subir SonarQube via Docker ou SonarCloud (SaaS)")
    pdf.bullet("Gerar token e configurar sonar.projectKey no pom.xml (plugin sonar-maven)")
    pdf.bullet("Executar: mvn verify sonar:sonar -Dsonar.host.url=...")
    pdf.body(
        "Para hexagonal: configure exclusões de cobertura apenas para DTOs e Application main, "
        "não para core.domain — meta é alta cobertura no core e application."
    )

    # --- Capítulo 10 Cucumber ---
    pdf.h1("10. Cucumber — testes BDD")
    pdf.body(
        "Cucumber expressa comportamento em Gherkin (Given/When/Then), legível para negócio. "
        "Testa a aplicação de fora: HTTP + banco (integração) ou mocks das portas (unitário de serviço)."
    )
    pdf.code(
        "Funcionalidade: Consultar clima\n"
        "  Cenário: Cidade existente\n"
        "    Dado que existe clima cadastrado para \"Curitiba\"\n"
        "    Quando consulto o clima de \"Curitiba\"\n"
        "    Então recebo temperatura e descrição"
    )
    pdf.body(
        "Step definitions em src/test/java chamam MockMvc ou Testcontainers PostgreSQL. "
        "Mantenha steps finos; lógica de assert no core testado separadamente com JUnit 5."
    )

    # --- Capítulo 11 Testes ---
    pdf.h1("11. Estratégia de testes alinhada à arquitetura")
    pdf.bullet("Core/Application: JUnit 5 + Mockito — mock de WeatherRepositoryPort")
    pdf.bullet("Adapter JPA: @DataJpaTest + Testcontainers")
    pdf.bullet("Controller: @WebMvcTest mockando GetWeatherUseCase")
    pdf.bullet("E2E: @SpringBootTest + RestAssured ou MockMvc")
    pdf.body(
        "O pom já inclui spring-boot-starter-*-test — expanda além de contextLoads()."
    )

    # --- Capítulo 12 Roadmap ---
    pdf.h1("12. Roadmap sugerido (ordem de estudo)")
    steps = [
        "WeatherController + DTO + liberar rota no SecurityConfig",
        "CRUD completo + tratamento global de erros (@ControllerAdvice)",
        "Flyway + dados seed",
        "Adaptador HTTP para API meteorológica externa",
        "Testes unitários e integração (JUnit + Testcontainers)",
        "Cucumber para fluxos críticos",
        "CI (GitHub Actions): build, test, SonarQube",
        "Kafka para eventos de domínio",
        "Observabilidade: logs estruturados, métricas, tracing",
    ]
    for i, s in enumerate(steps, 1):
        pdf.bullet(f"{i}. {s}")

    pdf.h1("13. Maven e ciclo de build")
    pdf.body(
        "O Maven (mvnw no projeto) gerencia dependências transitivas do Spring Boot parent POM. "
        "Fases principais: compile → test → package (JAR executável com spring-boot-maven-plugin). "
        "O annotationProcessorPaths registra Lombok no compilador — sem isso, getters gerados falham."
    )
    pdf.code("./mvnw clean verify\n./mvnw spring-boot:run")
    pdf.body(
        "spring-boot-docker-compose (runtime): em dev local pode subir o compose automaticamente; "
        "em produção use apenas docker compose na raiz do monorepo."
    )

    pdf.h1("14. JPA e persistência — o que acontece no adaptador")
    pdf.body(
        "Hibernate (por baixo do Spring Data) sincroniza WeatherEntity com tb_weather. "
        "@GeneratedValue(IDENTITY) delega o id ao PostgreSQL SERIAL/BIGSERIAL. "
        "@Column(unique=true) em city evita duplicatas — alinhado à regra de negócio."
    )
    pdf.body(
        "O adaptador nunca retorna WeatherEntity para fora da infrastructure: sempre converte para "
        "record Weather. Se amanhã migrar para MongoDB, cria MongoWeatherAdapter implementando a "
        "mesma porta — WeatherService não muda."
    )

    pdf.h1("15. Como hexagonal se relaciona com DDD e Clean Architecture")
    pdf.body(
        "Hexagonal ≈ Ports & Adapters (Cockburn). Clean Architecture (Uncle Bob) usa camadas "
        "Entities / Use Cases / Interface Adapters / Frameworks — mapeamento direto: "
        "core.domain = Entities; application = Use Cases; infrastructure = Frameworks; "
        "ports = boundaries. DDD agrega Aggregates e Domain Events; um evento WeatherUpdated "
        "pode nascer no core e ser publicado por adaptador Kafka sem poluir o domínio."
    )

    pdf.h1("16. OpenAPI, validação e boas práticas REST")
    pdf.bullet("springdoc-openapi: documentação automática em /swagger-ui")
    pdf.bullet("jakarta.validation @NotBlank no DTO de entrada — validação na borda")
    pdf.bullet("Padrão de erro RFC 7807 (Problem Details) via @ControllerAdvice")
    pdf.bullet("Idempotência em PUT; POST retorna 201 + Location header")
    pdf.body(
        "Versionamento: /api/v1/weather evita quebrar clientes ao evoluir contratos."
    )

    pdf.h1("17. Pipeline CI/CD (visão inicial)")
    pdf.code(
        "# Exemplo GitHub Actions (conceitual)\n"
        "jobs:\n"
        "  build:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-java@v4\n"
        "        with: { java-version: '21' }\n"
        "      - run: ./mvnw -B verify\n"
        "      - run: docker build -t weather-backend ./backend"
    )
    pdf.body(
        "SonarQube entra após verify. Imagem Docker publicada em registry; deploy em Kubernetes "
        "com probes apontando para Actuator health."
    )

    pdf.h1("18. Resumo: encaixe ferramenta × camada hexagonal")
    pdf.body(
        "Java 21 + records → core.domain | Spring @Service → application | "
        "@RestController → infrastructure in | JPA + PostgreSQL → infrastructure out | "
        "RestClient/API → nova porta out | KafkaTemplate → porta out eventos | "
        "Cucumber/MockMvc → testes atravessam borda | SonarQube → qualidade transversal | "
        "Docker → empacota infrastructure runtime."
    )

    pdf.h1("19. Referências rápidas")
    pdf.bullet("Alistair Cockburn — Hexagonal Architecture (original)")
    pdf.bullet("Spring Boot Reference Documentation 4.x")
    pdf.bullet("PostgreSQL 15 Docs — tipos e índices")
    pdf.bullet("Docker Docs — multi-stage builds, compose depends_on")
    pdf.bullet("Apache Kafka Documentation — producers/consumers")
    pdf.bullet("SonarQube Docs — quality gates")
    pdf.bullet("Cucumber.io — Gherkin reference")

    pdf.output(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    path = build_pdf()
    print(f"PDF generated: {path}")
