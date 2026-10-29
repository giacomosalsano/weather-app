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

## Study materials (PDFs)

| File | Purpose | Regenerate |
|------|---------|------------|
| **[Roteiro-Estudo-Weather-App.pdf](./Roteiro-Estudo-Weather-App.pdf)** | Printable study roadmap (modules 1–12, Module 1 complete, request flow, commands) | `python3 generate_study_roadmap.py` |
| **[Guia-Arquitetura-Hexagonal-Weather-App.pdf](./Guia-Arquitetura-Hexagonal-Weather-App.pdf)** | Broader hexagonal study guide (may lag behind the code) | `python3 generate_study_guide.py` |

> For the current implemented state of the app, also prefer the root [`README.md`](../README.md) and [`backend/documentation.md`](../backend/documentation.md).

## Regenerate

```bash
cd docs
python3 generate_study_roadmap.py   # printable architecture study roadmap
python3 generate_study_guide.py     # older broader hexagonal guide
```

On macOS, the scripts use the system **Arial Unicode** font for UTF-8 (Portuguese) rendering.
