#!/usr/bin/env python3
"""Generate a printable study roadmap PDF for the Weather App."""

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
OUTPUT = DOCS_DIR / "Roteiro-Estudo-Weather-App.pdf"


def ensure_fonts() -> tuple[str, str]:
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

        for url, dest in [
            (
                "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf",
                regular,
            ),
            (
                "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf",
                bold,
            ),
        ]:
            urllib.request.urlretrieve(url, dest)
    return str(regular), str(bold)


class RoadmapPDF(FPDF):
    def __init__(self, regular: str, bold: str):
        super().__init__(format="A4")
        self.add_font("AppFont", "", regular)
        self.add_font("AppFont", "B", bold)
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(16, 16, 16)

    def footer(self):
        self.set_y(-11)
        self.set_font("AppFont", "", 8)
        self.set_text_color(110, 110, 110)
        self.cell(
            0,
            8,
            f"Weather App — Roteiro de Estudo (imprimir)  |  Página {self.page_no()}",
            align="C",
        )

    def _x(self):
        self.set_x(self.l_margin)

    def cover(self):
        self.add_page()
        self.ln(28)
        self.set_font("AppFont", "B", 24)
        self.set_text_color(25, 55, 110)
        self._x()
        self.multi_cell(0, 12, "Weather App", align="C")
        self.set_font("AppFont", "B", 17)
        self._x()
        self.multi_cell(0, 9, "Roteiro de Estudo da Arquitetura", align="C")
        self.ln(6)
        self.set_font("AppFont", "", 11)
        self.set_text_color(50, 50, 50)
        self._x()
        self.multi_cell(
            0,
            6.5,
            "Material para impressão e estudo aprofundado\n"
            "Java 21 · Spring Boot 4 · Hexagonal · Docker · OpenWeather\n\n"
            "Objetivo: compreender a aplicação de ponta a ponta —\n"
            "ler, interpretar, depurar e evoluir com autonomia.\n\n"
            "Inclui: confirmação do fluxo, mapas, diagramas, códigos reais,\n"
            "módulos 1–12, proposta de branch de estudos e Módulo 1 completo.",
            align="C",
        )
        self.ln(10)
        self.set_font("AppFont", "", 9)
        self.set_text_color(80, 80, 80)
        self._x()
        self.multi_cell(
            0,
            5,
            "Baseado no estado real do repositório.\n"
            "Diferencie sempre: (1) fato no código  (2) inferência  (3) melhoria ainda não existente.\n"
            "Regenerar: cd docs && python3 generate_study_roadmap.py",
            align="C",
        )

    def h1(self, text: str):
        self.add_page()
        self.set_font("AppFont", "B", 15)
        self.set_text_color(25, 55, 110)
        self.multi_cell(0, 8, text)
        self.ln(1)
        self.set_draw_color(25, 55, 110)
        y = self.get_y()
        self.line(16, y, 194, y)
        self.ln(4)
        self._x()

    def h2(self, text: str):
        self.ln(2.5)
        self._x()
        self.set_font("AppFont", "B", 11.5)
        self.set_text_color(35, 35, 35)
        self.multi_cell(0, 6.5, text)
        self.ln(1)

    def h3(self, text: str):
        self.ln(1.5)
        self._x()
        self.set_font("AppFont", "B", 10.5)
        self.set_text_color(55, 55, 55)
        self.multi_cell(0, 5.5, text)
        self.ln(0.5)

    def body(self, text: str):
        self._x()
        self.set_font("AppFont", "", 9.5)
        self.set_text_color(25, 25, 25)
        self.multi_cell(0, 5.2, text)
        self.ln(1.2)

    def bullet(self, text: str):
        self._x()
        self.set_font("AppFont", "", 9.5)
        self.set_text_color(25, 25, 25)
        self.multi_cell(0, 5.2, f"  •  {text}")

    def code(self, text: str):
        self._x()
        self.set_font("AppFont", "", 7.5)
        self.set_fill_color(242, 242, 242)
        self.set_text_color(15, 15, 15)
        for line in text.split("\n"):
            # Avoid empty lines collapsing oddly
            display = line if line.strip() != "" else " "
            self.cell(0, 4.2, "  " + display, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)
        self.set_font("AppFont", "", 9.5)

    def note(self, text: str):
        self._x()
        self.set_fill_color(230, 240, 250)
        self.set_font("AppFont", "", 8.5)
        self.set_text_color(25, 45, 75)
        self.multi_cell(0, 4.8, text, fill=True)
        self.ln(2)
        self.set_text_color(25, 25, 25)

    def warn(self, text: str):
        self._x()
        self.set_fill_color(255, 244, 230)
        self.set_font("AppFont", "", 8.5)
        self.set_text_color(90, 55, 20)
        self.multi_cell(0, 4.8, text, fill=True)
        self.ln(2)
        self.set_text_color(25, 25, 25)


def build_pdf() -> Path:
    regular, bold = ensure_fonts()
    pdf = RoadmapPDF(regular, bold)
    pdf.cover()

    # ========== 0 ==========
    pdf.h1("0. Como usar este roteiro")
    pdf.body(
        "Este PDF organiza o estudo do Weather App em módulos progressivos. "
        "Não é um manual para implementar features novas: o foco é compreender "
        "o que já existe — por que cada peça existe, como se conecta e quais "
        "alternativas existem."
    )
    pdf.h2("Método sugerido")
    pdf.bullet("Leia um módulo por sessão (comece pelo Módulo 1, completo neste PDF).")
    pdf.bullet("Abra os arquivos reais citados enquanto lê.")
    pdf.bullet("Responda às perguntas de revisão antes de avançar.")
    pdf.bullet("Faça os exercícios de leitura sem alterar o código (ou use branch de estudos).")
    pdf.h2("Perguntas-guia para cada conceito")
    pdf.bullet("O que é? — definição e terminologia")
    pdf.bullet("Onde está? — arquivo, classe, pacote, camada")
    pdf.bullet("O que faz? — responsabilidade prática")
    pdf.bullet("Por que existe? — problema que resolve")
    pdf.bullet("Como funciona? — sintaxe e interações")
    pdf.bullet("Como se conecta? — relação com o fluxo completo")
    pdf.bullet("Quais alternativas? — trade-offs")
    pdf.bullet("Como se relaciona com Node.js? — analogia cuidadosa (sem forçar)")

    # ========== 1 ==========
    pdf.h1("1. Confirmação do fluxo que você já estudou")
    pdf.body(
        "Você descreveu o fluxo de uma requisição que consulta a OpenWeather, "
        "trata JSON/erros e devolve uma resposta processada. Isso está correto "
        "para o caso GET com cache miss. Ressalvas importantes:"
    )
    pdf.bullet(
        "Nem toda requisição chama a OpenWeather. O WeatherService é cache-aside: "
        "primeiro PostgreSQL; só se a cidade não existir no banco a API externa entra."
    )
    pdf.bullet(
        "Há dois fluxos HTTP: GET /weather/{city} (busca + possível OpenWeather) e "
        "POST /weather (cria no banco; NÃO passa pela OpenWeather)."
    )
    pdf.bullet(
        "Erros têm famílias distintas: input inválido → 400 (@Valid); "
        "cidade inexistente → 404 (CityNotFoundException); "
        "falhas inesperadas (ex.: key inválida, DB) → hoje 500 genérico "
        "(ainda sem tratamento específico de erro externo)."
    )
    pdf.note(
        "FATO no código: a decisão 'DB primeiro, API depois' está em "
        "WeatherService.execute(String city), não no controller."
    )

    # ========== 2 ==========
    pdf.h1("2. Mapa inicial da aplicação")
    pdf.h2("Problema que a aplicação resolve")
    pdf.body(
        "API HTTP de clima para estudo: dado o nome de uma cidade, devolver "
        "temperatura e descrição, preferindo cache local e buscando na internet "
        "só quando necessário. Não é um produto completo (sem frontend, sem auth "
        "real, testes quase só smoke)."
    )
    pdf.h2("Diagrama — mapa de componentes")
    pdf.code(
        "+------------------+     +---------------------------------------------+\n"
        "|     Cliente      |     |         Nossa aplicação (backend)           |\n"
        "|  curl / futuro   |---->|  Security → Controller → UseCase/Service    |\n"
        "|    frontend      |     |       |              |                      |\n"
        "+------------------+     |       v              v                      |\n"
        "                        |  ExceptionHandler   Ports (interfaces)       |\n"
        "                        |                         |                    |\n"
        "                        |            +------------+------------+       |\n"
        "                        |            v                         v       |\n"
        "                        |   PersistenceAdapter      OpenWeatherAdapter |\n"
        "                        +------------+-------------------------+-------+\n"
        "                                     |                         |\n"
        "                                     v                         v\n"
        "                              +-----------+            +---------------+\n"
        "                              | PostgreSQL|            | OpenWeatherMap|\n"
        "                              |  (externo)|            |   (externo)   |\n"
        "                              +-----------+            +---------------+"
    )
    pdf.h2("Camadas (intenção hexagonal)")
    pdf.bullet("core.domain + core.ports — o 'quê' (Weather, contratos)")
    pdf.bullet("application.services — orquestração dos casos de uso (WeatherService)")
    pdf.bullet("infrastructure.* — HTTP, JPA, OpenWeather, Security, erros, validação")
    pdf.h2("Tecnologias e papéis")
    pdf.bullet("Java 21 — linguagem, records, tipagem estática")
    pdf.bullet("Spring Boot 4 — HTTP, DI, Security, Validation, JPA")
    pdf.bullet("PostgreSQL 15 + Flyway — persistência e migrations")
    pdf.bullet("OpenWeatherMap — fonte externa de clima")
    pdf.bullet("Docker Compose — sobe app + banco juntos")
    pdf.bullet("Maven Wrapper — dependências e build")
    pdf.h2("Nosso vs externo")
    pdf.bullet("Nosso: controllers, service, ports, adapters, security, validation, ApiError")
    pdf.bullet("Externo: OpenWeatherMap e o processo/container PostgreSQL")
    pdf.h2("Analogia Node.js (cuidado — não são iguais)")
    pdf.bullet("@RestController ≈ rotas Express/Fastify (mas com DI do Spring)")
    pdf.bullet("WeatherService + ports ≈ service + interface (estilo NestJS)")
    pdf.bullet("Adapter JPA ≈ Prisma/TypeORM atrás de uma interface")
    pdf.bullet("RestClient ≈ axios/fetch tipado")
    pdf.bullet("@ControllerAdvice ≈ middleware central de erro")
    pdf.warn(
        "Diferença: em Node a DI costuma ser manual ou NestJS; no Spring o container "
        "cria e injeta os beans sozinho. Não assuma que 'parecido' = 'igual'."
    )

    # ========== 3 ==========
    pdf.h1("3. Caminho de uma requisição real")
    pdf.h2("Exemplo concreto: GET /weather/Porto (cache miss)")
    pdf.bullet("1. Cliente: curl http://localhost:8080/weather/Porto")
    pdf.bullet("2. Tomcat + Security: rota pública (permitAll)")
    pdf.bullet("3. WeatherController: extrai city do path (@PathVariable)")
    pdf.bullet("4. GetWeatherUseCase → WeatherService: orquestra a regra")
    pdf.bullet("5. WeatherRepositoryPort → PersistenceAdapter → JPA: SELECT vazio")
    pdf.bullet("6. ExternalWeatherPort → OpenWeatherExternalAdapter: HTTP na OpenWeather")
    pdf.bullet("7. JSON → OpenWeatherResponse → Weather (infrastructure → domínio)")
    pdf.bullet("8. Repository save: INSERT em tb_weather")
    pdf.bullet("9. Controller: 200 + JSON do Weather")
    pdf.body(
        "Segunda chamada ao mesmo path: passos 6–7 NÃO ocorrem (cache hit). "
        "POST inválido para no @Valid → GlobalExceptionHandler → 400 (service nem roda)."
    )
    pdf.h2("Diagrama de sequência (cache miss vs hit)")
    pdf.code(
        "CACHE MISS (1ª vez Porto)              CACHE HIT (2ª vez Porto)\n"
        "---------------------------            --------------------------\n"
        "Cliente → Controller                   Cliente → Controller\n"
        "       → Service                              → Service\n"
        "       → DB findByCity (vazio)                 → DB findByCity (achou)\n"
        "       → OpenWeather fetch                     → return Weather\n"
        "       → DB save                               → 200 JSON\n"
        "       → return Weather\n"
        "       → 200 JSON"
    )
    pdf.h2("Código real — decisão no WeatherService")
    pdf.note("Arquivo: backend/.../application/services/WeatherService.java")
    pdf.code(
        "@Override\n"
        "public Weather execute(String city) {\n"
        "    return weatherRepositoryPort.findByCity(city)\n"
        "        .orElseGet(() -> {\n"
        "            Weather externalWeather = externalWeatherPort.fetchWeather(city)\n"
        "                .orElseThrow(() -> new CityNotFoundException(city));\n"
        "            return weatherRepositoryPort.save(externalWeather);\n"
        "        });\n"
        "}"
    )
    pdf.h2("Código real — entrada HTTP (controller fino)")
    pdf.note("Arquivo: backend/.../infrastructure/controllers/WeatherController.java")
    pdf.code(
        "@GetMapping(\"/{city}\")\n"
        "public ResponseEntity<Weather> getWeather(@PathVariable String city) {\n"
        "    Weather weather = getWeatherUseCase.execute(city);\n"
        "    return ResponseEntity.ok(weather);\n"
        "}\n"
        "\n"
        "@PostMapping\n"
        "public ResponseEntity<Weather> createWeather(\n"
        "        @Valid @RequestBody WeatherRequest request) { ... }"
    )
    pdf.h2("Porta de saída — contrato (sem saber OpenWeather)")
    pdf.note("Arquivo: backend/.../core/ports/ExternalWeatherPort.java")
    pdf.code(
        "public interface ExternalWeatherPort {\n"
        "    Optional<Weather> fetchWeather(String city);\n"
        "}"
    )

    # ========== 4 ==========
    pdf.h1("4. Estrutura dos módulos (ordem recomendada)")
    pdf.body(
        "Estude nesta ordem. Cada módulo deve responder: o quê / onde / por quê / "
        "como / Node. Ritmo sugerido: 1 módulo por sessão."
    )
    modules = [
        ("1", "Visão geral da aplicação", "Mapa mental antes dos detalhes — COMPLETO neste PDF"),
        ("2", "Linguagem, sintaxe e tipagem (Java)", "Ler o código sem 'mágica'"),
        ("3", "Framework, HTTP e ciclo de vida", "Seguir uma request no Spring"),
        ("4", "Integração OpenWeather", "Caso de estudo da API externa"),
        ("5", "Arquitetura hexagonal (crítica)", "O que está bem e o que é simplificação"),
        ("6", "Clean Code, SOLID e design", "Julgar decisões no código real"),
        ("7", "Banco de dados e persistência", "Entity vs Domain, Flyway, JPA"),
        ("8", "Pacotes e estrutura do projeto", "Localizar responsabilidades"),
        ("9", "Docker, Maven e ferramentas", "Como o sistema sobe e se configura"),
        ("10", "Testes — visão introdutória", "Como travaríamos o conhecimento (sem implementar ainda)"),
        ("11", "Possível frontend", "Consumo HTTP superficial"),
        ("12", "Revisão e consolidação", "Glossário, mapas, autoavaliação"),
    ]
    for num, title, why in modules:
        pdf.bullet(f"Módulo {num} — {title}. Por quê: {why}.")
    pdf.h2("Checklist mental por módulo")
    pdf.bullet("Ler a visão do módulo")
    pdf.bullet("Abrir 1–3 arquivos reais citados")
    pdf.bullet("Responder: o que / onde / por quê / como se conecta")
    pdf.bullet("Fazer analogia Node.js (só se houver equivalência real)")
    pdf.bullet("Responder perguntas de revisão")
    pdf.bullet("Só então avançar")

    # ========== 5 ==========
    pdf.h1("5. Proposta: branch de estudos")
    pdf.body(
        "Sugestão (criar só após sua aprovação): manter main limpa para desenvolvimento "
        "e uma branch study/guide para material didático."
    )
    pdf.code(
        "main          → código de desenvolvimento\n"
        "study/guide   → mesma base + docs/comentários de estudo\n\n"
        "git checkout main\n"
        "git checkout study/guide\n"
        "git checkout study/guide && git merge main   # atualizar estudos"
    )
    pdf.h2("Onde colocar o material")
    pdf.bullet("Principal: docs/study/01-visao-geral.md … 12-consolidacao.md")
    pdf.bullet("Opcional: docs/study/REQUEST-WALKTHROUGH.md")
    pdf.h2("Comentários no código — riscos")
    pdf.bullet("Prós de comentar nos .java: contexto imediato ao ler a classe")
    pdf.bullet("Contras: merge ruidoso com main; risco de commit acidental na main")
    pdf.bullet(
        "Recomendação: docs em docs/study/; no código só TO LEARN curtos "
        "(já existem alguns), sem ensaios longos nas classes"
    )
    pdf.warn(
        "Nada desta proposta foi aplicada automaticamente. Branch e arquivos "
        "só depois da sua aprovação explícita."
    )

    # ========== 6 ==========
    pdf.h1("6. Agenda detalhada — Módulos 2 a 12")
    pdf.body(
        "O Módulo 1 está completo na seção seguinte. Os módulos 2–12 são o roteiro "
        "do que estudar em sessões futuras (ainda a aprofundar)."
    )

    pdf.h2("Módulo 2 — Java: linguagem e tipagem")
    pdf.bullet("Classes, interfaces, records, construtores (Weather, WeatherEntity)")
    pdf.bullet("Tipagem estática vs JS; Optional; genéricos")
    pdf.bullet("Modificadores public/private/protected; final")
    pdf.bullet("Annotations (@Service, @Component…) vs decorators Nest/TS")
    pdf.bullet("Exceções (CityNotFoundException) vs throw em Node")
    pdf.bullet("DI por construtor — ciclo de vida dos beans Spring")
    pdf.bullet("Separar: o que é Java puro vs o que é Spring")

    pdf.h2("Módulo 3 — Framework, HTTP e ciclo de vida")
    pdf.bullet("WeatherController: @RestController, @GetMapping, @PostMapping")
    pdf.bullet("@PathVariable, @RequestBody, ResponseEntity, status 200/201")
    pdf.bullet("WeatherRequest + @Valid + Bean Validation → 400")
    pdf.bullet("Serialização JSON (Jackson) do record Weather")
    pdf.bullet("GlobalExceptionHandler / ApiError")
    pdf.bullet("Exercício: acompanhar GET e POST passo a passo")

    pdf.h2("Módulo 4 — OpenWeather")
    pdf.bullet("Por que a responsabilidade está no adapter, não no service")
    pdf.bullet("RestClient + OpenWeatherConfig + WEATHER_API_KEY")
    pdf.bullet("OpenWeatherResponse (DTO) vs Weather (domínio)")
    pdf.bullet("O que o código faz hoje em 404 vs 401/timeout (fato vs melhoria)")
    pdf.bullet("Profile mock vs !mock")
    pdf.h3("Código real — esqueleto do adapter")
    pdf.note("Arquivo: .../adapters/out/external/OpenWeatherExternalAdapter.java")
    pdf.code(
        "@Component\n"
        "@Profile(\"!mock\")\n"
        "public class OpenWeatherExternalAdapter implements ExternalWeatherPort {\n"
        "    // RestClient + apiKey injetados\n"
        "    public Optional<Weather> fetchWeather(String city) {\n"
        "        // GET /weather?q=...&appid=...&units=metric&lang=pt_br\n"
        "        // 404 → Optional.empty()\n"
        "        // sucesso → Optional.of(new Weather(city, temp, desc, now))\n"
        "    }\n"
        "}"
    )

    pdf.h2("Módulo 5 — Hexagonal (análise crítica)")
    pdf.bullet("Ports de entrada (use cases) e saída (repository, external)")
    pdf.bullet("Direção das dependências: infrastructure → core, não o contrário")
    pdf.bullet("O que está bem vs simplificações (controller devolve domain)")
    pdf.code(
        "Dependências desejadas:\n"
        "  Controller ──usa──► UseCase (port in)\n"
        "  Service     ──usa──► RepositoryPort / ExternalPort\n"
        "  Adapters    ──implementam──► Ports\n"
        "  Domain      ──não conhece──► Spring / JPA / OpenWeather"
    )

    pdf.h2("Módulo 6 — Clean Code e SOLID")
    pdf.bullet("SRP: controller fino vs service orquestrador")
    pdf.bullet("ISP: GetWeatherUseCase vs SaveWeatherUseCase no controller")
    pdf.bullet("DIP: service depende de ports, não de JPA/OpenWeather")
    pdf.bullet("Custos de abstração desnecessária — quando NÃO criar interface")

    pdf.h2("Módulo 7 — Persistência")
    pdf.bullet("PostgreSQL neste projeto; env vars no Compose")
    pdf.bullet("WeatherEntity vs Weather vs WeatherRequest")
    pdf.bullet("Flyway V1__create_tb_weather.sql; ddl-auto=none")
    pdf.bullet("UNIQUE city; 409 ainda NÃO implementado")

    pdf.h2("Módulo 8 — Árvore de pacotes")
    pdf.code(
        "weather-app/\n"
        "  docker-compose.yml   .env.example   README.md\n"
        "  docs/                (PDFs + geradores Python)\n"
        "  backend/\n"
        "    pom.xml  dockerfile  scripts/start.sh\n"
        "    src/main/java/com/weather_app/\n"
        "      core/  application/  infrastructure/\n"
        "    src/main/resources/\n"
        "      application.properties\n"
        "      db/migration/V1__create_tb_weather.sql"
    )

    pdf.h2("Módulo 9 — Docker e ferramentas")
    pdf.bullet("Imagem vs container; portas; rede Compose")
    pdf.bullet(".env / WEATHER_API_KEY; rebuild vs up")
    pdf.bullet("Logs: docker logs weather-backend")
    pdf.bullet("Maven: ./mvnw compile / test / package")

    pdf.h2("Módulo 10 — Testes (visão, sem implementar agora)")
    pdf.bullet("Unitário do WeatherService com mocks dos ports")
    pdf.bullet("@WebMvcTest para 400/404/201")
    pdf.bullet("Por que hexagonal facilita testes")
    pdf.bullet("Comparar com Jest + supertest / Nest testing")

    pdf.h2("Módulo 11 — Frontend possível")
    pdf.bullet("fetch/axios → mesmos endpoints e status")
    pdf.bullet("Loading / erro / ApiError.fieldErrors")
    pdf.bullet("CORS e auth como decisões futuras (não existem no app hoje)")

    pdf.h2("Módulo 12 — Consolidação (entregáveis)")
    pdf.bullet("Mapa da arquitetura com suas palavras")
    pdf.bullet("Diagrama do fluxo completo")
    pdf.bullet("Glossário + tabela Java ↔ Node")
    pdf.bullet("Comandos úteis; pontos fortes/limitações/melhorias")
    pdf.bullet("Roteiro de autoavaliação")

    # ========== 7 Module 1 ==========
    pdf.h1("7. Módulo 1 completo — Visão geral da aplicação")
    pdf.h2("O que é este projeto?")
    pdf.body(
        "Uma API HTTP de clima para estudo. Resolve: dado o nome de uma cidade, "
        "devolver temperatura/descrição, preferindo cache local e buscando na "
        "internet só quando necessário."
    )
    pdf.h2("Como está organizado?")
    pdf.code(
        "backend/src/main/java/com/weather_app/\n"
        "  core/domain          Weather, CityNotFoundException\n"
        "  core/ports           Get/Save use cases + Repository + External ports\n"
        "  application/services WeatherService\n"
        "  infrastructure/\n"
        "    controllers        REST, WeatherRequest, ApiError, GlobalExceptionHandler\n"
        "    config             SecurityConfig, OpenWeatherConfig\n"
        "    adapters/out/\n"
        "      persistence      WeatherEntity, JpaRepository, PersistenceAdapter\n"
        "      external         OpenWeather* + WeatherMockExternalAdapter"
    )
    pdf.h2("Componentes no fluxo GET")
    pdf.bullet("WeatherController — entrada HTTP")
    pdf.bullet("GetWeatherUseCase / WeatherService — regra cache-aside")
    pdf.bullet("WeatherRepositoryPort / PersistenceAdapter — Postgres")
    pdf.bullet("ExternalWeatherPort / OpenWeatherExternalAdapter — API")
    pdf.bullet("GlobalExceptionHandler — tradução de falhas em JSON HTTP")
    pdf.h2("Jornada da requisição (visão única)")
    pdf.code(
        "Cliente\n"
        "  → Security (permitAll em /weather/**)\n"
        "  → WeatherController\n"
        "  → WeatherService\n"
        "       ├─ findByCity (Postgres)\n"
        "       │     hit  → retorna Weather\n"
        "       │     miss → fetchWeather (OpenWeather)\n"
        "       │              empty → CityNotFoundException → 404 ApiError\n"
        "       │              ok    → save (Postgres) → retorna Weather\n"
        "  → 200 JSON\n"
        "\n"
        "POST /weather + body inválido:\n"
        "  → @Valid falha → MethodArgumentNotValidException → 400 + fieldErrors\n"
        "  (WeatherService NÃO executa)"
    )
    pdf.h2("Hexagonal: fato vs simplificação")
    pdf.bullet("Presente: ports, adapters, domínio sem JPA/OpenWeather")
    pdf.bullet(
        "Simplificações: controller devolve record de domínio; "
        "um service implementa dois use cases; testes quase ausentes"
    )
    pdf.h2("Comparação rápida Node.js")
    pdf.code(
        "Aqui                              |  Node (aproximação)\n"
        "----------------------------------|--------------------------------\n"
        "@RestController                   |  rotas Express/Fastify\n"
        "WeatherService + ports            |  service + interface/DI\n"
        "WeatherRepositoryPort             |  repository interface\n"
        "Adapter JPA                       |  Prisma/TypeORM impl\n"
        "Adapter OpenWeather               |  axios client isolado\n"
        "@ControllerAdvice / ApiError      |  error middleware\n"
        "record Weather                    |  type + objeto imutável"
    )
    pdf.h2("Resumo do Módulo 1")
    pdf.bullet("App = API de clima com cache Postgres + fallback OpenWeather")
    pdf.bullet("GET e POST são fluxos diferentes")
    pdf.bullet("Externos: DB e OpenWeather; o resto é nosso")
    pdf.bullet("Hexagonal útil, não 'pura de livro'")
    pdf.h2("Conceitos essenciais")
    pdf.body(
        "Cache-aside · Port/Adapter · Domínio vs Infrastructure · "
        "Request lifecycle · Boundary com sistema externo"
    )
    pdf.h2("Perguntas de revisão — Módulo 1")
    pdf.bullet("1. Por que a segunda chamada a /weather/Porto não precisa da OpenWeather?")
    pdf.bullet("2. Qual componente decide 'DB primeiro, API depois'?")
    pdf.bullet("3. O POST usa a OpenWeather? Por quê?")
    pdf.bullet("4. Cite uma coisa nossa e uma externa no fluxo GET.")
    pdf.bullet(
        "5. Em Node, o que mais se parece com ExternalWeatherPort + "
        "OpenWeatherExternalAdapter?"
    )
    pdf.h2("Exercício de leitura (sem mudar código)")
    pdf.body(
        "Abra WeatherService.execute(String city) e, em voz alta ou no papel, "
        "numere os 3 passos do comentário Smart Flow. Digue qual classe concreta "
        "o Spring injeta hoje em cada port — com profile padrão e com profile mock."
    )
    pdf.h2("Espaço para suas respostas (escreva à mão)")
    pdf.ln(1)
    for i in range(1, 6):
        pdf.body(f"{i}.")
        pdf.ln(1)
        pdf.set_draw_color(180, 180, 180)
        for _ in range(3):
            y = pdf.get_y()
            pdf.line(16, y, 194, y)
            pdf.ln(7)
        pdf.ln(2)

    # ========== 8 ==========
    pdf.h1("8. Comandos úteis (referência rápida)")
    pdf.h2("Docker")
    pdf.code(
        "docker compose build backend\n"
        "docker compose up -d\n"
        "docker compose logs -f backend\n"
        "docker compose down"
    )
    pdf.h2("API — smoke e cenários de estudo")
    pdf.code(
        "curl -s http://localhost:8080/hello\n"
        "\n"
        "# cache miss / hit\n"
        "curl -s http://localhost:8080/weather/Porto | python3 -m json.tool\n"
        "\n"
        "# 404 ApiError\n"
        "curl -s http://localhost:8080/weather/CidadeXYZ | python3 -m json.tool\n"
        "\n"
        "# 400 validation\n"
        "curl -s -X POST http://localhost:8080/weather \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        "  -d '{\"city\":\"\",\"temperature\":null,\"description\":\"\"}' | python3 -m json.tool\n"
        "\n"
        "# 201 create\n"
        "curl -s -i -X POST http://localhost:8080/weather \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        "  -d '{\"city\":\"Coimbra\",\"temperature\":22.0,\"description\":\"Sol\"}'"
    )
    pdf.h2("Build local")
    pdf.code("cd backend && ./mvnw compile\ncd backend && ./mvnw test")
    pdf.h2("Regenerar este PDF")
    pdf.code("cd docs\npython3 generate_study_roadmap.py\n# ou: .venv/bin/python generate_study_roadmap.py")

    # ========== 9 ==========
    pdf.h1("9. Estado atual — o que estudar vs o que NÃO inventar")
    pdf.h2("Já implementado (pode estudar no código)")
    pdf.bullet("Hexagonal básico, GET/POST weather, Flyway, OpenWeather, mock profile")
    pdf.bullet("ApiError: 404 cidade, 400 validação (+ fieldErrors), 500 fallback")
    pdf.bullet("Docker Compose + WEATHER_API_KEY via .env")
    pdf.bullet("Documentação README + backend/documentation.md alinhadas")
    pdf.h2("Ainda NÃO implementado")
    pdf.bullet("409 cidade duplicada; 502 falha OpenWeather; 400 JSON malformado dedicado")
    pdf.bullet("Testes automatizados além do smoke; TTL de cache; Actuator; OpenAPI; JWT")
    pdf.bullet("Frontend; Kafka; Cucumber; CI")
    pdf.note(
        "Ao estudar, diferencie sempre: (1) fato no código, (2) inferência, "
        "(3) melhoria recomendada mas não existente."
    )

    # ========== 10 ==========
    pdf.h1("10. Resultado esperado e próximos passos")
    pdf.body(
        "Ao concluir o roteiro completo, você deve conseguir, com suas próprias palavras: "
        "explicar a arquitetura; acompanhar uma requisição de ponta a ponta; justificar "
        "as principais decisões técnicas; e dizer como cada tecnologia participa do "
        "sistema — incluindo limitações conscientes do MVP de estudo."
    )
    pdf.h2("Próximo passo sugerido agora")
    pdf.bullet("Imprimir este PDF e responder as perguntas do Módulo 1 à mão")
    pdf.bullet("Decidir se quer a branch study/guide + docs/study/")
    pdf.bullet("Avançar para o Módulo 2 (Java/sintaxe com exemplos reais do projeto)")
    pdf.ln(6)
    pdf.set_font("AppFont", "B", 11)
    pdf.set_text_color(25, 55, 110)
    pdf._x()
    pdf.multi_cell(0, 6, "Fim do roteiro de partida — bom estudo.", align="C")

    pdf.output(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    path = build_pdf()
    print(f"PDF generated: {path}")
